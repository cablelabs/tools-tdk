QT       += network webkit testlib
include(../twctests.pri)
TARGET = tst_qtestcss3features
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcss3features.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcss3features.qrc
