#Gstreamer tests

include ../../def.inc

default: build

#debug log level
ifeq ($(DEBUG_LEVEL),TRACE)
COPTS     := -DDEBUG_LEVEL_TRACE
endif
ifeq ($(DEBUG_LEVEL),LOG)
COPTS     := -DDEBUG_LEVEL_LOG
endif
ifeq ($(DEBUG_LEVEL),ERROR)
COPTS     := -DDEBUG_LEVEL_ERROR
endif

ifeq ($(RDK_VERSION),RDK2DOT0)
COPTS     += -DRDK_BR_2DOT0
VERSION    = br2.0
endif

ifeq ($(RDK_VERSION),RDK1DOT3)
COPTS     += -DRDK_BR_1DOT3
VERSION    = br1.3
endif

ifeq ($(RDK_VERSION),RDK1DOT2)
COPTS     += -DRDK_BR_1DOT2
VERSION    = br1.2
endif

TDK_ROOT = $(RDK_BUILD_DIR)/tdk
# Config for this build
CC  := $(CROSSCOMPILE)gcc
INCLUDES  := -I$(TDK_ROOT)/stub/twc_tdkcommon/include -I$(TDKENV_RDK_ROOTFS_USRPATH)/include/gstreamer-0.10 -I$(TDKENV_RDK_ROOTFS_USRPATH)/include/glib-2.0 -I$(TDKENV_RDK_ROOTFS_USRPATH)/lib/glib-2.0/include -I$(RDK_ROOT)/sdk//src/target/src/sd/celf/libs/comps/mediaframeworks/gstplayermiddle/inc/ -I$(RDK_ROOT)/sdk//src/target/src/inc/ -I$(_TMTGTBUILDROOT)/comps/generic_apps/usr/include/gstreamer-0.10/gst -I$(_TMTGTBUILDROOT)/comps/generic_apps/usr/include/gstreamer-0.10/ -I$(_TMTGTBUILDROOT)/comps/generic_apps/usr/include/glib-2.0 -I$(_TMTGTBUILDROOT)/comps/generic_apps/usr/lib/glib-2.0/include -I$(_TMTGTBUILDROOT)/comps/generic_apps/usr/include/libsoup-2.4 -I$(_TMROOT)/sd/celf/libs/comps/omx/inc/khronos -I$(_TMROOT)/sd/celf/libs/comps/omx/inc -I$(ROOTFS_INCLUDE)/gstreamer-0.10 -I$(ROOTFS_INCLUDE)/glib-2.0 -I$(TDK_ROOT)/twc_tdkcommon/include 

LDOPTS   = -lgstcheck-0.10 -lffi -lintl -lgstreamer-0.10 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lglib-2.0 -lgstplayback -lgstbase-0.10 -lgstcontroller-0.10 -lgstvideo-0.10 -lgstpbutils-0.10 -lgstreamer-0.10 -lgstapp-0.10 -lpthread 
PKG_CONFIG_PATH=$(TDKENV_RDK_ROOTFS_USRPATH)/lib/pkgconfig pkg-config --cflags --libs gstreamer-0.10 -lstdc++
LDFLAGS = -L$(TDKENV_RDK_ROOTFS_USRPATH)/lib -L$(TDKENV_TDK_ROOT)/stub/$(PLATFORM)/$(VENDOR)/$(VERSION)/libs/ -L$(MODULE_INSTALL_LOC)/appfs-hnav/appfs/lib/ -L$(MODULE_INSTALL_LOC)/lib/ -L$(TDK_ROOT)/$(VERSION)/libs/ -L$(TDK_ROOT)/build/libs/ -L$(IMAGE_PATH)/usr/local/lib


#Intermediate object file and source file to generate shared library
PLATFORM_SRC = $(TDK_ROOT)/twc_tdkcommon/src/platform.c
PLATFORM_OBJDIR	  := $(TDK_ROOT)/twc_tdkcommon/obj
SOURCES   := common/gstplayback.c
OBJDIR	  := ./obj
COPTS     := -c

HOSTED_TEST_SRCS :=  Gstreamer_Audio_Performance_On_New_Pipeline_HttpHosted.c  \
        Gstreamer_Audio_Performance_On_Same_Pipeline_HttpHosted.c   \
	Gstreamer_Video_Performance_On_Same_Pipeline_HttpHosted.c  \
	Gstreamer_Video_Performance_On_New_Pipeline_HttpHosted.c   \
	Gstreamer_Audio_Playback_HttpHosted.c \
	Gstreamer_Image_Playback_HttpHosted.c \
	Gstreamer_Video_Playback_HttpHosted.c \
	udp_aac_receiver.c   \
	udp_ac3_receiver.c   \
	udp_mp3_receiver.c   \
	udp_mp4_receiver.c   \
	perf_udp_mp4_receiver.c   \
	perf_udp_mp4_sender.c   \
	udp_aac_sender_hosted.c   \
	udp_ac3_sender_hosted.c   \
	udp_mp3_sender_hosted.c   \
	udp_mp4_sender_hosted.c 


#Library path

LIBOPTS   := -shared
LIBDIR    := $(TDK_ROOT)/build/libs/
LIBGSTREAMER	  := libgstplayback.so

# Library built by this makefile
#
LIB        = $(LIBDIR)/$(LIBGSTREAMER)

# Intermediate files
#
OBJS       =$(OBJDIR)/*.o
PLATFORM_OBJS       =$(PLATFORM_OBJDIR)/*.o

#
# Compile source files into intermediate files
#
$(OBJS): $(SOURCES) 
	mkdir -p $(TARGETDIR)/opensourcecomptest/gst-plugin-custom-test
	mkdir -p $(TARGETDIR)/opensourcecomptest/resources
	mkdir -p $(OBJDIR)
	$(CC) -Wall $(INCLUDES) -fPIC $(COPTS) $^
	mv *.o $(OBJDIR)

$(PLATFORM_OBJS): $(PLATFORM_SRC) 
	mkdir -p $(PLATFORM_OBJDIR)
	$(CC) -Wall $(INCLUDES) -fPIC $(COPTS) $(PLATFORM_SRC)
	mv *.o $(PLATFORM_OBJDIR)

#
# Build the library from intermediate files
#
commonlib: $(OBJS)
	mkdir -p $(LIBDIR) 
	$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(LIBGSTREAMER)
	mv $(LIBGSTREAMER) $(LIBDIR)
	mkdir -p $(TARGETDIR)
	rm -rf $(OBJDIR)

all: commonlib tests install

# Compile tests 
tests: $(PLATFORM_OBJS) $(patsubst %.c, %, $(HOSTED_TEST_SRCS)) 
%: %.c Makefile
	-$(CC) $(INCLUDES) $(PLATFORM_OBJS) -DSERVER_PATH='"${PUBLISHER_IP}"' $(LDOPTS) $(LDFLAGS) $< -o $@ -lm  

install:
	$(shell find . -type f ! -name "*.*" -perm -og+rx -exec mv -f {} $(TARGETDIR)/opensourcecomptest/gst-plugin-custom-test/. \;)
	cp -r $(TDK_ROOT)/gstreamerCustomTests/resources/urlCheck.sh  $(TARGETDIR)/opensourcecomptest/resources/
	

#
# build library and all files 
#
build: all

#
# Clean 
#
clean:
	@echo "Cleaning"
	@rm -rf $(OBJDIR)        
	@rm -rf $(PLATFORM_OBJDIR)      
	@rm -rf $(LIBDIR)/$(LIBGSTREAMER)
	@rm -rf *.so            
	@rm -rf *~
	find . -type f ! -name "*.*" -perm -og+rx -delete
	$(shell find $(TARGETDIR)/* -executable -delete)
