QT       += network webkit testlib

QT       += gui
include(../twctests.pri)
TARGET = tst_qtestcssperformance
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssperformance.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssperformance.qrc
