## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -g -Wall -DGCC4_XXX -DBUILD_DVRSOURCE -DRMF_STREAMER -DENABLE_DVRSRC_MPSINK -fPIC -DRMF_OSAL_LITTLE_ENDIAN

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/trm \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0 \
              -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include \
              -I${PKG_CONFIG_SYSROOT_DIR}/$(includedir)/rdk/iarmmgrs-hal \
              -I${top_srcdir}/tdkRmfApp/include -I${top_srcdir}/agent/include

bin_PROGRAMS = tdkRmfApp
tdkRmfAppdir = ${bindir}
tdkRmfApp_SOURCES = tdkRmfApp.cpp
tdkRmfApp_LDFLAGS = -ldvrmgr -ltinyxml -luuid -lcrypto -lTasseograph -lssl -lreadline -lnetsnmp -lnetsnmpagent -lnetsnmphelpers \
-lssl -lhistory -lgstreamer-0.10 -lgio-2.0 -lglib-2.0 -llog4c -lgobject-2.0 -linit -lrdkloggers -lrmfbase -lncurses -ldvrmgrsoc \
-lgstbase-0.10 -lhnsource -lrmfosal -lrmfosalutils -ltrm -ljansson -ldvrsink -lmediaplayersink -lIARMBus
tdkRmfApp_includedir = ${includedir}
