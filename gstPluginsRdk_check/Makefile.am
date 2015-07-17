## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CFLAGS = -Wall -fPIC ${COPTS} $(GST_CFLAGS) $(GST_CHECK_CFLAGS) \
            -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
            -I${top_srcdir}/gstPluginsRdk_check/include -I${top_srcdir}/agent/include

bin_PROGRAMS = gstpluginsrdkcheck
gstpluginsrdkcheck_SOURCES = src/gst_plugins_rdk.c
gstpluginsrdkcheck_LDADD = $(GST_LIBS) $(GST_CHECK_LIBS) -ldl -lpthread
