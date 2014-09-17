## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -Wall -DGCC4_XXX -fPIC $(COPTS)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/directfb \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I./include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libccstub.la
libccstub_la_SOURCES = src/CCStub.cpp
libccstub_la_LIBADD = -lrdkloggers
libccstub_la_includedir = ${includedir}
libccstub_la_include_HEADERS = ./include/CCAgent.h
