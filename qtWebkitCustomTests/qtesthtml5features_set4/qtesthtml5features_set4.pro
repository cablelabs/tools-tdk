QT       += network webkit testlib webkitwidgets
include(../twctests.pri)

TARGET = tst_qtesthtml5features_set4
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app

SOURCES += \
    tst_qtesthtml5features_set4.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"
DEFINES += SERVER_PATH=\\\"$$PUBLISHER_IP_PATH/\\\"

RESOURCES += \
    tst_qtesthtml5features_set4.qrc
