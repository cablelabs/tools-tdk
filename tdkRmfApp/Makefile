include ../def.inc
default: build

#
# Source files
#
SRC_DIR   := ./
OBJDIR    := ./obj
COPTS     := -c
LDOPTS    += -L $(IMAGE_PATH)/usr/local/lib/ 
CFLAGS += -DRMF_OSAL_LITTLE_ENDIAN
CFLAGS += -g -Wall -DGCC4_XXX -DBUILD_DVRSOURCE -DRMF_STREAMER -DENABLE_DVRSRC_MPSINK

INCLUDES  +=    -I$(RDK_BUILD_DIR)/mediaframework/core/  \
		-I$(RDK_BUILD_DIR)/opensource/src/gstreamer \
		-I$(RDK_BUILD_DIR)/opensource/src/glib/glib/ \
		-I$(RDK_BUILD_DIR)/opensource/src/glib/ \
		-I$(RDK_BUILD_DIR)/opensource/gstreamer/gstreamer-0.10.34 \
		-I$(RDK_BUILD_DIR)/opensource/src/libxml2/include/ \
		-I$(RDK_BUILD_DIR)/opensource/src/glib/gmodule \
		-I$(RDK_BUILD_DIR)/mediaframework/osal/utils/inc/ \
		-I$(RDK_BUILD_DIR)/mediaframework/hnsource/ \
		-I$(RDK_BUILD_DIR)/mediaframework/dvr/source/ \
		-I$(RDK_BUILD_DIR)/mediaframework/dvr/common/tasseograph \
		-I$(RDK_BUILD_DIR)/mediaframework/dvr/common/dvrmgr/ \
		-I$(RDK_BUILD_DIR)/mediaframework/cfg \
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
              -L $(RDK_BUILD_DIR)/opensource/openssl \
              -ldvrmgr -ltinyxml -lIARMBus -lTasseograph -lpodmgr -ltrm -ljansson -ltrh -lcanh -ldvrsink  -lrdkloggers -lrmfbase -lglib-2.0  -llog4c -lqamsrc -linbsimanager -lsectionfilter -linbsectionfilter -lhnsource -lgstreamer-0.10 -lgobject-2.0 -lgstbase-0.10 -ldvrmgrsoc -l:librmfosal.so.0 -l:librmfosalutils.so.0 -lmediaplayersink -ldvrmgrsoc -loobsectionfilter -lpodserver -loobsimanager -loobsicache -l:libippvsource.so.0 



BOPTS   := -shared

CC        := g++
LIBMF     := tdkRmfApp
#
# Library built by this makefile
#
LIB        = $(TARGETDIR)/$(LIBMF)

SOURCES   += $(SRC_DIR)*.cpp
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
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBMF) $(LDOPTS) 
	rm -rf $(OBJDIR)
	mv $(LIBMF) $(LIB)
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

