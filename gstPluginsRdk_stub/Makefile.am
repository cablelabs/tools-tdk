## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -Wall -fPIC ${COPTS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I./include $(GLIB_CFLAGS) -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libgstpluginsrdkstub.la
libgstpluginsrdkstub_la_SOURCES = src/gstPluginsRdkAgent.cpp
libgstpluginsrdkstub_la_LIBADD = $(GLIB_LIBS)
libgstpluginsrdkstub_la_includedir = $(includedir)
libgstpluginsrdkstub_la_include_HEADERS = ./include/gstPluginsRdkAgent.h
