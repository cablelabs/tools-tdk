## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -c -Wall -shared ${COPTS} -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${top_srcdir}/TR069_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libtr069modulestub.la
libtr069modulestub_la_SOURCES = src/TR069Agent.cpp
libtr069modulestub_la_includedir = ${includedir}
libtr069modulestub_la_include_HEADERS = ${top_srcdir}/TR069_stub/include/TR069Agent.h
