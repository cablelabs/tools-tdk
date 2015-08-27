## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -Wall -fPIC ${COPTS} -DGCC4_XXX -DRMFAGENT -DRMF_OSAL_LITTLE_ENDIAN ${TDKINTEGRATION_FLAGS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${top_srcdir}/TDKIntegration_Stub/include \
	      -I${top_srcdir}/agent/include ${TDKINTEGRATION_INCLUDE_PATH} \
              -I${TDKINTEGRATION_INCLUDE_PATH}

lib_LTLIBRARIES = libtdkintegrationstub.la
libtdkintegrationstub_la_SOURCES = src/TDKIntegrationStub.cpp
libtdkintegrationstub_la_LIBADD = -lrdkloggers -lmediaplayersink -lhnsource -lrmfbase ${TDKINTEGRATION_HYBRID_LIBS} -lrmfinit -lglib-2.0  -lrmfosalutils -lrmfosal -lrdkloggers -llog4c
libtdkintegrationstub_la_includedir = ${includedir}

