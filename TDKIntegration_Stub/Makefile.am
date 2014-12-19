## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -Wall -fPIC ${COPTS} -DGCC4_XXX -DRMFAGENT -DRMF_OSAL_LITTLE_ENDIAN ${TDKINTEGRATION_FLAGS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I./include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libtdkintegrationstub.la
libtdkintegrationstub_la_SOURCES = src/TDKIntegrationStub.cpp
libtdkintegrationstub_la_LIBADD = -lrdkloggers -lmediaplayersink -lhnsource -lrmfbase ${TDKINTEGRATION_HYBRID_LIBS}
libtdkintegrationstub_la_includedir = ${includedir}
libtdkintegrationstub_la_include_HEADERS = ./include/TDKIntegrationStub.h
