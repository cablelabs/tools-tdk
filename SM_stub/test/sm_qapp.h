/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
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
#include "libIARM.h"
#include "rdktestagentintf.h"

#define PORT 0
#define FAIL 1

class AVIListener : public ServiceListener
{
public:
       	void onServiceEvent(const QString& event, ServiceParams params);
};

class DisListener : public ServiceListener
{
public:
        void onServiceEvent(const QString& event, ServiceParams params);
};
