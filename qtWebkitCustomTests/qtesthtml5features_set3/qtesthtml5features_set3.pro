QT       += network webkit webkitwidgets testlib
include(../twctests.pri)

TARGET = tst_qtesthtml5features_set3
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app

SOURCES += \
    tst_qtesthtml5features_set3.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"
DEFINES += SERVER_PATH=\\\"$$PUBLISHER_IP_PATH/\\\"
