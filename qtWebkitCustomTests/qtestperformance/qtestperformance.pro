QT       += network webkit testlib webkitwidgets
QT       += gui

include(../twctests.pri)
TARGET = tst_qtestperformance
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app

SOURCES += tst_qtestperformance.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"
DEFINES += SERVER_PATH=\\\"$$PUBLISHER_IP_PATH/\\\"
