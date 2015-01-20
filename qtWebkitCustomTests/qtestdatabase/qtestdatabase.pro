QT       += sql webkit testlib network

QT      += gui

include(../twctests.pri)

TARGET = tst_qtestdatabase
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += \
    tst_qtestdatabase.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestdatabase.qrc


