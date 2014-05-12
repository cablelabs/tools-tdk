include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := ./src/
OBJDIR	  := obj
COPTS     := -c
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
ifeq ($(RDK_VERSION),RDK1DOT3)
export PKG_CONFIG_PATH =$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/lib/pkgconfig/
PLAYERCFLAGS    := `pkg-config gstreamer-0.10  --cflags`
PLAYERLIBS      := `pkg-config gstreamer-0.10  --libs`
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
		 
ifeq ($(RDK_VERSION),RDK2DOT0)	
INCLUDES  :=	-I$(RDK_BUILD_DIR)/mediaframework/core/ -I $(RDK_BUILD_DIR)/opensource/src/gstreamer -I $(RDK_BUILD_DIR)/opensource/src/glib/glib/ -I $(RDK_BUILD_DIR)/opensource/src/glib/ -I $(RDK_BUILD_DIR)/opensource/gstreamer/gstreamer-0.10.34 -I $(RDK_BUILD_DIR)/opensource/src/libxml2/include/ -I $(RDK_BUILD_DIR)/opensource/src/glib/gmodule -I$(RDK_BUILD_DIR)/mediaframework/hnsource/ -I$(RDK_BUILD_DIR)/mediaframework/dvr/source/ -I$(RDK_BUILD_DIR)/mediaframework/dvr/common/tasseograph -I$(RDK_BUILD_DIR)/mediaframework/dvr/common/dvrmgr/ -I$(RDK_BUILD_DIR)/rdklogger/include/  -I$(RDK_BUILD_DIR)/mediaframework/dvr/sink/ -I$(RDK_BUILD_DIR)/mediaframework/qamsource/main/ -I$(RDK_BUILD_DIR)/mediaframework/init/  -I$(RDK_BUILD_DIR)/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/lib/glib-2.0/include -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/glib-2.0 -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/gstreamer-0.10 -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/libxml2 -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/usr/include/ -I$(RDK_BUILD_DIR)/mediaframework/mediaplayersink/ -I$(RDK_BUILD_DIR)/mediaframework/osal/include/ -I$(RDK_BUILD_DIR)/mediaframework/osal/utils/inc/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/gstreamer-0.10/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/glib-2.0/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/gstreamer-0.10/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/lib/glib-2.0/include/ -I$(RDK_BUILD_DIR)mediaframework/dvr/common/dvrmgr -I$(RDK_BUILD_DIR)/mediaframework/dvr/common/dvrmgr/soc/intel/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/usr/local/include/directfb/fusion -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/usr/local/include/directfb/ -I$(RDK_BUILD_DIR)/thirdparty/tinyxml

LDOPTS    :=    -L $(IMAGE_PATH)/mnt/nfs/bin/target-snmp/lib      \
                -L $(IMAGE_PATH)/lib \
                -L $(IMAGE_PATH)/usr/local/lib \
                -L${IMAGE_PATH}/lib/glib-2.0 \
                -L$(IMAGE_PATH)/usr/lib \
                -L $(IMAGE_PATH)/mnt/nfs/lib \
                -L $(IMAGE_PATH)/mnt/nfs/bin \
                -ldvrmgr -ltinyxml -l:libuuid.so.1 -l:libcrypto.so.0.9.8 -lTasseograph -l:libssl.so.0.9.8 -lfwloader -l:libreadline.so.6 -l:libnetsnmp.so.15 -l:libnetsnmpagent.so.15 -l:libnetsnmphelpers.so.15 -lpodmgr -lsysResource -lsectionfilter -linbsimanager -linbsectionfilter -lqamsrc -l:libssl.so.0.9.8 -l:libhistory.so.6 -l:libgstreamer-0.10.so.0 -l:libgio-2.0.so.0 -lglib-2.0 -llog4c -l:libgobject-2.0.so.0 -lmspod_pal -linit -lrdkloggers -lrdklogger

SOURCES   := $(RDK_BUILD_DIR)/mediaframework/core/rmfbase.cpp \
	     $(RDK_BUILD_DIR)/mediaframework/mediaplayersink/mediaplayersink.cpp \
             $(RDK_BUILD_DIR)/mediaframework/hnsource/hnsource.cpp

CFLAGS += -g -Wall -Wno-format -Wunused -DUSE_CC_GETTIMEOFDAY -DRMF_OSAL_FEATURE_IPV6 -DRMF_OSAL_LITTLE_ENDIAN  -DXONE_STB -DUSE_HW_DEMUX -DUSE_QAMSRC -DUSE_TRANSCODEFILTER -DUSE_FRONTPANEL -DUSE_DTCP -DUSE_HNSINK -DUSE_HNSRC -DUSE_DVR -DUSE_VODSRC -DUSE_MEDIAPLAYERSINK -DSRC_INIT_IN_CONSTRUCTOR -DRMF_STREAMER -DENABLE_AUTODISCOVERY_FOR_VOD   -DQAMSRC_FACTORY -DQAMSRC_PMTBUFFER_PROPERTY -DRECORDER_SUPPORT -DTEST_WITH_PODMGR -DIPPV_CLIENT_ENABLED -DUSE_POD_IPC -DOOBSI_SUPPORT -DDEBUG_CONF_FILE="\"debug.ini\"" -DENV_CONF_FILE="\"rmfconfig.ini\""
endif

INCLUDES  +=    -I./include \
                -I../agent/include \
                -I$(PLATFORM_SDK)/include \
                -I$(JSONRPC_PATH)/include \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH)
               		
LIBOPTS   := -shared

CPP	  := g++
CC        := gcc

LDOPTS    +=    -L $(IMAGE_PATH)/usr/local/lib 

#LIBDIR    := ../../$(VERSION)/libs
#TARGETDIR := ../../$(VERSION)/bin
LIBMEDIASTREAMER	  := libmediastreamerstub.so	
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBMEDIASTREAMER)
SOURCES   += $(SRC_DIR)*.cpp

DEVICES_DIR	:= ../../../../devices
SOURCE_APP:= $(SRC_DIR)*.c

ifeq ($(RDK_VERSION),RDK1DOT3)
PLAYER_APP:= $(SOURCE_APP)
PLAYER_EXE:= player
TARGET    := $(TARGEDIR)/$(PLAYER_EXE)
SCRIPTS :=scripts/runPlayer.sh scripts/alignRecList.sh
endif
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
	mkdir -p $(LIBDIR)
	$(CROSSCOMPILE)g++ $(OBJS) -fPIC $(LIBOPTS) -o $(LIBMEDIASTREAMER) $(LDOPTS)
	rm -rf $(OBJDIR)
	mv $(LIBMEDIASTREAMER) $(LIBDIR)
#
# Build everything
#
$(TARGET): $(PLAYER_APP)
	mkdir -p $(TARGETDIR)
	$(CC) $(PLAYERCFLAGS) $(PLAYER_APP) -o $(PLAYER_EXE) $(PLAYERLIBS)
	mv $(PLAYER_EXE) $(TARGETDIR)
	cp $(SCRIPTS) $(TARGETDIR)
ifeq ($(RDK_VERSION),RDK1DOT3)
build: $(TARGET)
endif
build: $(LIB) 

#
# Clean 
#
clean:
	rm -rf $(LIB)
	rm -rf $(TARGETDIR)/$(PLAYER_EXE)
	rm -rf $(TARGET)
