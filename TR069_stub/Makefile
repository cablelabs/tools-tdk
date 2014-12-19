include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := ./src/
OBJDIR	  := obj
COPTS     := -c -Wall

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
	        -I$(JSONCPP_PATH)/include \
             	-I$(CURL_PATH)

LDOPTS += -L $(IMAGE_PATH)/usr/lib -L $(IMAGE_PATH)/usr/local/lib

LIBOPTS   := -shared
CC	  := g++
TARGETLIB	:= libtr069modulestub.so	
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(TARGETLIB)
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
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) $(LDOPTS) -o $(TARGETLIB)
	rm -rf $(OBJDIR)
	mv $(TARGETLIB) $(LIBDIR)
#
# Build everything
#
build: $(LIB) 

#
# Clean 
#
clean:
	rm -rf $(LIB)
	rm -rf $(OBJDIR)

