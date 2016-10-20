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
ACLOCAL_AMFLAGS = -Im4 --install

AM_CPPFLAGS = ${COPTS} -DRMF_OSAL_LITTLE_ENDIAN -g -Wall -Wno-format -Wunused -DUSE_CC_GETTIMEOFDAY -DRMF_OSAL_FEATURE_IPV6 -DXONE_STB -DUSE_HW_DEMUX -DUSE_QAMSRC -DUSE_TRANSCODEFILTER -DUSE_FRONTPANEL -DUSE_DTCP -DUSE_HNSINK -DUSE_HNSRC -DUSE_DVR -DUSE_VODSRC -DUSE_MEDIAPLAYERSINK -DSRC_INIT_IN_CONSTRUCTOR -DRMF_STREAMER -DENABLE_AUTODISCOVERY_FOR_VOD -DQAMSRC_FACTORY -DQAMSRC_PMTBUFFER_PROPERTY -DRECORDER_SUPPORT -DTEST_WITH_PODMGR -DIPPV_CLIENT_ENABLED -DUSE_POD_IPC -DOOBSI_SUPPORT -DDEBUG_CONF_FILE="\"debug.ini\"" -DENV_CONF_FILE="\"rmfconfig.ini\"" -DRDK_BR_2DOT0

INCLUDES = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/core/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/gstreamer \
          \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/gstreamer-0.10/gst/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0/ \
          -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include/ \
          \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/glib/glib/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/glib/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/gstreamer/gstreamer-0.10.34/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/libxml2/include/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/opensource/src/glib/gmodule \
            \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/osal/utils/inc/ \
            \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/hnsource/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/hnsink/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/dvr/source/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/dvr/common/tasseograph/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/dvr/common/dvrmgr/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdklogger/include/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/dvr/sink/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/qamsource/main/ \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/mediaframework/init/ \
            \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
          -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/curl \
              -I${top_srcdir}/MediaStreamer_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libmediastreamerstub.la
libmediastreamerstub_la_SOURCES = src/MediaStreamerStub.cpp
libmediastreamerstub_la_LIBADD = -ldvrmgr -lqamsrc -lhnsource -lmediaplayersink

libmediastreamerstub_la_includedir = ${includedir}
libmediastreamerstub_la_include_HEADERS = ${top_srcdir}/MediaStreamer_stub/include/MediaStreamerStub.h

