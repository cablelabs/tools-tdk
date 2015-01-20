QT       += network webkit testlib
include(../twctests.pri)
TARGET = tst_qtestcssgenericfeatures
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssgenericfeatures.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssgenericfeatures.qrc
