#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
#

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------
import os
import sys

def getInstanceNumber(paramName,index):
                try:
                    instanceNumber = 0
                    paramList = paramName.split(".")
                    instanceNumber = paramList[index]
                except:
                        return 0
                return instanceNumber

def readtdkbConfigFile(self):

# Reads config file and returns the value.

# Syntax      : OBJ.readtdkbConfigFile()
# Description : Reads config file and returns the value.
# Parameters  : configFile - Name of config file.
# Return Value: value given in the config file

        configFile = self.realpath + "fileStore/" + "tdkb.config"
        print "Configuration File Found : ", configFile
        sys.stdout.flush()

        # Checking if file exists
        fileCheck = os.path.isfile(configFile)
        if (fileCheck):
                for line in open(configFile).readlines():
                        if "HOST_NAME" in line:
                                HostName=line.rsplit(None, 1)[-1];
                                print "Host name is %s" %HostName;
        else:
                print "Configuration File does not exist."
                sys.stdout.flush()
                exit()

        return HostName;

########## End of Function ##########
