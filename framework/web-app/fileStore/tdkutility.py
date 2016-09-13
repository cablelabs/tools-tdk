#!/usr/bin/python
#
# ============================================================================
# COMCAST C O N F I D E N T I A L AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of Comcast.  It may
# not be used, copied, distributed or otherwise  disclosed in whole or in part
# without the express written permission of Comcast.
# ============================================================================
# Copyright (c) 2016 Comcast. All rights reserved.
# ============================================================================
#

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------

def getInstanceNumber(paramName,index):
                try:
                    instanceNumber = 0
                    paramList = paramName.split(".")
                    instanceNumber = paramList[index]
                except:
                        return 0
                return instanceNumber
