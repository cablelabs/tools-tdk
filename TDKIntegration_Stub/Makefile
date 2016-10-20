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
include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := src/
OBJDIR    := ./obj
COPTS     += -c

ifeq ($(RDK_VERSION),RDK1DOT3)
COPTS     += -DRDK_BR_1DOT3
VERSION    = br1.3
endif

ifeq ($(RDK_VERSION),RDK2DOT0)
COPTS     += -DRDK_BR_2DOT0
VERSION    = br2.0
endif

ifeq ($(RDK_VERSION),RDK1DOT2)
COPTS     += -DRDK_BR_1DOT2
VERSION    = br1.2
endif

#debug log level
ifeq ($(DEBUG_LEVEL),TRACE)
COPTS     += -DDEBUG_LEVEL_TRACE
endif
ifeq ($(DEBUG_LEVEL),LOG)
COPTS     += -DDEBUG_LEVEL_LOG
endif
ifeq ($(DEBUG_LEVEL),ERROR)
COPTS     += -DDEBUG_LEVEL_ERROR
endif
CFLAGS += -g -Wall 
LDOPTS    +=  -L $(IMAGE_PATH)/usr/local/lib \
              -L $(IMAGE_PATH)/usr/lib \
              -L $(IMAGE_PATH)/lib 

ifneq ($(SINGLE_TUNER_IP_CLIENT),y)
#LDOPTS    += -lsdvsectionfilter -lrmfsdvconfiguration -lrmfsdvdiscovery -lcurl
endif

INCLUDES  +=    -I./include \
                -I../agent/include \
                -I$(PLATFORM_SDK)/include \
                -I$(JSONRPC_PATH)/include \
                -I$(JSONRPC_PATH)/include/jsonrpc \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH)

LIBOPTS   := -shared

CC        := g++
LIBTDKINTEGRATION  := libtdkintegrationstub.so
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBTDKINTEGRATION)
SOURCES   +=	$(SRC_DIR)*.cpp $(BENCHMARK_SRC)

#
# Intermediate files
#
OBJS       =$(OBJDIR)/*.o

#
# Compile source files into intermediate files
#
$(OBJS): $(SOURCES)
	mkdir -p $(OBJDIR)
	$(CROSSCOMPILE)$(CC) -Wall $(INCLUDES) -fPIC $(COPTS) $(CFLAGS) $^
	mv *.o $(OBJDIR)
#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	mkdir -p $(LIBDIR)
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBTDKINTEGRATION) $(LDOPTS) 
	rm -rf $(OBJDIR)
	mv $(LIBTDKINTEGRATION) $(LIBDIR)
#
# Build everything
#
build: $(LIB)

#
# Clean
#
clean:
	rm -rf $(OBJDIR)
	rm -rf $(LIB)
