ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -DRDK_BR_2DOT0 ${COPTS} -std=c++0x -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I./include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = librmfappstub.la
librmfappstub_la_SOURCES = src/rmfappteststub.cpp
librmfappstub_la_includedir = ${includedir}
librmfappstub_la_include_HEADERS = ./include/rmfAppteststub.h
