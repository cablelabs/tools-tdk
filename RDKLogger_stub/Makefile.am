## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -g -Wall -std=c++0x -DGCC4_XXX \
	      -DDEBUG_CONF_FILE="\"$(CONFIG_PREFIX)debug.ini\"" \
	      -fPIC ${COPTS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${top_srcdir}/RDKLogger_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = librdkloggerstub.la
librdkloggerstub_la_SOURCES = src/RDKLoggerAgent.cpp
librdkloggerstub_la_LIBADD = -lrdkloggers
librdkloggerstub_la_includedir = ${includedir}
librdkloggerstub_la_include_HEADERS = ${top_srcdir}/RDKLogger_stub/include/RDKLoggerAgent.h
