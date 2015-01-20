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
