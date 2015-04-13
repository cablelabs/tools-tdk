ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = -c ${COPTS} -fPIC

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I${top_srcdir}/Recorder_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libRecorderstub.la
libRecorderstub_la_SOURCES = src/Recorderstub.cpp
libRecorderstub_la_includedir = ${includedir}
libRecorderstub_la_include_HEADERS = ${top_srcdir}/Recorder_stub/include/RecorderStub.h

