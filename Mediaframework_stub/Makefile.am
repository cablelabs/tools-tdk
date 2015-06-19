## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -DQT_WEBKIT_LIB ${COPTS} -std=c++0x -fPIC -DGCC4_XXX -DBUILD_DVRSOURCE -DRMF_STREAMER -DENABLE_DVRSRC_MPSINK -DRMF_OSAL_LITTLE_ENDIAN

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/core/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/gstreamer \
          \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/gstreamer-0.10/gst/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0/ \
          -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include/ \
          \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/glib/glib/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/glib/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/gstreamer/gstreamer-0.10.34/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/libxml2/include/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/glib/gmodule \
            \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/osal/utils/inc/ \
            \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/hnsource/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/hnsink/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/dvr/source/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/dvr/common/tasseograph/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/dvr/common/dvrmgr/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdklogger/include/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/dvr/sink/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/qamsource/main/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/init/ \
            \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I${top_srcdir}/Mediaframework_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libmediaframeworkstub.la
libmediaframeworkstub_la_SOURCES = src/MediaframeworkAgent.cpp
libmediaframeworkstub_la_LIBADD = -lglib-2.0 -llog4c -ldvrmgr -ltinyxml -luuid -lcrypto -lTasseograph -lssl -lreadline -lnetsnmp -lnetsnmpagent -lnetsnmphelpers -lsectionfilter -linbsimanager -linbsectionfilter -lhistory -lgstreamer-0.10 -lgio-2.0 -lgobject-2.0 -lrmfinit -lrdkloggers -lqamsrc -lncurses -ldvrmgrsoc -lgstbase-0.10 -lhnsource -ldvrsink -lhnsink -ltrh -ltrm -lIARMBus -lDtcpMgr -lrmfbase -ljansson -lmediaplayersink -ldvrsource
libmediaframeworkstub_la_includedir = ${includedir}
libmediaframeworkstub_la_include_HEADERS = ${top_srcdir}/Mediaframework_stub/include/MediaframeworkAgent.h

