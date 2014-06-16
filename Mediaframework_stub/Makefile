
include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := src/
OBJDIR    := ./obj
COPTS     := -c

LDOPTS    += -L $(IMAGE_PATH)/usr/local/lib/ 

CFLAGS += -g -Wall -DGCC4_XXX -DBUILD_DVRSOURCE -DRMF_STREAMER -DENABLE_DVRSRC_MPSINK

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
		-I$(RDK_BUILD_DIR)/mediaframework/core/  \
		-I$(RDK_BUILD_DIR)/opensource/src/gstreamer \
		-I$(RDK_BUILD_DIR)/opensource/src/glib/glib/ \
		-I$(RDK_BUILD_DIR)/opensource/src/glib/ \
		-I$(RDK_BUILD_DIR)/opensource/gstreamer/gstreamer-0.10.34 \
		-I$(RDK_BUILD_DIR)/opensource/src/libxml2/include/ \
		-I$(RDK_BUILD_DIR)/opensource/src/glib/gmodule \
		\
		-I$(RDK_BUILD_DIR)/mediaframework/osal/utils/inc/ \
		\
		-I$(RDK_BUILD_DIR)/mediaframework/hnsource/ \
		-I$(RDK_BUILD_DIR)/mediaframework/hnsink/ \
		-I$(RDK_BUILD_DIR)/mediaframework/dvr/source/ \
		-I$(RDK_BUILD_DIR)/mediaframework/dvr/common/tasseograph \
		-I$(RDK_BUILD_DIR)/mediaframework/dvr/common/dvrmgr/ \
		-I$(RDK_BUILD_DIR)/rdklogger/include/ \
		-I$(RDK_BUILD_DIR)/mediaframework/dvr/sink/ \
		-I$(RDK_BUILD_DIR)/mediaframework/qamsource/main/ \
		-I$(RDK_BUILD_DIR)/mediaframework/init/ \
		-I$(PLATFORM_SDK)/include \
		-I${PLATFORM_SDK}/lib/glib-2.0/include \
            	-I${PLATFORM_SDK}/include/glib-2.0 \
            	-I${PLATFORM_SDK}/include/gstreamer-0.10 \
            	-I$(PLATFORM_SDK)/include \
            	-I$(PLATFORM_SDK)/usr/local/include \
            	-I$(PLATFORM_SDK)/usr/include \
            	-I$(PLATFORM_SDK)/include/linux_user \
            	-I${PLATFORM_SDK}/include/libxml2\
                -I$(JSONRPC_PATH)/include \
                -I$(JSONCPP_PATH)/include \
                -I$(CURL_PATH)


LDOPTS    +=  -L $(IMAGE_PATH)/usr/local/lib \
              -L $(IMAGE_PATH)/lib \
              -L $(IMAGE_PATH)/mnt/nfs/lib \
              -L $(IMAGE_PATH)/mnt/nfs/bin/ \
		-L $(IMAGE_PATH)/usr/lib \
              -L $(IMAGE_PATH)/mnt/nfs/bin/target-snmp/lib \
               -ldvrmgr -ltinyxml -l:libuuid.so.1 -l:libcrypto.so.0.9.8 -lTasseograph -l:libssl.so.0.9.8 -lfwloader -l:libreadline.so.6 -l:libnetsnmp.so.15 -l:libnetsnmpagent.so.15 -l:libnetsnmphelpers.so.15 -lpodmgr -lsysResource -lsectionfilter -linbsimanager -linbsectionfilter -l:libssl.so.0.9.8 -l:libhistory.so.6 -l:libgstreamer-0.10.so.0 -l:libgio-2.0.so.0 -lglib-2.0 -llog4c -l:libgobject-2.0.so.0 -lmspod_pal -linit -lrdkloggers -lrdklogger -lqamsrc -l:libncurses.so.5 -l:libdvrmgrsoc.so.0.0.0 -l:libgstbase-0.10.so -lismd_demux -lhnsource -ldvrsink -lhnsink -lcanh -ltrh -ltrm -lIARMBus -lDtcpMgr -lrmfbase


BOPTS   := -shared

CC        := g++
LIBMF     := libmediaframeworkstub.so
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBMF)
SOURCES   += $(SRC_DIR)*.cpp	\
		$(RDK_BUILD_DIR)/mediaframework/mediaplayersink/mediaplayersink.cpp	\
		$(RDK_BUILD_DIR)/mediaframework/dvr/source/DVRSource.cpp
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
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -shared -o $(LIBMF) $(LDOPTS) 
	rm -rf $(OBJDIR)
	mkdir -p $(TDK_BIN_PATH)/scripts
	cp -r ../platform/Mediaframework_stub/scripts/* $(TDK_BIN_PATH)/scripts
	mv $(LIBMF) $(LIBDIR)
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

