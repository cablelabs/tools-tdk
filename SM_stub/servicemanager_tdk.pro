
QT += webkitwidgets webkit widgets network core gui
DEFINES += HAS_API_HDMI_CEC QT_WEBKIT_LIB USE_DEVICE_SETTINGS_SERVICE SCREEN_CAPTURE DEBUG_LEVEL_TRACE RDK2DOT0

INCLUDEPATH += ${SM_STUB_ROOT_PATH}/include
INCLUDEPATH += ${SM_STUB_ROOT_PATH}/../agent/include
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/servicemanager/services/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/servicemanager/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/servicemanager/helpers/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/ccec/include/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/osal/include/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/iarmbus/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/rdk/ds/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/host/include/
INCLUDEPATH += ${STAGING_DIR_TARGET}/usr/include/qt5/QtCore \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtWidgets \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtNetwork \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtGui \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtWebKit \
               ${STAGING_DIR_TARGET}/usr/include/qt5/QtWebKitWidgets \
               ${STAGING_DIR_TARGET}/usr/include/qt5/include

cross_compile:DEFINES+=CROSS_COMPILED_FOR_DEVICE

TEMPLATE = lib
TARGET = servicemanagerstub

LIBS += -L"${STAGING_DIR_TARGET}/usr/lib/"
LIBS += -lservicemanager -lRCEC -lRCECOSHal -lRCECHal -lQt5WebKitWidgets -ludev -lgstpbutils-0.10 -lgstvideo-0.10 -lgstbase-0.10 -lgthread-2.0 -lglib-2.0 -lQt5Sql -lQt5OpenGL -lQt5WebKit -lQt5Widgets -lQt5Network -lQt5Gui -lQt5Core -lz -lssl -lcrypto -ljpeg -licui18n -licuuc -licudata

HEADERS += $$(STAGING_DIR_TARGET)/usr/include/rdk/servicemanager/services/hdmicecservice.h \

SOURCES += src/ServiceManagerAgent.cpp \
           servicemanager/src/services/hdmicecservice.cpp       \
