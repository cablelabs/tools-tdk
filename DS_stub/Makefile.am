## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -DQT_WEBKIT_LIB ${COPTS} -std=c++0x -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/ds \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/ds-hal \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/ds-rpc \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/ir \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs-hal/ \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/mfr \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/power \
              -I${top_srcdir}/DS_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libdevicesettingsstub.la
libdevicesettingsstub_la_SOURCES = src/DeviceSettingsAgent.cpp
libdevicesettingsstub_la_LIBADD = -ldshalcli -lds -lrdkloggers -lglib-2.0 -llog4c -lIARMBus -ldirect -lfusion -ldbus-1
libdevicesettingsstub_la_includedir = ${includedir}
libdevicesettingsstub_la_include_HEADERS = ./include/DeviceSettingsAgent.h
