QT       += network webkit testlib 
include(../twctests.pri)
TARGET = tst_qtestcssfeatures_set2
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssfeatures_set2.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssfeatures_set2.qrc
