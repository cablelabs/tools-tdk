QT       += widgets network webkit webkitwidgets testlib
include(../twctests.pri)

TARGET = tst_qtestcssfeatures_set4
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssfeatures_set4.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssfeatures_set4.qrc