include ../def.inc

default: build

#
# Source files
#
SRC_DIR   := ./src/
OBJDIR	  := obj
COPTS     += -c

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


#LIBDIR   := ../../$(VERSION)/libs/
#TARGETDIR := ../../$(VERSION)/bin/
		
INCLUDES  += 	-I./include \
                -I../agent/include \
		-I$(PLATFORM_SDK)/include \
                -I$(JSONRPC_PATH)/include \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH)
		  

		
LIBOPTS   := -shared

CCX	  := g++
CC	  := gcc
LIBE2E	  := libe2estub.so	
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBE2E)
SOURCES   := $(SRC_DIR)*.cpp
SOURCE_APP:= $(PLAYER_SRC_PATH)*.c
PLAYER_EXE:= mplayer
TARGET    := $(TARGETDIR)/$(PLAYER_EXE)
SCRIPTS	:= $(PLAYER_SRC_PATH)/scripts/mplayerscript.sh $(PLAYER_SRC_PATH)/scripts/runmplayer_xi3.sh
  
#
# Intermediate files
#
OBJS       =$(OBJDIR)/*.o

#
# Compile source files into intermediate files
#
$(OBJS): $(SOURCES) 
	mkdir -p $(OBJDIR)
	$(CROSSCOMPILE)$(CCX) $(INCLUDES) -fPIC $(COPTS) $^
	mv *.o $(OBJDIR)


#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	mkdir -p $(LIBDIR)   
	$(CROSSCOMPILE)$(CCX) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBE2E)
	rm -rf $(OBJDIR)
	mv $(LIBE2E) $(LIBDIR)

player:
	$(MAKE) -C $(PLAYER_SRC_PATH)
	cp $(SCRIPTS) $(TARGETDIR) 

build: player
build: $(LIB) 

#
# Clean 
#
clean:
	rm -rf $(OBJDIR)
	rm -rf $(LIB)

