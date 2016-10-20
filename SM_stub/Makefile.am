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
AM_CXXFLAGS = -DQT_WEBKIT_LIB -DUSE_DEVICE_SETTINGS_SERVICE -DSCREEN_CAPTURE $(SM_STUB_CFLAG_HYBRID) $(GST_CFLAGS) ${COPTS} \
	      -fPIC -I${top_srcdir}/include -I${top_srcdir}/../agent/include \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir) \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager/helpers \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/rdk/servicemanager/services \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5 \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtWidgets \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtCore \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtGui \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtNetwork/ \
	      -I${PKG_CONFIG_SYSROOT_DIR}$(includedir)/qt5/QtWebKitWidgets

lib_LTLIBRARIES = libservicemanagerstub.la
libservicemanagerstub_la_SOURCES = src/ServiceManagerAgent.cpp
libservicemanagerstub_la_LIBADD = -lservicemanager
libservicemanagerstub_la_includedir = ${includedir}
