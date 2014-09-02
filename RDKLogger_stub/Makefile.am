## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -g -Wall -std=c++0x -DGCC4_XXX \
	      -DDEBUG_CONF_FILE="\"$(CONFIG_PREFIX)debug.ini\"" \
	      -fPIC ${COPTS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I./include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = librdkloggerstub.la
librdkloggerstub_la_SOURCES = src/RDKLoggerAgent.cpp
librdkloggerstub_la_LIBADD = -lrdkloggers
librdkloggerstub_la_includedir = ${includedir}
librdkloggerstub_la_include_HEADERS = ./include/RDKLoggerAgent.h
