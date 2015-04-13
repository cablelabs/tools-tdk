ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -DRDK_BR_2DOT0 ${COPTS} -std=c++0x -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I${top_srcdir}/OpenSourceComponent_Stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libopensourcetestsuitestub.la
libopensourcetestsuitestub_la_SOURCES = src/opensrcteststub.cpp
#libopensourcetestsuitestub_la_LIBADD =
libopensourcetestsuitestub_la_includedir = ${includedir}
libopensourcetestsuitestub_la_include_HEADERS = ${top_srcdir}/OpenSourceComponent_Stub/include/opensrcteststub.h
