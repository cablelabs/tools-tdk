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

include ../../def.inc

ifeq ($(RDK_VERSION),RDK1DOT3)
COPTS     += -DRDK_BR_1DOT3
VERSION    = br1.3
endif
ifeq ($(RDK_VERSION),RDK1DOT2)
COPTS     += -DRDK_BR_1DOT2
VERSION    = br1.2
endif

ifeq ($(RDK_VERSION),RDK2DOT0)
COPTS     += -DRDK_BR_2DOT0
VERSION    = br2.0
endif

#The PKG_CONFIG_PATH needs to be changed based on the toolchain on user's environment
export PKG_CONFIG_PATH =$(RDK_BUILD_DIR)/workXI3/Refsw/AppLibs/target/97428b0.mipsel-linux.release/usr/local/lib/pkgconfig
PLAYERCFLAGS    := `pkg-config gstreamer-0.10 libffi --cflags`
PLAYERLIBS      := `pkg-config gstreamer-0.10 libffi --libs`
CC	  := gcc

SOURCE_APP:= $(PLAYER_SRC_PATH)/*.c
PLAYER_EXE:= mplayer

all : 
	mkdir -p $(TARGETDIR)
	$(CROSSCOMPILE)$(CC) $(PLAYERCFLAGS) $(SOURCE_APP) -o $(PLAYER_EXE) $(PLAYERLIBS)
	mv $(PLAYER_EXE) $(TDK_BIN_PATH)

build: all

