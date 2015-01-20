QT       += network webkit testlib

QT       += gui
include(../twctests.pri)
TARGET = tst_qtestcssvisualeffects
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssvisualeffects.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssvisualeffects.qrc
