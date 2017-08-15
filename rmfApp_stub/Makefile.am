# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -DRDK_BR_2DOT0 ${COPTS} -std=c++0x -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${top_srcdir}/rmfApp_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = librmfappstub.la
librmfappstub_la_SOURCES = src/rmfappteststub.cpp
librmfappstub_la_includedir = ${includedir}
librmfappstub_la_include_HEADERS = ${top_srcdir}/rmfApp_stub/include/rmfAppteststub.h
