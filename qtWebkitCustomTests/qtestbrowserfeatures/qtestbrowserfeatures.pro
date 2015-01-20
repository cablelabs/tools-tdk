QT       += network testlib webkit
include(../twctests.pri)
QT       += gui

TARGET = tst_qtestbrowserfeatures
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestbrowserfeatures.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"


