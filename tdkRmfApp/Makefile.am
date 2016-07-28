## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -g -Wall -DGCC4_XXX -fPIC -DRMF_OSAL_LITTLE_ENDIAN ${SOC_FLAGS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0 \
              -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include \
              -I${top_srcdir}/agent/include

bin_PROGRAMS = tdkRmfApp
tdkRmfAppdir = ${bindir}
tdkRmfApp_SOURCES = tdkRmfApp.cpp
tdkRmfApp_LDFLAGS = -ldvrmgr -ldvrsink -lmediaplayersink -lhnsource -luuid ${SOC_LIBS} $(TDK_GST_LIBS)
tdkRmfApp_includedir = ${includedir}
