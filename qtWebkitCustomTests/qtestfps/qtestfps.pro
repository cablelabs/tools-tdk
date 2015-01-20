QT       += webkit testlib gui network
include(../twctests.pri)
TARGET = tst_qtestfps
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += \
    tst_qtestfps.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestfps.qrc

OTHER_FILES += \
    resources/SVGSource.html \
    resources/test.html \
    resources/charDefs.js \
    resources/engine.js \
    resources/canvas.html
