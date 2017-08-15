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

AM_CPPFLAGS = -Wall -fPIC ${COPTS} -DGCC4_XXX -DRMFAGENT -DRMF_OSAL_LITTLE_ENDIAN ${TDKINTEGRATION_FLAGS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${top_srcdir}/TDKIntegration_Stub/include \
	      -I${top_srcdir}/agent/include ${TDKINTEGRATION_INCLUDE_PATH} \
              -I${TDKINTEGRATION_INCLUDE_PATH}

lib_LTLIBRARIES = libtdkintegrationstub.la
libtdkintegrationstub_la_SOURCES = src/TDKIntegrationStub.cpp
libtdkintegrationstub_la_LIBADD = -lmediaplayersink -lhnsource
libtdkintegrationstub_la_includedir = ${includedir}

