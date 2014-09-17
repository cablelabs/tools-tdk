## Copyright (c) 2013 Comcast. All rights reserved.

SUBDIRS =

AM_CXXFLAGS = -DAGENT_LOG_ENABLE $(GST_CFLAGS) $(GST_LIBS)  \
              -I./include -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

bin_PROGRAMS = agent
agentdir = ${bindir}
agent_SOURCES = src/agentmain.cpp src/rpcmethods.cpp
agent_SCRIPTS = scripts/configure_iptables.sh scripts/flush_iptables.sh scripts/get_moca_devices.sh scripts/runSysStat.sh scripts/TDK_version.txt
agent_LDADD = -ljsoncpp -ljsonrpc-cpp -ldl -lpthread
agent_includedir = ${includedir}
