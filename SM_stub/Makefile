include ../def.inc
default: build
#
# Source files
#
SRC_DIR   := ./src/
OBJDIR	  := obj
COPTS     += -c

ifeq ($(RDK_VERSION),RDK1DOT3)
VERSION    = br1.3
endif
ifeq ($(RDK_VERSION),RDK1DOT2)
VERSION    = br1.2
endif
ifeq ($(RDK_VERSION),RDK2DOT0)
VERSION    = br2.0
endif

LDOPTS    += -L $(IMAGE_PATH)/usr/local/lib  \
	     -L $(IMAGE_PATH)/usr/lib \
	     -L $(IMAGE_PATH)/lib \
	     -L $(IMAGE_PATH)/usr/local/Qt/lib

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

INCLUDES  +=    -I include \
                -I ../agent/include \
		-I$(PLATFORM_SDK)/include \
                -I$(JSONRPC_PATH)/include \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH) \
                -I $(RDK_BUILD_DIR)/servicemanager/include \
                -I $(RDK_BUILD_DIR)/servicemanager/include/services \
                -I $(RDK_BUILD_DIR)/servicemanager/include/helpers \
		-I $(IMAGE_PATH)/usr/local/Qt/include/QtWidgets \
                -I $(IMAGE_PATH)/usr/local/Qt/include/\
                -I $(IMAGE_PATH)/usr/local/Qt/include/QtCore/\
                -I $(RDK_BUILD_DIR)/opensource/qt/stage//usr/local/Qt/include/\
                -I $(RDK_BUILD_DIR)/opensource/qt/stage//usr/local/Qt/include/QtCore


#LIBs common for Both CLIENT and GATEWAY
LDOPTS += -lservicemanager -l:libgobject-2.0.so.0 -l:libgio-2.0.so.0 -l:libgstapp-0.10.so.0 -l:libgstinterfaces-0.10.so.0 -l:libgstreamer-0.10.so.0 -l:libgmodule-2.0.so.0 -l:libgstcontroller-0.10.so.0 


LIBOPTS   := -shared
CC	  := g++
LIBSM	  := libservicemanagerstub.so	
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBSM)
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
	$(CROSSCOMPILE)$(CC) -Wall $(INCLUDES) -fPIC $(COPTS) $^ 
	mv *.o $(OBJDIR)


#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	mkdir -p $(LIBDIR)
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBSM) $(LDOPTS)
	rm -rf $(OBJDIR)
	mv $(LIBSM) $(LIBDIR)
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

