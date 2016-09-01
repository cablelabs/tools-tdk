/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file (and its contents) are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#include <iostream>
#include <stdio.h>
#include <QApplication>
#include <unistd.h>
#include "servicemanager.h"
#include "servicelistener.h"
#include "avinputservice.h"
#include "displaysettingsservice.h"
#include "dsDisplay.h"
#include "servicemanagernotifier.h"
#include "dsMgr.h"
#include "libIBus.h"
#include "rdktestagentintf.h"

#define PORT 0
#define FAIL 1

class AVIListener : public ServiceListener
{
public:
       	void onServiceEvent(const QString& event, ServiceParams params);
};
