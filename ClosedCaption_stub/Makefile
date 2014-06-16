include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := ./src
OBJDIR	  := obj
COPTS     := -c

CFLAGS    := -g -Wall -DGCC4_XXX

LDOPTS    := -L $(IMAGE_PATH)/usr/local/lib

ifeq ($(RDK_VERSION),RDK1DOT2)
LDOPTS    += -llogger
endif
ifeq ($(RDK_VERSION),RDK1DOT3)
LDOPTS    += -lrdklogger
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

INCLUDES  += -I./include \
             -I../agent/include \
             -I$(JSONRPC_PATH)/include \
             -I$(JSONCPP_PATH)/include \
             -I$(CURL_PATH) \
             -I$(CURL_PATH)/../ \
             -I$(RDK_BUILD_DIR)/closedcaption/ccManager/utils \
             -I$(RDK_BUILD_DIR)/closedcaption/ccGraphics

CC	  := g++
LIBCC 	  := libccstub.so	

#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBCC)
SOURCES   := $(SRC_DIR)/*.cpp

#
# Intermediate files
#
OBJS       =$(OBJDIR)/*.o

#
# Compile source files into intermediate files
#
$(OBJS): $(SOURCES) 
	mkdir -p $(OBJDIR)
	$(CROSSCOMPILE)$(CC) $(CFLAGS) $(INCLUDES) -fPIC $(COPTS) $^
	mv *.o $(OBJDIR)


#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC -shared -o $(LIBCC) $(LDOPTS)
	rm -rf $(OBJDIR)
	mv $(LIBCC) $(LIBDIR)
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
