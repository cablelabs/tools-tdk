#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2014 Comcast. All rights reserved.
#  ============================================================================

QT += widgets network core gui
DEFINES += HAS_API_HDMI_CEC USE_DEVICE_SETTINGS_SERVICE SCREEN_CAPTURE ENABLE_WEBSOCKET_SERVICE HAS_API_APPLICATION DEBUG_LEVEL_TRACE RDK2DOT0

DEFINES += $$CEC_PERSIST_NAME

greaterThan(QT_MAJOR_VERSION, 4) {
        DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0
}

INCLUDEPATH += ${SM_STUB_ROOT_PATH}/include
INCLUDEPATH += ${SM_STUB_ROOT_PATH}/../agent/include
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/servicemanager/services/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/servicemanager/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/servicemanager/helpers/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/ccec/include/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/osal/include/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/iarmbus/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/ds/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/ds-rpc/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/ds-hal/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/host/include/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/qt5/QtCore \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtWidgets \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtNetwork \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtGui \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtWebKit \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtWebKitWidgets \
               ${STAGING_DIR_TARGET}/usr/include/qt5/include
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/iarmmgrs/sysmgr

cross_compile:DEFINES+=CROSS_COMPILED_FOR_DEVICE

TEMPLATE = lib
TARGET = servicemanagerstub

packagesExist("gstreamer-1.0"){
LIBS += -lgstpbutils-1.0 -lgstvideo-1.0 -lgstbase-1.0
}

else{
LIBS += -lgstpbutils-0.10 -lgstvideo-0.10 -lgstbase-0.10
}

LIBS += -L"${STAGING_DIR_TARGET}/usr/lib/"
LIBS += -lservicemanager -lds

#non-yocto env variables
exists(../platform/SM_stub/intel.pri) : include(../platform/SM_stub/intel.pri)
exists(../platform/SM_stub/broadcom.pri) : include(../platform/SM_stub/broadcom.pri)

contains(DEFINES,HAS_API_HDMI_CEC) {
HEADERS += servicemanager/include/services/hdmicecservice.h
SOURCES += servicemanager/src/services/hdmicecservice.cpp
LIBS += -lRCEC -lRCECOSHal -lRCECIARMBusHal
}

HEADERS += servicemanager/include/services/applicationservice.h

SOURCES += src/ServiceManagerAgent.cpp \
	   servicemanager/src/services/applicationservice.cpp
