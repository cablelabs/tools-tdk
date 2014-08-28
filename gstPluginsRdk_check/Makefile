include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := ./src/
COPTS     := -Wall

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

		 
INCLUDES  +=    -I./include \
		-I ../agent/include \
                -I$(PLATFORM_SDK)/include \
		-I$(JSONRPC_PATH)/include \
                -I$(JSONRPC_PATH)/include/jsonrpc \
	        -I$(JSONCPP_PATH)/include \
             	-I$(CURL_PATH)
		
LDOPTS	+=	-L $(IMAGE_PATH)/lib \
		-L $(IMAGE_PATH)/usr/lib \
		-L $(IMAGE_PATH)/usr/local/lib	\
		-ldl -lpthread

CC	  := gcc
#
# Library built by this makefile
#
TARGETNAME:=$(TARGETDIR)/gstpluginsrdkcheck
SOURCES   := $(SRC_DIR)*.c


TARGET:
	mkdir -p $(TARGETDIR)
	$(CROSSCOMPILE)$(CC) $(SOURCES) $(INCLUDES) $(COPTS) -o $(TARGETNAME) $(LDOPTS)

#
# Build everything
#
build: TARGET

#
# Clean
#
clean:
	rm -rf $(TARGETDIR)/gstpluginsrdkcheck
