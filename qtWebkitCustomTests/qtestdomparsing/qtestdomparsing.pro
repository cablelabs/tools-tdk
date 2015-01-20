QT       += network webkit testlib
include(../twctests.pri)
#QT       -= gui

TARGET = tst_qtestdomparsing
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += \
    tst_qtestdomparsing.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"
