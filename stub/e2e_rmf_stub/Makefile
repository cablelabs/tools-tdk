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

LDOPTS    += -L $(IMAGE_PATH)/usr/local/lib/ 

CFLAGS += -g -Wall -DGCC4_XXX

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
                -I../agent/include \
		-I$(PLATFORM_SDK)/include \
                -I$(JSONRPC_PATH)/include \
                -I$(JSONRPC_PATH)/include/jsonrpc \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH)\
		-I$(RDK_BUILD_DIR)/mediaframework/core/ \
                -I$(RDK_BUILD_DIR)/mediaframework/mediaplayersink/\
                -I$(RDK_BUILD_DIR)/mediaframework/hnsource/\
		-I${PLATFORM_SDK}/lib/glib-2.0/include \
            	-I${PLATFORM_SDK}/include/glib-2.0 \
            	-I${PLATFORM_SDK}/include/gstreamer-0.10 \
            	-I$(PLATFORM_SDK)/include \
            	-I$(PLATFORM_SDK)/usr/local/include \
            	-I$(PLATFORM_SDK)/usr/include \
            	-I$(PLATFORM_SDK)/include/linux_user \
            	-I${PLATFORM_SDK}/include/libxml2

LDOPTS    +=  -L $(IMAGE_PATH)/usr/local/lib \
              -L $(IMAGE_PATH)/usr/lib \
              -L $(IMAGE_PATH)/lib \
              -L $(IMAGE_PATH)/mnt/nfs/lib \
              -L $(IMAGE_PATH)/mnt/nfs/bin/ \
              -L $(IMAGE_PATH)/mnt/nfs/bin/target-snmp/lib	\
		 -ltinyxml -lgstapp-0.10 -lgobject-2.0 -lgstbase-0.10 -llog4c -lgmodule-2.0 -lgthread-2.0 -lglib-2.0 -lgstreamer-0.10 -luuid

LIBOPTS   := -shared

CC        := g++
LIBENDTOENDRMF     := libendtoendrmfstub.so
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBENDTOENDRMF)
SOURCES   +=	$(SRC_DIR)*.cpp	

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
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBENDTOENDRMF) $(LDOPTS) 
	rm -rf $(OBJDIR)
	mv $(LIBENDTOENDRMF) $(LIBDIR)
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
