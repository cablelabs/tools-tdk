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

AM_CPPFLAGS = -Wall -DGCC4_XXX -fPIC $(COPTS)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/directfb \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${top_srcdir}/ClosedCaption_stub/include -I${top_srcdir}/agent/include
lib_LTLIBRARIES = libccstub.la
libccstub_la_SOURCES = src/CCStub.cpp
libccstub_la_LIBADD = -lrdkloggers -lrdkCCGfx -lrdkCCManager -ldirectfb -lcurl -llog4c -lz -lrdkCCReader
libccstub_la_includedir = ${includedir}
