#!/usr/bin/python

import os
import yaml
import datetime
import logging

LOGGER = logging.getLogger("frague")

# File methods
def read_file(file_name, open_type="r"):
    result = ""
    LOGGER.debug("Reading file \"%s\"" % file_name)
    if os.path.exists(file_name):
        rf = file(file_name, open_type)
        result = rf.read()
        rf.close()
        LOGGER.debug("File reading succeeded - %s bytes read" % len(result))
    return result

def write_file(file_name, contents):
    LOGGER.debug("Writing file \"%s\"" % file_name)
    wf = file(file_name, "w")
    wf.write(contents)
    wf.close()

def get_config(config_file="config.yaml"):
    return yaml.load(read_file(config_file))



# Date & time methods
today = datetime.datetime.now()

def printable_date(d):
    return d.strftime("%B, %d (%A)")
