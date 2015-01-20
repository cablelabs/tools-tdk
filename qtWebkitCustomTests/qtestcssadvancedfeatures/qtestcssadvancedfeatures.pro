QT       +=network webkit testlib
include(../twctests.pri)
TARGET = tst_qtestcssadvancedfeatures
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssadvancedfeatures.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssadvancedfeatures.qrc
