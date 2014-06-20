include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := ./src/
OBJDIR	  := obj
COPTS     := -c
VERSION    = br2.0

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
		 


INCLUDES  :=    -I./include \
                -I../agent/include \
                -I$(PLATFORM_SDK)/include \
                -I$(JSONRPC_PATH)/include \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH)
               		
LIBOPTS   := -shared

CPP	  := g++
CC        := gcc

LDOPTS    :=    -L $(IMAGE_PATH)/usr/local/lib 

LIBRECORDER	  := libRecorderstub.so	
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBRECORDER)
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
	$(CROSSCOMPILE)$(CPP) $(CFLAGS) $(INCLUDES) -fPIC $(COPTS)  $^
	mv *.o $(OBJDIR)


#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	$(CROSSCOMPILE)g++ $(OBJS) -fPIC $(LIBOPTS) -o $(LIBRECORDER) $(LDOPTS)
	rm -rf $(OBJDIR)
	mkdir -p $(TDK_BIN_PATH)/scripts
	cp -r ../platform/Recorder_stub/scripts/* $(TDK_BIN_PATH)/scripts
	mv $(LIBRECORDER) $(LIBDIR)
#
# Build everything
#
build: $(LIB) 

#
# Clean 
#
clean:
	rm -rf $(LIB)
