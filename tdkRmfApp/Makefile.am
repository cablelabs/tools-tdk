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

AM_CPPFLAGS = -g -Wall -DGCC4_XXX -fPIC -DRMF_OSAL_LITTLE_ENDIAN -DUSE_RBI ${SOC_FLAGS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0 \
              -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include \
              -I${top_srcdir}/agent/include

bin_PROGRAMS = tdkRmfApp
tdkRmfAppdir = ${bindir}
tdkRmfApp_SOURCES = tdkRmfApp.cpp
tdkRmfApp_LDFLAGS = -ldvrmgr -ldvrsink -lmediaplayersink -lhnsource -luuid -lsharedtsb -lrbifilter -lrbi ${SOC_LIBS} $(TDK_GST_LIBS)
tdkRmfApp_includedir = ${includedir}
