## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -Wall -g -DGCC4_XXX -Wno-format -Wunused -DUSE_CC_GETTIMEOFDAY -DRMF_OSAL_FEATURE_IPV6 -DRMF_OSAL_LITTLE_ENDIAN \
              -DRDK_BR_2DOT0 ${COPTS} -DDEBUG_CONF_FILE="\"/etc/debug.ini\""


AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/trm \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0 \
              -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include \
              -I${top_srcdir}/TRM_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libtrmstub.la
libtrmstub_la_SOURCES = src/TRMAgent.cpp \
                        src/TRMAgentHelper.cpp

libtrmstub_la_LIBADD = -lrmfosal -lrmfosalutils -ltrm -lpthread -lrdkloggers -ljansson -llog4c
libtrmstub_la_includedir = ${includedir}
libtrmstub_la_include_HEADERS = ${top_srcdir}/TRM_stub/include/TRMAgentHelper.h \
                                ${top_srcdir}/TRM_stub/include/TRMAgent.h
