#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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

import ConfigParser
from pexpect import pxssh

def executeBluetoothCtl(bluetoothObj,commands):

    try :
 
        #Get Bluetooth configuration file
        bluetoothConfigFile = bluetoothObj.realpath+'fileStore/bluetoothcredential.config'
        configParser = ConfigParser.ConfigParser()
        configParser.read(r'%s' % bluetoothConfigFile)
        ip = configParser.get('bluetooth-config', 'ip')
        username = configParser.get('bluetooth-config', 'username')
        password = configParser.get('bluetooth-config', 'password')
        global deviceName;
        deviceName = configParser.get('bluetooth-config','devicename')
        #Executing the commands in device
        print 'Number of commands:', len(commands)
        print 'Commands List:', commands
        print "Connecting to client device"
        global session
        session = pxssh.pxssh(options={
                            "StrictHostKeyChecking": "no",
                            "UserKnownHostsFile": "/dev/null"})
        session.login(ip,username,password)
        print "Executing the bluetoothctl commands"
        for parameters in range(0,len(commands)):
            session.sendline(commands[parameters])
        session.prompt()
        status=session.before
        status=status.strip()
        session.logout()
        session.close()
        print "Successfully Executed bluetoothctl commands in client device"

    except Exception, e:
        print e;
        status = "FAILURE"
        
    return status
