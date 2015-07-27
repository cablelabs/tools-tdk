## Copyright (c) 2013 Comcast. All rights reserved.

ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = ${COPTS} -fPIC -DDEBUG_LEVEL_TRACE

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/power/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/ir \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/mfr \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs-hal/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/sysmgr/ \
           -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/disk/ \
           -I${top_srcdir}/IARMBUS_stub/include -I${top_srcdir}/agent/include


AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmbus/ \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/ir \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/mfr \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs-hal/ \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/power \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/sysmgr/ \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/iarmmgrs/disk/ \
              -I${top_srcdir}/IARMBUS_stub/include -I${top_srcdir}/agent/include


lib_LTLIBRARIES = libiarmbusstub.la
libiarmbusstub_la_SOURCES = src/IARMBUSStub.cpp
libiarmbusstub_la_LIBADD = -lglib-2.0 -lIARMBus -ldirect -lfusion -ldbus-1 -lz
libiarmbusstub_la_includedir = ${includedir}
libiarmbusstub_la_include_HEADERS = ${top_srcdir}/IARMBUS_stub/include/IARMBUSAgent.h

bin_PROGRAMS = tst_iarmbus Test_Event_Mgr gen_single_event gen_multiple_events gen_irevent
tst_iarmbusdir = ${bindir}
tst_iarmbus_SOURCES = src/tst_iarmbus.c
tst_iarmbus_LDADD = -lIARMBus -lz -lglib-2.0
tst_iarmbus_includedir = ${includedir}

Test_Event_Mgrdir = ${bindir}
Test_Event_Mgr_SOURCES = src/Test_Event_Mgr.c
Test_Event_Mgr_LDADD = -lIARMBus -lz -lglib-2.0
Test_Event_Mgr_includedir = ${includedir}

gen_single_eventdir = ${bindir}
gen_single_event_SOURCES = src/gen_single_event.cpp
gen_single_event_LDADD = -lrt -lIARMBus -lz -lglib-2.0
gen_single_event_includedir = ${includedir}

gen_multiple_eventsdir = ${bindir}
gen_multiple_events_SOURCES = src/gen_multiple_events.cpp
gen_multiple_events_LDADD = -lrt -lIARMBus -lz -lglib-2.0
gen_multiple_events_includedir = ${includedir}

gen_ireventdir = ${bindir}
gen_irevent_SOURCES = src/gen_irevent.cpp
gen_irevent_LDADD = -lrt -lIARMBus -lz -lglib-2.0
gen_irevent_includedir = ${includedir}
