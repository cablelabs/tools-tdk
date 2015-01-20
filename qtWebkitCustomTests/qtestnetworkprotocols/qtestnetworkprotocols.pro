QT       += network webkit testlib

QT       += gui
include(../twctests.pri)
TARGET = tst_qtestnetworkprotocols
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += tst_qtestnetworkprotocols.cpp
DEFINES += SRCDIR=\\\"$$PWD/\\\"


