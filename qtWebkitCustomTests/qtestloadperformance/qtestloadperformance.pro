#-------------------------------------------------
#
# Project created by QtCreator 2014-02-06T16:02:05
#
#-------------------------------------------------

QT       += network webkit webkitwidgets testlib
include(../twctests.pri)
TARGET = tst_qtestloadperformance 
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += \
    tst_qtestloadperformance.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"
