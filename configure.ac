##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
dnl                                               -*- Autoconf -*-
dnl Process this file with autoconf to produce a configure script.

dnl AC_PREREQ([2.69])
AC_INIT(tdk, 1.0, praveensnair@tataelxsi.co.in,tdk)
AC_CONFIG_SRCDIR([agent/src/agentmain.cpp])
AM_CONFIG_HEADER(cfg/config.h)
AC_CONFIG_MACRO_DIR([cfg])
AC_CONFIG_AUX_DIR([cfg])
AM_INIT_AUTOMAKE([foreign no-dist-gzip dist-bzip2 subdir-objects 1.9])
LT_INIT

dnl subdirectories.

dnl Checks for programs.
AC_PROG_CXX
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_CPP
AC_PROG_CXXCPP

dnl use pretty build output with automake >= 1.11
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])],
  [AM_DEFAULT_VERBOSITY=1
   AC_SUBST(AM_DEFAULT_VERBOSITY)])


dnl **********************************
dnl checks for dependencies
dnl **********************************
AC_HEADER_STDC

dnl Checks for header files.
AC_CHECK_HEADERS([limits.h memory.h stdlib.h string.h sys/socket.h unistd.h])

dnl Checks for typedefs, structures, and compiler characteristics.
dnl AC_CHECK_HEADER_STDBOOL
AC_TYPE_UINT8_T

dnl Checks for library functions.
AC_FUNC_MALLOC
AC_CHECK_FUNCS([memset strdup strerror])

COPTS="-DDEBUG_LEVEL_TRACE"
AM_CXXFLAGS="$AM_CXXFLAGS -DDEBUG_LEVEL_TRACE"
AGENT_FLAGS=" "
CONFIG_PREFIX="/etc/"
DVRMGR_FLAGS=" "
RDK_VERSION="RDK2DOT0"
TDKINTEGRATION_FLAGS=" "
TDKINTEGRATION_HYBRID_LIBS=" "
QAM_LIBS=" "
SF_LIBS=" "
TDK_GST_LIBS=" "
HEADLESS=" "
SUBDIR_HYBRID=" "
SUBDIR_CLIENT=" "
SM_STUB_CFLAG_HYBRID=" "

dnl GStreamer version. Use 0.10 by default
AC_ARG_ENABLE(gstreamer1,
    AS_HELP_STRING([--enable-gstreamer1],
                    [Use GStreamer 1.x]), ,
        [enable_gstreamer1=auto])

AS_IF([test "x$enable_gstreamer1" = "xyes"], [
    GST_MAJORMINOR=1.0
    PKG_CHECK_MODULES([GST], [gstreamer-1.0 >= 1.4], have_gst1="yes", have_gst1="no")
    PKG_CHECK_MODULES([GST_CHECK], [gstreamer-check-1.0 >= 1.4], have_gst1="yes", have_gst1="no")
    PKG_CHECK_MODULES([GLIB], [glib-2.0 >= 2.38.2])
    AC_DEFINE(USE_GST1, 1, [Build with GStreamer 1.x])
], [])

AS_IF([test "x$enable_gstreamer1" = "xyes" -a "x$have_gst1" != "xyes"], [
    AC_MSG_ERROR([Could not find GStreamer 1.x dependencies:
$GST_PKG_ERRORS])], [])

AS_IF([test "x$have_gst1" != "xyes"], [
    GST_MAJORMINOR=0.10
    PKG_CHECK_MODULES([GST], [gstreamer-0.10 >= 0.10.28])
    PKG_CHECK_MODULES([GST_CHECK], [gstreamer-check-0.10 >= 0.10.28])
    PKG_CHECK_MODULES([GLIB], [glib-2.0 >= 2.22.5])
], [])


AC_ARG_ENABLE([hybrid],
        AS_HELP_STRING([--enable-hybrid],[enable hybrid build]),
        [
          case "${enableval}" in
             yes) HYBRID=true
                  SUBDIR_HYBRID="TRM_stub Mediaframework_stub MediaStreamer_stub tdkRmfApp rmfApp_stub DTCP_stub"
                  AGENT_FLAGS=" -DPORT_FORWARD"
                  TDK_GST_LIBS=" -lgstreamer-$GST_MAJORMINOR -lgstbase-$GST_MAJORMINOR"
                  TDKINTEGRATION_HYBRID_LIBS="-ldvrmgr -lqamsrc"
                  TDKINTEGRATION_FLAGS="-DENABLE_HYBRID_CODECOMPILE -DHYBRID" ;;
           no) HYBRID=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-hybrid ]) ;;
           esac
           ],
         [echo "hybrid build is enable"])
AM_CONDITIONAL([HYBRID], [test x$HYBRID = xtrue])

AC_ARG_ENABLE([client],
        AS_HELP_STRING([--enable-client],[enable client build]),
        [
          case "${enableval}" in
             yes) CLIENT=true
                  SUBDIR_CLIENT="TR069_stub NetSrvMgr_stub"
                  TDKINTEGRATION_FLAGS="-DIPCLIENT" ;;
           no) CLIENT=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-client ]) ;;
           esac
           ],
         [echo "client build is enable"])
AM_CONDITIONAL([CLIENT], [test x$CLIENT = xtrue])

AC_ARG_ENABLE([aspcomponents],
         AS_HELP_STRING([--enable-aspcomponents],[enable aspcomponents (default is no)]),
         [
           case "${enableval}" in
              yes) ASPCOMPONENTS=true
                   AS_IF([test x$HYBRID = xtrue], [SUBDIR_HYBRID+=" advancecomponents/Recorder_stub"],
                          [test x$CLIENT = xtrue], [SUBDIR_CLIENT+=" advancecomponents/gstPluginsRdk_check advancecomponents/gstPluginsRdk_stub"],
                          [echo box type not specified]) ;;
             no) ASPCOMPONENTS=false ;;
            *) AC_MSG_ERROR([bad value ${enableval} for --enable-aspcomponents ]) ;;
             esac
            ],
           [echo "advanced components build is not enabled"])
AM_CONDITIONAL([ASPCOMPONENTS], [test x$ASPCOMPONENTS = xtrue])

AC_ARG_ENABLE([quemux86mc],
        AS_HELP_STRING([--enable-qemux86mc],[enable quemux86mc build]),
        [
          case "${enableval}" in
             yes) QEMUX86MC=true
                  SUBDIR_CLIENT="TR069_stub"
                  TDKINTEGRATION_FLAGS="-DIPCLIENT -DSTAND_ALONE_CLIENT" ;;
           no) QEMUX86MC=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-client ]) ;;
           esac
           ],
         [echo "client build is enable"])
AM_CONDITIONAL([QEMUX86MC], [test x$QEMUX86MC = xtrue])

AC_ARG_ENABLE([trace],
              AS_HELP_STRING([--enable-trace],[enable trace (default is no)]),
              [
                      case "${enableval}" in
                 yes) COPTS="$COPTS -DDEBUG_LEVEL_TRACE"
                      echo "DEBUG_LOG_LEVEL : TRACE";;
                 no)  AC_MSG_ERROR([trace is disabled]) ;;
                 *) AC_MSG_ERROR([bad value ${enableval} for --enable-trace]) ;;
                       esac
                  ],
                  )

AC_ARG_ENABLE([log],
              AS_HELP_STRING([--enable-log],[enable log (default is no)]),
              [
                      case "${enableval}" in
                 yes) COPTS="$COPTS -DDEBUG_LEVEL_LOG"
                      echo "DEBUG_LOG_LEVEL : LOG";;
                 no)  AC_MSG_ERROR([log is disabled]) ;;
                 *) AC_MSG_ERROR([bad value ${enableval} for --enable-log]) ;;
                       esac
                  ],
                  )

AC_ARG_ENABLE([errorlog],
              AS_HELP_STRING([--enable-errorlog],[enable errorlog (default is no)]),
              [
                      case "${enableval}" in
                 yes) COPTS="$COPTS -DDEBUG_LEVEL_ERROR"
                      echo "DEBUG_LOG_LEVEL : ERROR";;
                 no)  AC_MSG_ERROR([errorlog is disabled]) ;;
                 *) AC_MSG_ERROR([bad value ${enableval} for --enable-errorlog]) ;;
                       esac
                  ],
                  )

PKG_CHECK_MODULES([XML2], [libxml-2.0 >= 2.7.8])
PKG_CHECK_MODULES([JANSON],[jansson >= 2.4])

m4_syscmd([test -d advancecomponents/Recorder_stub/])
m4_if(m4_sysval,[0],[AC_CONFIG_FILES([advancecomponents/Recorder_stub/Makefile])])


m4_syscmd([test -d advancecomponents/gstPluginsRdk_check/])
m4_if(m4_sysval,[0],[AC_CONFIG_FILES([advancecomponents/gstPluginsRdk_check/Makefile])])
m4_if(m4_sysval,[0],[AC_CONFIG_FILES([advancecomponents/gstPluginsRdk_stub/Makefile])])

AC_SUBST(COPTS)
AC_SUBST(AGENT_FLAGS)
AC_SUBST(DVRMGR_FLAGS)
AC_SUBST(CONFIG_PREFIX)
AC_SUBST(RDK_VERSION)
AC_SUBST(TDKINTEGRATION_FLAGS)
AC_SUBST(TDKINTEGRATION_HYBRID_LIBS)
AC_SUBST(QAM_LIBS)
AC_SUBST(SF_LIBS)
AC_SUBST(TDK_GST_LIBS)
AC_SUBST(SUBDIR_HYBRID)
AC_SUBST(SUBDIR_CLIENT)
AC_SUBST(SM_STUB_CFLAG_HYBRID)
AC_CONFIG_FILES([Makefile
         cfg/Makefile
         agent/Makefile
         IARMBUS_stub/Makefile
         DS_stub/Makefile
         ClosedCaption_stub/Makefile
         RDKLogger_stub/Makefile
         TDKIntegration_Stub/Makefile
         Mediaframework_stub/Makefile
         MediaStreamer_stub/Makefile
	 NetSrvMgr_stub/Makefile
         OpenSourceComponent_Stub/Makefile
         TR069_stub/Makefile
         TRM_stub/Makefile
         rmfApp_stub/Makefile
         XUPNP_stub/Makefile
         DTCP_stub/Makefile
         tdkRmfApp/Makefile])
AC_OUTPUT
