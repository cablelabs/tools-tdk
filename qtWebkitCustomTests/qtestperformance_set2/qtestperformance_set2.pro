QT       += network webkit testlib webkitwidgets
include(../twctests.pri)
TARGET = tst_qtestperformance_set2
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestperformance_set2.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"
DEFINES += SERVER_PATH=\\\"$$PUBLISHER_IP_PATH/\\\"
