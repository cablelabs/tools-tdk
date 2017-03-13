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

AM_CPPFLAGS = -g -Wall -DGCC4_XXX -fPIC -DRMF_OSAL_LITTLE_ENDIAN -DUSE_RBI ${SOC_FLAGS}

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/json \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/jsonrpc \
              -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/glib-2.0 \
              -I${PKG_CONFIG_SYSROOT_DIR}/usr/lib/glib-2.0/include \
              -I${top_srcdir}/agent/include

bin_PROGRAMS = tdkRmfApp
tdkRmfAppdir = ${bindir}
tdkRmfApp_SOURCES = tdkRmfApp.cpp
tdkRmfApp_LDFLAGS = -ldvrmgr -ldvrsink -lmediaplayersink -lhnsource -luuid -lsharedtsb -lrbifilter -lrbi ${SOC_LIBS} $(TDK_GST_LIBS)
tdkRmfApp_includedir = ${includedir}
