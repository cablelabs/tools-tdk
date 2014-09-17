## Copyright (c) 2013 Comcast. All rights reserved.

AM_CXXFLAGS = -DQT_WEBKIT_LIB $(GST_CFLAGS) ${COPTS} -fPIC -I./include -I${top_srcdir}/agent/include \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager/helpers \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager/services \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5 \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtWidgets \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtCore \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtGui \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtWebKitWidgets

lib_LTLIBRARIES = libservicemanagerstub.la
libservicemanagerstub_la_SOURCES = src/ServiceManagerAgent.cpp
libservicemanagerstub_la_LIBADD = -lservicemanager $(GST_LIBS)
libservicemanagerstub_la_includedir = ${includedir}
libservicemanagerstub_la_include_HEADERS = ./include/ServiceManagerAgent.h
