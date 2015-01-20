#-------------------------------------------------
#
# Project created by QtCreator 2014-04-14T12:02:24
#
#-------------------------------------------------

QT       += widgets network webkit webkitwidgets testlib
include(../twctests.pri)

TARGET = tst_testhtml5features_set5
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += \
    tst_qtesthtml5features_set5.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"
DEFINES += SERVER_PATH=\\\"$$PUBLISHER_IP_PATH/\\\"

RESOURCES += \
    tst_qtesthtml5features_set5.qrc
