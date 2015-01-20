QT       += network webkit testlib
include(../twctests.pri)
#QT       -= gui

TARGET = tst_qtestcssfeatures
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += \
    tst_qtestcssfeatures.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"


RESOURCES += \
    tst_qtestcssfeatures.qrc
