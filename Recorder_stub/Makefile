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
SRC_DIR   := ./src/
OBJDIR	  := obj
COPTS     := -c
VERSION    = br2.0

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
		 


INCLUDES  :=    -I./include \
                -I../agent/include \
                -I$(PLATFORM_SDK)/include \
                -I$(JSONRPC_PATH)/include \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH)
               		
LIBOPTS   := -shared

CPP	  := g++
CC        := gcc

LDOPTS    :=    -L $(IMAGE_PATH)/usr/local/lib 

LIBRECORDER	  := libRecorderstub.so	
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBRECORDER)
SOURCES   := $(SRC_DIR)*.cpp

#
# Intermediate files
#
OBJS       =$(OBJDIR)/*.o

#
# Compile source files into intermediate files
#
$(OBJS): $(SOURCES) 
	mkdir -p $(OBJDIR)
	$(CROSSCOMPILE)$(CPP) $(CFLAGS) $(INCLUDES) -fPIC $(COPTS)  $^
	mv *.o $(OBJDIR)


#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	$(CROSSCOMPILE)g++ $(OBJS) -fPIC $(LIBOPTS) -o $(LIBRECORDER) $(LDOPTS)
	rm -rf $(OBJDIR)
	mkdir -p $(TDK_BIN_PATH)/scripts
	cp -r ../platform/Recorder_stub/scripts/* $(TDK_BIN_PATH)/scripts
	mv $(LIBRECORDER) $(LIBDIR)
#
# Build everything
#
build: $(LIB) 

#
# Clean 
#
clean:
	rm -rf $(LIB)
