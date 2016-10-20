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
AM_CXXFLAGS = -DYOCTO_LIB_LOADING -DDEBUG_LEVEL_TRACE -DRDKVERSION="\"${RDK_VERSION}\"" $(GST_CFLAGS) $(GST_LIBS) $(AGENT_FLAGS) \
              -I${top_srcdir}/agent/include -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

bin_PROGRAMS = rdk_tdk_agent_process
rdk_tdk_agent_processdir = ${bindir}
rdk_tdk_agent_process_SOURCES = src/agentmain.cpp src/rpcmethods.cpp
rdk_tdk_agent_process_LDADD = -ljsoncpp -ljsonrpc-cpp -ldl -lpthread
rdk_tdk_agent_process_includedir = ${includedir}
