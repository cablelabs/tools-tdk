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
DEFINES += HAS_API_AVINPUT USE_AVINPUT USE_DISPLAY_SETTINGS DEBUG_LEVEL_TRACE RDK2DOT0 

greaterThan(QT_MAJOR_VERSION, 4) {
        DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0
}

INCLUDEPATH += ../include
INCLUDEPATH += ../../agent/include
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
               ${STAGING_DIR_TARGET}/usr/include/qt5/include \
	       ${STAGING_DIR_TARGET}/usr/include/directfb
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/iarmmgrs/sysmgr

exists(../servicemanager/platform/broadcom/build/broadcom.pri): INCLUDEPATH += ../servicemanager/platform/broadcom/include/helpers/

cross_compile:DEFINES+=CROSS_COMPILED_FOR_DEVICE

TEMPLATE = app
TARGET = SMEventApp

packagesExist("gstreamer-1.0"){
LIBS += -lgstpbutils-1.0 -lgstvideo-1.0 -lgstbase-1.0
}

else{
LIBS += -lgstpbutils-0.10 -lgstvideo-0.10 -lgstbase-0.10
}

LIBS += -L"${STAGING_DIR_TARGET}/usr/lib/"
LIBS += -lservicemanager -lds -ldshalcli -lIARMBus -ljsoncpp -ljsonrpc-cpp

#non-yocto env variables
exists(../../platform/SM_stub/intel.pri) : include(../../platform/SM_stub/intel.pri)
exists(../../platform/SM_stub/broadcom.pri) : include(../../platform/SM_stub/broadcom.pri)

SOURCES += sm_qapp.cpp 

contains(DEFINES,USE_DISPLAY_SETTINGS) {
HEADERS += ../servicemanager/include/services/displaysettingsservice.h

SOURCES += ../servicemanager/src/services/displaysettingsservice.cpp
}

contains(DEFINES,HAS_API_AVINPUT) {
	HEADERS += ../servicemanager/include/abstractservice.h \
        	   $$(STAGING_DIR_TARGET)/usr/include/rdk/servicemanager/services/avinputservice.h

	SOURCES += ../servicemanager/src/abstractservice.cpp \
                   ../servicemanager/src/services/avinputservice.cpp

	exists(../servicemanager/platform/broadcom/build/broadcom.pri): 
		HEADERS += ../servicemanager/platform/broadcom/include/helpers/avinputhelper.h \
                           ../servicemanager/platform/broadcom/include/helpers/avinput.h
		SOURCES += ../servicemanager/platform/broadcom/src/helpers/avinputhelper.cpp
}
