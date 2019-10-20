# Template tools
This tool allows you to save and restore Cisco DNAC Cetner templates from the controller.  It uses the newly released 
CiscoDNACenter SDK.

Currenty, it does not support composite templates

## Getting stated
First (optional) step, create a vitualenv. This makes it less likely to clash with other python libraries in future.
Once the virtualenv is created, need to activate it.
```buildoutcfg
python3 -mvenv env3
source env3/bin/activate
```

Next clone the code.

```buildoutcfg
git clone https://github.com/CiscoDevNet/DNAC-NOC.git
```

Then install the  requirements (after upgrading pip). 
Older versions of pip may not install the requirements correctly.
```buildoutcfg
pip install -U pip
pip install -r DNAC-NOC/requirements.txt