## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -Wall -fPIC ${COPTS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I./include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libtdkintegrationstub.la
libtdkintegrationstub_la_SOURCES = src/TDKIntegrationStub.cpp
libtdkintegrationstub_la_LIBADD = -lrdkloggers
libtdkintegrationstub_la_includedir = ${includedir}
libtdkintegrationstub_la_include_HEADERS = ./include/TDKIntegrationStub.h
