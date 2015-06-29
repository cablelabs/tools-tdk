## Copyright (c) 2013 Comcast. All rights reserved.

AM_CXXFLAGS = -DUSE_DEVICE_SETTINGS_SERVICE -DSCREEN_CAPTURE $(SM_STUB_CFLAG_HYBRID) $(GST_CFLAGS) ${COPTS} \
           -fPIC -I${top_srcdir}/include -I${top_srcdir}/../agent/include \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager/helpers \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager/services \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5 \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtWidgets \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtCore \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtGui \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtNetwork/ \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtWebKitWidgets

lib_LTLIBRARIES = libservicemanagerstub.la
libservicemanagerstub_la_SOURCES = src/ServiceManagerAgent.cpp
libservicemanagerstub_la_LIBADD = -lservicemanager $(GST_LIBS) -ludev -lgstpbutils-0.10 -lgstvideo-0.10 -lgstbase-0.10 -lgthread-2.0 -lglib-2.0 -lQt5Sql -lQt5OpenGL -lQt5Widgets -lQt5Network -lQt5Gui -lQt5Core -lz -lssl -lcrypto -ljpeg -licui18n -licuuc -licudata
libservicemanagerstub_la_includedir = ${includedir}
