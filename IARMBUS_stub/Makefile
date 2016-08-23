## Copyright (c) 2013 Comcast. All rights reserved.

include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := ./src/
OBJDIR	  := obj
COPTS     := -c -g -Wall -DGCC4_XXX -Wno-format -Wunused
APP_EXE   := tst_iarmbus
DUMMY_TESTAPP_EXE   := Test_Event_Mgr 
SINGLEEVT_APP_EXE   := gen_single_event
MULTIEVT_APP_EXE   := gen_multiple_events
IREVT_APP_EXE      := gen_irevent

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
INCLUDES  +=    -I$(RDK_BUILD_DIR)/iarmbus/core/include -I$(RDK_BUILD_DIR)/iarmbus/core -I$(RDK_BUILD_DIR)/iarmmgrs/generic/ir/include -I$(RDK_BUILD_DIR)/iarmmgrs/generic/mfr/include -I$(RDK_BUILD_DIR)/iarmmgrs/generic/sysmgr/include -I$(RDK_BUILD_DIR)/iarmmgrs/generic/disk/include 
LDOPTS    +=    -L $(IMAGE_PATH)/usr/local/lib 	

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

		
INCLUDES  += 	-I./include \
                -I../agent/include \
		-I$(PLATFORM_SDK)/include \
		-I$(JSONRPC_PATH)/include \
		-I$(JSONCPP_PATH)/include \
		-I$(CURL_PATH) 


LDOPTS	  += -lIARMBus -lglib-2.0
LIBOPTS   += -shared

CC	  := g++
LIBIARM	  := libiarmbusstub.so	

#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBIARM)

SOURCES   := $(SRC_DIR)/IARMBUSStub.cpp
SOURCE_APP:= $(SRC_DIR)/tst_iarmbus.c
DUMMY_TEST_APP_SOURCE:= $(SRC_DIR)/Test_Event_Mgr.c
TARGET    := $(TARGETDIR)/$(APP_EXE)
DUMMY_TEST_APP    := $(TARGETDIR)/$(DUMMY_TESTAPP_EXE)
SINGLEEVT_SOURCE_APP:= $(SRC_DIR)/gen_single_event.cpp
MULTIEVT_SOURCE_APP:= $(SRC_DIR)/gen_multiple_events.cpp
IREVT_SOURCE_APP:= $(SRC_DIR)/gen_irevent.cpp
SINGLEEVT_APP_TARGET    := $(TARGETDIR)/$(SINGLEEVT_APP_EXE)
MULTIEVT_APP_TARGET    := $(TARGETDIR)/$(MULTIEVT_APP_EXE)
IREVT_APP_TARGET    := $(TARGETDIR)/$(IREVT_APP_EXE)


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
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBIARM) $(LDOPTS)
	rm -rf $(OBJDIR)
	mv $(LIBIARM) $(LIBDIR)
#
# Build everything
#
$(TARGET): $(SOURCE_APP)
	mkdir -p $(TARGETDIR)
	$(CROSSCOMPILE)$(CC) $(INCLUDES) -DDEBUG_LEVEL_TRACE $(LDOPTS) -o $(APP_EXE) $^
	mv $(APP_EXE) $(TARGETDIR)

$(DUMMY_TEST_APP): $(DUMMY_TEST_APP_SOURCE)
	$(CROSSCOMPILE)$(CC) $(INCLUDES) -DDEBUG_LEVEL_TRACE $(LDOPTS) -o $(DUMMY_TESTAPP_EXE) $^
	mv $(DUMMY_TESTAPP_EXE) $(TARGETDIR)

$(SINGLEEVT_APP_TARGET): $(SINGLEEVT_SOURCE_APP)
	mkdir -p $(TARGETDIR)
	$(CROSSCOMPILE)$(CC) $(INCLUDES) -DDEBUG_LEVEL_TRACE $(LDOPTS) -lrt -o $(SINGLEEVT_APP_EXE) $^
	mv $(SINGLEEVT_APP_EXE) $(TARGETDIR)

$(MULTIEVT_APP_TARGET): $(MULTIEVT_SOURCE_APP)
	mkdir -p $(TARGETDIR)
	$(CROSSCOMPILE)$(CC) $(INCLUDES) -DDEBUG_LEVEL_TRACE $(LDOPTS) -lrt -o $(MULTIEVT_APP_EXE) $^
	mv $(MULTIEVT_APP_EXE) $(TARGETDIR)

$(IREVT_APP_TARGET): $(IREVT_SOURCE_APP)
	mkdir -p $(TARGETDIR)
	$(CROSSCOMPILE)$(CC) $(INCLUDES) -DDEBUG_LEVEL_TRACE $(LDOPTS) -lrt -o $(IREVT_APP_EXE) $^
	mv $(IREVT_APP_EXE) $(TARGETDIR)


build: $(LIB) $(TARGET) $(DUMMY_TEST_APP) $(SINGLEEVT_APP_TARGET) $(MULTIEVT_APP_TARGET) $(IREVT_APP_TARGET)
#
# Clean 
#
clean:
	rm -rf $(OBJDIR)
	rm -rf $(LIB)
	rm -rf $(TARGET)
	rm -rf $(DUMMY_TEST_APP)
	rm -rf $(SINGLEEVT_APP_TARGET)
	rm -rf $(MULTIEVT_APP_TARGET)
	rm -rf $(IREVT_APP_TARGET)

