include ../def.inc

#This Makefile is to build the agent binary and tftp server from the source and library file 

default: build

SCRIPTS += scripts/output_json_parser.sh scripts/file_copy.sh scripts/RemoveLogs.sh

COPTS     += -rdynamic

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

#Defining RDK version
ifndef RDK_VERSION
$(error You must define the RDK_VERSION variable in def.inc)
else
COPTS     += -DRDKVERSION="\"$(RDK_VERSION)\""
endif

#
# Source files
#
LDOPTS    +=    -L $(IMAGE_PATH)/usr/local/lib \
		-L ../../opensource/lib/

INCLUDES  += -I ./include \
             -I$(PLATFORM_SDK)/include \
             -I$(JSONRPC_PATH)/include \
             -I$(JSONCPP_PATH)/include \
             -I$(CURL_PATH)

LDOPTS	  += -ljsoncpp \
	     -l$(JSONRPC_LIB)\
	     -ldl \
	     -lpthread 

ifeq ($(RDK_VERSION),RDK1DOT2)
LDOPTS    += -llogger
endif


CC	  := g++
TARGETNAME:=$(TARGETDIR)/rdk_tdk_agent_process
SOURCES   := src/*.cpp


#
# Build the TARGET from library and souce files
#
TARGET:
	mkdir -p $(TARGETDIR)
	$(CROSSCOMPILE)$(CC) $(COPTS) $(SOURCES) $(LDOPTS) $(INCLUDES) -o $(TARGETNAME)
	cp $(SCRIPTS) $(TARGETDIR)

#
# Build everything
#
build: TARGET

#
# Clean 
#
clean:
	rm -rf $(TARGETDIR)/rdk_tdk_agent_process
