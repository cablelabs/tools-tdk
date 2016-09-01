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
DEFINES += DEBUG_LEVEL_TRACE RDK2DOT0
DEFINES += HAS_API_HDMI_CEC USE_DEVICE_SETTINGS_SERVICE SCREEN_CAPTURE ENABLE_WEBSOCKET_SERVICE HAS_API_APPLICATION
DEFINES += HAS_API_AVINPUT USE_AVINPUT
DEFINES += QT_WEBKIT_LIB

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
exists($(SM_STUB_ROOT_PATH)/servicemanager/platform/broadcom/build/broadcom.pri): INCLUDEPATH += ${SM_STUB_ROOT_PATH}/servicemanager/platform/broadcom/include/helpers/

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
exists(../../platform/SM_stub/intel.pri) : include(../../platform/SM_stub/intel.pri)
exists(../../platform/SM_stub/broadcom.pri) : include(../../platform/SM_stub/broadcom.pri)

SOURCES += ServiceManagerAgent.cpp

contains(DEFINES,HAS_API_HDMI_CEC) {
HEADERS += ../servicemanager/include/services/hdmicecservice.h
SOURCES += ../servicemanager/src/services/hdmicecservice.cpp
LIBS += -lRCEC -lRCECOSHal -lRCECIARMBusHal
}

contains(DEFINES,HAS_API_APPLICATION) {
HEADERS += ../servicemanager/include/services/applicationservice.h
SOURCES += ../servicemanager/src/services/applicationservice.cpp \
}

contains(DEFINES,USE_DISPLAY_SETTINGS) {
HEADERS += ../servicemanager/include/services/displaysettingsservice.h
SOURCES += ../servicemanager/src/services/displaysettingsservice.cpp
}

contains(DEFINES,HAS_API_AVINPUT) {
HEADERS += ../servicemanager/include/abstractservice.h \
           $$(STAGING_DIR_TARGET)/usr/include/rdk/servicemanager/services/avinputservice.h

exists($(SM_STUB_ROOT_PATH)/servicemanager/platform/broadcom/build/broadcom.pri): HEADERS += \
                        ${SM_STUB_ROOT_PATH}/servicemanager/platform/broadcom/include/helpers/avinputhelper.h \
                        ${SM_STUB_ROOT_PATH}/servicemanager/platform/broadcom/include/helpers/avinput.h

SOURCES += ../servicemanager/src/abstractservice.cpp \
           ../servicemanager/src/services/avinputservice.cpp
exists($(SM_STUB_ROOT_PATH)/servicemanager/platform/broadcom/build/broadcom.pri): SOURCES += $$(SM_STUB_ROOT_PATH)/servicemanager/platform/broadcom/src/helpers/avinputhelper.cpp
}
