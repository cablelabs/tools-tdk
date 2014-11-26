dnl                                               -*- Autoconf -*-
dnl Process this file with autoconf to produce a configure script.

dnl AC_PREREQ([2.69])
AC_INIT(tdk, 1.0, ridish.ra@lnttechservices.com,tdk)
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
DVRMGR_FLAGS=" "
QAM_LIBS=" "
SF_LIBS=" "
HEADLESS=" "
SUBDIR_HYBRID=" "
SUBDIR_CLIENT=" "
SM_STUB_CFLAG_HYBRID=" "
AC_ARG_ENABLE([hybrid],
        AS_HELP_STRING([--enable-hybrid],[enable hybrid build]),
        [
          case "${enableval}" in
             yes) HYBRID=true
                  SUBDIR_HYBRID="TRM_stub Recorder_stub Mediaframework_stub MediaStreamer_stub tdkRmfApp"
                  SM_STUB_CFLAG_HYBRID="-DENABLE_WEBSOCKET_SERVICE" ;;
           no) HYBRID=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-headless ]) ;;
           esac
           ],
         [echo "headless build is enable"])
AM_CONDITIONAL([HYBRID], [test x$HYBRID = xtrue])

AC_ARG_ENABLE([client],
        AS_HELP_STRING([--enable-client],[enable client build]),
        [
          case "${enableval}" in
             yes) CLIENT=true
                  SUBDIR_CLIENT="TR069_stub gstPluginsRdk_check gstPluginsRdk_stub" ;;
           no) CLIENT=false ;;
          *) AC_MSG_ERROR([bad value ${enableval} for --enable-headless ]) ;;
           esac
           ],
         [echo "headless build is enable"])
AM_CONDITIONAL([CLIENT], [test x$CLIENT = xtrue])

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



PKG_CHECK_MODULES([GST], [gstreamer-0.10 >= 0.10.28])
PKG_CHECK_MODULES([GST_CHECK], [gstreamer-check-0.10 >= 0.10.28])
PKG_CHECK_MODULES([GLIB], [glib-2.0 >= 0.10.28])
PKG_CHECK_MODULES([XML2], [libxml-2.0 >= 2.7.8])
PKG_CHECK_MODULES([JANSON],[jansson >= 2.4])

AC_SUBST(COPTS)
AC_SUBST(DVRMGR_FLAGS)
AC_SUBST(QAM_LIBS)
AC_SUBST(SF_LIBS)
AC_SUBST(SUBDIR_HYBRID)
AC_SUBST(SUBDIR_CLIENT)
AC_SUBST(SM_STUB_CFLAG_HYBRID)
AC_CONFIG_FILES([Makefile
         cfg/Makefile
         agent/Makefile
         SM_stub/Makefile
         IARMBUS_stub/Makefile
         DS_stub/Makefile
         ClosedCaption_stub/Makefile
         RDKLogger_stub/Makefile
         TDKIntegration_Stub/Makefile
         gstPluginsRdk_check/Makefile
         gstPluginsRdk_stub/Makefile
         Recorder_stub/Makefile
         Mediaframework_stub/Makefile
         MediaStreamer_stub/Makefile
         OpenSourceComponent_Stub/Makefile
         TR069_stub/Makefile
         TRM_stub/Makefile
         tdkRmfApp/Makefile])
AC_OUTPUT
