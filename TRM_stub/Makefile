## Copyright (c) 2013 Comcast. All rights reserved.

include ../def.inc
default: build

CC      = g++
CFLAGS  = -Wall -g -DGCC4_XXX -Wno-format -Wunused

#
# Source files
#
SRC_DIR = src
OBJ_DIR = ./
TRM_LIB = libtrmstub.so

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

ifeq ($(RDK_PLATFORM_DEVICE),xg1)
ifeq ($(RDK_PLATFORM_SOC),intel)
TRM_NUMBER_OF_TUNERS=5
endif
ifeq ($(RDK_PLATFORM_SOC),broadcom)
TRM_NUMBER_OF_TUNERS=6
endif
COPTS     += -DNUM_OF_TUNERS=$(TRM_NUMBER_OF_TUNERS)
endif

OBJS       = $(OBJ_DIR)/TRMAgent.o $(OBJ_DIR)/TRMAgentHelper.o

INCLUDES+= -I./include \
	-I../agent/include \
	-I$(JSONRPC_PATH)/include \
	-I$(JSONCPP_PATH)/include \
	-I$(CURL_PATH)\
	-I$(CURL_PATH)/../ \
	-I$(RDK_BUILD_DIR)/opensource/include \
	-I$(RDK_BUILD_DIR)/opensource/include/uuid \
	-I$(RDK_BUILD_DIR)/trm/common/include

CFLAGS  += $(INCLUDES)

LDOPTS  += -L $(IMAGE_PATH)/usr/local/lib \
           -L $(IMAGE_PATH)/usr/lib \
           -ltrm

build: clean library install
	@echo "Build Finished...."

library: $(OBJS)
	@echo "Building $(TRM_LIB) ...."
	$(CROSSCOMPILE)$(CC) $(OBJS) $(CFLAGS) -fPIC $(COPTS) $(LDOPTS) -shared -Wl,-rpath -o $(TRM_LIB)
	rm -rf $(OBJS)

$(OBJ_DIR)/%.o:$(SRC_DIR)/%.cpp
	$(CROSSCOMPILE)$(CC) -c $< $(CFLAGS) -fPIC $(COPTS) -o $@

install:
	mv $(TRM_LIB) $(LIBDIR)

#
# Clean
#
clean :
	rm -rf *.o $(TRM_LIB)
