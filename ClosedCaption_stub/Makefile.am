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

AM_CPPFLAGS = -Wall -DGCC4_XXX -fPIC $(COPTS)

AM_CXXFLAGS = -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/directfb \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
              -I${top_srcdir}/ClosedCaption_stub/include -I${top_srcdir}/agent/include
lib_LTLIBRARIES = libccstub.la
libccstub_la_SOURCES = src/CCStub.cpp
libccstub_la_LIBADD = -lrdkloggers -lrdkCCGfx -lrdkCCManager -ldirectfb -lcurl -llog4c -lz -lrdkCCReader
libccstub_la_includedir = ${includedir}
