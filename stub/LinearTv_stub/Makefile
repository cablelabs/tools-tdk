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

LDOPTS    +=    -L $(IMAGE_PATH)/usr/local/lib \


INCLUDES  += 	-I./include \
                -I../agent/include \
		-I$(PLATFORM_SDK)/include \
                -I$(PLATFORM_SDK)/include/curl \
		-I$(JSONRPC_PATH)/include \
  	        -I$(JSONCPP_PATH)/include \
             	-I$(CURL_PATH)


		
LIBOPTS   := -shared

CC	  := g++
LIBLINEARTV  := liblineartvstub.so	
scripts := scripts/T2pTrickMode.sh  scripts/T2pTuning.sh

#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBLINEARTV)

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
	$(CROSSCOMPILE)$(CC) $(INCLUDES) -fPIC $(COPTS) $^
	mv *.o $(OBJDIR)

#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	mkdir -p $(LIBDIR) 
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBLINEARTV)
	rm -rf $(OBJDIR)
	mv $(LIBLINEARTV) $(LIBDIR)
	cp $(scripts) $(TARGET)
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

