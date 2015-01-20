QT       += network testlib webkit

include(../twctests.pri)

TARGET = tst_qtestcssbasicfeatures
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestcssbasicfeatures.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"

RESOURCES += \
    tst_qtestcssbasicfeatures.qrc
