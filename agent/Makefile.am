## Copyright (c) 2013 Comcast. All rights reserved.

AM_CXXFLAGS = -DDEBUG_LEVEL_TRACE -DAGENT_LOG_ENABLE -DRDKVERSION="\"${RDK_VERSION}\"" $(GST_CFLAGS) $(GST_LIBS)  \
              -I./include -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

bin_PROGRAMS = rdk_tdk_agent_process
rdk_tdk_agent_processdir = ${bindir}
rdk_tdk_agent_process_SOURCES = src/agentmain.cpp src/rpcmethods.cpp
rdk_tdk_agent_process_SCRIPTS = scripts/runSysStat.sh scripts/TDK_version.txt
rdk_tdk_agent_process_LDADD = -ljsoncpp -ljsonrpc-cpp -ldl -lpthread
rdk_tdk_agent_process_includedir = ${includedir}
