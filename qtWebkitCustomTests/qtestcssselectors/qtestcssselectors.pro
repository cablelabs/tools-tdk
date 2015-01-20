QT       += network testlib webkit
include(../twctests.pri)
QT       += gui

TARGET = tst_qtestcssselectors
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssselectors.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssselectors.qrc
