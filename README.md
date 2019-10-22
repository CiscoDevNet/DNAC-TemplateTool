# Template tools
This tool allows you to save and restore Cisco DNAC Cetner templates from the controller.  It uses the newly released 
CiscoDNACenter SDK.

Currenty, it does not support composite templates

## Getting stated
First (optional) step, create a vitualenv. This makes it less likely to clash with other python libraries in future.
Once the virtualenv is created, need to activate it.
```buildoutcfg
python3 -m venv env3
source env3/bin/activate
```

Next clone the code.

```buildoutcfg
git clone https://github.com/CiscoDevNet/DNAC-TemplateTool.git
```

Then install the  requirements (after upgrading pip). 
Older versions of pip may not install the requirements correctly.
```buildoutcfg
pip install -U pip
pip install -r requirements.txt
```

## Environment variables
The DNAC, username and passowrd of DNAC is specified in environment varaibles.  An example is provided in dnac_vars.
You can edit this file and use the "source" command to put the variables in your shell environment.
```buildoutcfg
source vars_dnac
```

## Archiving the templates.
Just running the script with no argumnents will dump all of the templates in json format.  You can save this to a file.
```buildoutcfg
$ ./template_archive.py > all.json
```

## Restoring the templates
Simply run the script with the --restore <filename> option
```buildoutcfg
$ ./template_archive.py --restore all.json
['Cloud DayN Templates/DMVPN Spoke for Branch Router - System Default/1', 'Cloud DayN Templates/DMVPN for Cloud Router - System Default/1', 'Cloud DayN Templates/IPsec for Branch Router - System Default/1', 'Cloud DayN Templates/IPsec for Cloud Router - System Default/1', 'Onboarding Configuration/3k-stack/1', 'Onboarding Configuration/3k-stack/2', 'Onboarding Configuration/9300-sdwan/1', 'Onboarding Configuration/DMVPN Hub for Cloud Router- System Default/1', 'Onboarding Configuration/IPsec 1 Branch for Cloud Router - System Default/1', 'Onboarding Configuration/IPsec 2 Branch for Cloud Router - System Default/1', 'adam/int-desc/1', 'adam/int-desc/2', 'adam/int-desc/3', 'adam/int-desc/4', 'adam/int-desc/5', 'adam/loop/1', 'adam/loop/2', 'adam/loop/3']
Updating template:DMVPN Spoke for Branch Router - System Default, CurrentVesion:1, NewVersion:1
Skipping template DMVPN Spoke for Branch Router - System Default, version 1.  Mismatch with existing version1
Updating template:DMVPN for Cloud Router - System Default, CurrentVesion:1, NewVersion:1
Skipping template DMVPN for Cloud Router - System Default, version 1.  Mismatch with existing version1
Updating template:IPsec for Branch Router - System Default, CurrentVesion:1, NewVersion:1
Skipping template IPsec for Branch Router - System Default, version 1.  Mismatch with existing version1
Updating template:IPsec for Cloud Router - System Default, CurrentVesion:1, NewVersion:1
Skipping template IPsec for Cloud Router - System Default, version 1.  Mismatch with existing version1
Updating template:3k-stack, CurrentVesion:2, NewVersion:1
Skipping template 3k-stack, version 1.  Mismatch with existing version2
Updating template:3k-stack, CurrentVesion:2, NewVersion:2
Skipping template 3k-stack, version 2.  Mismatch with existing version2
Updating template:9300-sdwan, CurrentVesion:1, NewVersion:1
Skipping template 9300-sdwan, version 1.  Mismatch with existing version1
Updating template:DMVPN Hub for Cloud Router- System Default, CurrentVesion:1, NewVersion:1
Skipping template DMVPN Hub for Cloud Router- System Default, version 1.  Mismatch with existing version1
Updating template:IPsec 1 Branch for Cloud Router - System Default, CurrentVesion:1, NewVersion:1
Skipping template IPsec 1 Branch for Cloud Router - System Default, version 1.  Mismatch with existing version1
Updating template:IPsec 2 Branch for Cloud Router - System Default, CurrentVesion:1, NewVersion:1
Skipping template IPsec 2 Branch for Cloud Router - System Default, version 1.  Mismatch with existing version1

```
you will notice nothing seemed to happen, as I was restoring the exact same templates as I saved.

The script is smart enough to match the versions of the template, and will not add the tempalte if it is already present.

If i was to delete a template or a folder, those templates would be re-added, or i could point the script to a new DNAC and upddate it.


