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

AM_CPPFLAGS = -DQT_WEBKIT_LIB ${COPTS} -std=c++0x -fPIC -DGCC4_XXX -DBUILD_DVRSOURCE -DRMF_STREAMER -DENABLE_DVRSRC_MPSINK -DRMF_OSAL_LITTLE_ENDIAN

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
              -I${top_srcdir}/Mediaframework_stub/include -I${top_srcdir}/agent/include

lib_LTLIBRARIES = libmediaframeworkstub.la
libmediaframeworkstub_la_SOURCES = src/MediaframeworkAgent.cpp
libmediaframeworkstub_la_LIBADD = -ldvrmgr -lqamsrc -ldvrmgrsoc -lhnsource -ldvrsink -lhnsink -lmediaplayersink -ldvrsource -lrmfinit
libmediaframeworkstub_la_includedir = ${includedir}
libmediaframeworkstub_la_include_HEADERS = ${top_srcdir}/Mediaframework_stub/include/MediaframeworkAgent.h

