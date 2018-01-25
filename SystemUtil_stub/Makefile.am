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

AM_CPPFLAGS = -c ${COPTS} -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${top_srcdir}/SystemUtil_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libsystemutilstub.la
libsystemutilstub_la_SOURCES = src/SystemUtil_stub.cpp
libsystemutilstub_la_includedir = ${includedir}
libsystemutilstub_la_include_HEADERS = ${top_srcdir}/SystemUtil_stub/include/SystemUtil_stub.h

