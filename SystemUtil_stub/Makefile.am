ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -c ${COPTS} -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${top_srcdir}/SystemUtil_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libsystemutilstub.la
libsystemutilstub_la_SOURCES = src/SystemUtil_stub.cpp
libsystemutilstub_la_includedir = ${includedir}
libsystemutilstub_la_include_HEADERS = ${top_srcdir}/SystemUtil_stub/include/SystemUtil_stub.h

