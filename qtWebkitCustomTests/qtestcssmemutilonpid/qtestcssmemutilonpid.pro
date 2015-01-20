QT       += network webkit testlib
include(../twctests.pri)
TARGET = tst_qtestcssmemutilonpid
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssmemutilonpid.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssmemutilonpid.qrc
