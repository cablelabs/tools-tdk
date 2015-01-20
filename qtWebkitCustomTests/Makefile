#make file for qtwebkit  tests

DEF_PATH   := ../
include $(DEF_PATH)/def.inc

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

#export $(RDK_BUILD_DIR)
# Config for this build
CC  := $(CROSSCOMPILE)g++
$(info $$CROSSCOMPILE is [${CROSSCOMPILE}])
$(info  $$CC is [${CC}])
$(info  $$RDK_BUILD_DIR is [${RDK_BUILD_DIR}])
INCLUDES  := -I$(TDKENV_RDK_ROOTFS_USRPATH)/include/gstreamer-0.10 -I$(TDKENV_RDK_ROOTFS_USRPATH)/include/glib-2.0 -I$(TDKENV_RDK_ROOTFS_USRPATH)/lib/glib-2.0/include 
LDOPTS    := -lgstcheck-0.10 -lgstreamer-0.10 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lglib-2.0 
PKG_CONFIG_PATH=$(TDKENV_RDK_ROOTFS_USRPATH)/lib/pkgconfig pkg-config --cflags --libs gstreamer-0.10
LDFLAGS = -L$(TDKENV_RDK_ROOTFS_USRPATH)/lib

QTWEBKIT_TARGETDIR:=$(TARGETDIR)/opensourcecomptest/webkit

#PLatform/Vendor/RDK Version Conditional config

LDOPTS   +=     $(LDOPTS) $(LDFLAGS)

all: 	
	mkdir -p $(QTWEBKIT_TARGETDIR)
	echo "make all - in webkit folder"
	./buildall.sh
	echo "buildall completed"
	./moveall.sh $(QTWEBKIT_TARGETDIR) 
	./cleanall.sh
	
install:
	mkdir -p $(QTWEBKIT_TARGETDIR)
	./moveall.sh $(QTWEBKIT_TARGETDIR) 
	echo "QtWebkit binary files moved to " $(QTWEBKIT_TARGETDIR)
#
# build all files 
#
build: all install
	echo "make build - in webkit folder"

#
# Clean 
#
clean:
	./cleanall.sh
#	echo "Cleaning"
#	@rm -rf *~
#	find . -type f ! -name "*.*" -perm -og+rx -delete
#	$(shell find $(QTWEBKIT_TARGETDIR)/* -executable -delete)
