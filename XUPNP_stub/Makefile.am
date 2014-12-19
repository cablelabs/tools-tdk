## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = ${COPTS} -std=c++0x -fPIC -DGCC4_XXX -g

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I./include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libxupnpstub.la
libxupnpstub_la_SOURCES = src/xupnpAgent.cpp
libxupnpstub_la_includedir = ${includedir}
libxupnpstub_la_include_HEADERS = ./include/xupnpAgent.h
