#!/usr/bin/env python
from __future__ import print_function
import json
import requests
import time
# turn off warninggs
requests.packages.urllib3.disable_warnings()
import re
import logging
from argparse import ArgumentParser
from dnacentersdk import api

# create a logger
logger = logging.getLogger(__name__)

class TaskTimeoutError(Exception):
    pass

class TaskError(Exception):
    pass

def wait_for_task(dnac, taskid, retry=2, timeout=10):
    start_time = time.time()
    first = True
    while True:
        result = dnac.task.get_task_by_id(taskid)

        # print json.dumps(response)
        if result.response.endTime is not None:
            return result
        else:
            # print a message the first time throu
            if first:
                logger.debug("Task:{} not complete, waiting {} seconds, polling {}".format(taskid, timeout, retry))
                first = False
            if timeout and (start_time + timeout < time.time()):
                raise TaskTimeoutError("Task %s did not complete within the specified timeout "
                                       "(%s seconds)" % (taskid, timeout))

            logging.debug("Task=%s has not completed yet. Sleeping %s seconds..." % (taskid, retry))
            time.sleep(retry)

        if result.response.isError == "True":
            raise TaskError("Task %s had error %s" % (taskid, result.response.progress))

    return response

def atoi(text):
    return int(text) if text.isdigit() else text

# natural sort for templates
def natural_sort(templatelist):
    return sorted(templatelist, key=lambda template: [ atoi(c) for c in re.split('(\d+)', template)])

def archive_templates(dnac):
    # get all of the templates and projects.
    templates = dnac.template_programmer.gets_the_templates_available()
    #print(json.dumps(result, indent=2))
    archive={}
    total = 0
    for template in templates:
        name = template.name
        project= template.projectName

        # this was for testing
        #if project != "archive":
        #    continue

        for version in template.versionsInfo:
            total += 1
            templateversion = dnac.template_programmer.get_template_details(version.id)
            archive['{}/{}/{}'.format(project, name, version['version'])] = templateversion

    print(json.dumps(archive, indent=2))
    logger.info("total:{}".format(total))

def split_name(name):
    parts = name.split("/")
    project = parts[0]
    if len(parts) > 3:
        name = '/'.join(parts[1:-1])
    else:
        name = parts[1]
    version = parts[-1]
    return project, name, version

def find_or_create_project(dnac, project):
    projects =  dnac.template_programmer.get_projects(name=project)
    try:
        projectid = projects[0].id

    except IndexError as e:
        print("Creating project:{}".format(project))
        response = dnac.template_programmer.create_project(name=project)
        project_response = wait_for_task(dnac, response.response.taskId)
        logger.debug(json.dumps(project_response))
        projectid = project_response.response.data

    logger.debug("returning projectId:{}".format(projectid))
    return projectid


def create_or_update_template(dnac, projectid, name, version, newtemplate):

    # cannot search for a template by name
    templates = dnac.template_programmer.gets_the_templates_available(project_id=projectid)
    logger.debug('templates:{}'.format(json.dumps(templates)))

    for template in templates:
        # if match name, then we need to update template
        if template.name == name:
            maxversion = max([int(v.version) for v in template.versionsInfo])
            print("Updating template:{}, CurrentVesion:{}, NewVersion:{}".format(name, maxversion, version))

            # look for version mismatch,
            if (maxversion + 1) != int(version):
                print("Skipping template {}, version {}.  Mismatch with existing version{}".format(name, version, maxversion))
                return None
            logger.debug("found template:{}".format(template))

            newtemplate['projectId']= projectid
            newtemplate['id'] = template.templateId
            newtemplate['parentTemplateId'] = template['templateId']
            logger.debug("update template:{}".format(json.dumps(newtemplate)))
            response = dnac.template_programmer.update_template(**newtemplate)
            template_response = wait_for_task(dnac, response.response.taskId)
            logger.debug(json.dumps(template_response))
            templateid = template_response.response.data
            return templateid

    # create template
    logger.debug('create template;{}'.format(json.dumps(newtemplate)))
    print("Creating template:{}, NewVersion:{}".format(name,  version))
    response = dnac.template_programmer.create_template(**newtemplate, project_id=projectid)
    template_response = wait_for_task(dnac, response.response.taskId)
    logger.debug(json.dumps(template_response))
    templateid = template_response.response.data
    return templateid


def add_template(dnac,project, name, version, template):

    # look to see if project exists
    projectid = find_or_create_project(dnac, project)

    # either create the template or update it
    templateid = create_or_update_template(dnac, projectid, name, version, template)

    # version template..  If the version mismatches, then do not version
    if templateid is not None:
        response = dnac.template_programmer.version_template(templateId=templateid)
        logging.debug('version {}'.format(json.dumps(response)))


def clean_template(template):
    template.pop('id')
    template.pop('createTime')
    template.pop('lastUpdateTime')
    template.pop('parentTemplateId')

    # need to clean vars.
    for var in template['templateParams']:
        var.pop('id')

    return template

def restore_templates(dnac, file):
    with open(file) as f:
        templates = json.load(f)
        print(natural_sort(templates.keys()))
        for key in natural_sort(templates.keys()):
            project,name,version = split_name(key)
            template = clean_template(templates[key])


            add_template(dnac, project,name,version, template)


if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--restore', type=str, required=False,
                        help="restore from file   ")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()

    if args.v:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.debug("logging enabled")

    dnac =api.DNACenterAPI()

    if args.restore:
        restore_templates(dnac, args.restore)
    else:
        archive_templates(dnac)
