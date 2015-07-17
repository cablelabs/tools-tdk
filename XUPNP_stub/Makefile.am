## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = ${COPTS} -std=c++0x -fPIC -DGCC4_XXX -g

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/sysmgr/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/directfb/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/core/include \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/core \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/generic/ir/include \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/generic/sysmgr/include \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/xupnp/generic/include

AM_CXXFLAGS = -I${top_srcdir}/XUPNP_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libxupnpstub.la
libxupnpstub_la_SOURCES = src/xupnpAgent.cpp
libxupnpstub_la_includedir = ${includedir}
libxupnpstub_la_include_HEADERS = ${top_srcdir}/XUPNP_stub/include/xupnpAgent.h
