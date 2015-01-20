QT       += network webkit testlib
include(../twctests.pri)

TARGET = tst_qtestbasichtml
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app
PKGCONFIG += fontconfig

SOURCES += \
    tst_qtestbasichtml.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"


RESOURCES += \
    tst_qtestbasichtml.qrc
