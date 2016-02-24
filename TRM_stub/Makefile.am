## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -Wall -g -DGCC4_XXX -Wno-format -Wunused -DUSE_CC_GETTIMEOFDAY \
              -DRDK_BR_2DOT0 ${COPTS} -DDEBUG_CONF_FILE="\"/etc/debug.ini\"" -DNUM_OF_TUNERS=$(MAX_NUM_TUNERS)

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

libtrmstub_la_LIBADD = -ltrm 
libtrmstub_la_includedir = ${includedir}
libtrmstub_la_include_HEADERS = ${top_srcdir}/TRM_stub/include/TRMAgentHelper.h \
                                ${top_srcdir}/TRM_stub/include/TRMAgent.h
