##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
#
# Master Makefile : To build all the binaries and component libraries
# Usage : make all
#         make <COMPONENT NAME>
#         make clean 
#         make clean-<COMPONENT NAME>
#

DEF_PATH   := ../
include $(DEF_PATH)/def.inc

#Exporting SCRIPT_PATH to copy the scripts to target directory.
CURRENT_PATH    :=$(PWD)
export SCRIPTS_PATH =$(CURRENT_PATH)/OpenSourceComponent_Stub/script
export PLAYER_SRC_PATH=$(CURRENT_PATH)/MediaStreamer_stub/
export T2P_SCRIPT_PATH=$(CURRENT_PATH)/TDKIntegration_Stub/scripts
export IMAGE_PATH=$(RDK_BUILD_DIR)/sdk/fsroot/ramdisk/
export SCRIPTS := $(CURRENT_PATH)/agent/scripts/StartTDK.sh scripts/configure_iptables.sh scripts/flush_iptables.sh scripts/get_moca_devices.sh  scripts/runSysStat.sh $(CURRENT_PATH)/agent/scripts/StopTDK.sh
export CROSSCOMPILE =$(CROSS_COMPILE)

SUBDIRS := agent MediaStreamer_stub OpenSourceComponent_Stub SM_stub IARMBUS_stub DS_stub ClosedCaption_stub RDKLogger_stub TDKIntegration_Stub TRM_stub


ifeq ($(RDK_VERSION),RDK2DOT0)
SUBDIRS += rmfApp_stub  Recorder_stub Mediaframework_stub tdkRmfApp
DS_COPTS +=-DIARMBUS
SM_LDOPTS +=-l:libpcre16.so.0
endif

ifeq ($(DBUS),y)
IARMBUS_LDOPTS  += -ldirect -lfusion -ldbus-1 
DS_LDOPTS        += -lIARMBus -ldirect -lfusion -ldbus-1
else
IARMBUS_LDOPTS  += -l:libdirect-1.4.so.0 -l:libfusiondale-0.8.so.1
DS_LDOPTS        += -lIARMBus -l:libfusiondale-0.8.so.1 -l:libz.so.1 -lglib-2.0 -l:libdirect-1.4.so.0
endif

ifeq ($(RDK_VERSION),$(filter $(RDK_VERSION),RDK1DOT3 RDK2DOT0 ))
SM_LDOPTS += -l:libQt5WebKitWidgets.so.5 -l:libQt5Sql.so.5 -l:libQt5OpenGL.so.5 -l:libQt5WebKit.so.5  -l:libQt5Widgets.so.5 -l:libQt5Network.so.5 -l:libQt5Gui.so.5 -l:libQt5Core.so.5 -l:libopus.so.0 -l:libexpat.so.1 -l:libicui18n.so.48 -l:libicuuc.so.48 -l:libicudata.so.48 -lglib-2.0
endif

CLEANDIRS = $(SUBDIRS:%=clean-%)

	
all:$(SUBDIRS)  
	@echo "BUILD SUCCESS"
	@echo $(SUBDIR[1])

$(SUBDIRS):
	@echo "BUILDING" $@
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@
agent:
	@$(eval LDOPTS =-lrdkCCReader -lismd_bufmon -lismd_viddec -lismd_core -lrdkCCGfx -lrdkCCManager -l:libdirectfb-1.4.so.0.3.0 -l:libcurl.so.4 -llog4c)
	@$(eval COPTS = -DPORT_FORWARD)
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@
DS_stub:
	@$(eval LDOPTS = $(DS_LDOPTS))
	@$(eval COPTS = $(DS_COPTS))
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@

ClosedCaption_stub:
	@$(eval INCLUDES = -I $(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/usr/local/include/directfb -I $(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include -I $(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/usr/local/include/directfb/direct -I $(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/usr/local/include/directfb/fusion)
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@

IARMBUS_stub:
	@$(eval LDOPTS  = $(IARMBUS_LDOPTS))
	@$(eval INCLUDES= -I$(RDK_BUILD_DIR)/iarmmgrs/generic/hal/include/)
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@

Mediaframework_stub:
	@$(eval CFLAGS += -DRMF_OSAL_LITTLE_ENDIAN)
	@$(eval INCLUDES  += -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/lib/glib-2.0/include/ -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/mediaplayersink/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/gstreamer-0.10/ -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/hnsource/ -I$(RDK_BUILD_DIR)/mediaframework/osal/include/ -I$(RDK_BUILD_DIR)/mediaframework/dvr/common/dvrmgr/soc/intel/ -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/mediaplayersink/)
	@$(eval LDOPTS = -lPaceFrontEnd -lPaceTuner -lPacePosixApi -lsec -lPaceDsgIf)
	@$(eval SOURCES= $(RDK_BUILD_DIR)/mediaframework/core/rmfbase.cpp)
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@

tdkRmfApp:
	@$(eval CFLAGS += -DRMF_OSAL_LITTLE_ENDIAN)
	@$(eval INCLUDES  += -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/lib/glib-2.0/include/ -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/mediaplayersink/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/gstreamer-0.10/ -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/hnsource/ -I$(RDK_BUILD_DIR)/mediaframework/osal/include/ -I$(RDK_BUILD_DIR)/mediaframework/dvr/common/dvrmgr/soc/intel/ -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/mediaplayersink/)
	@$(eval LDOPTS = -lPaceFrontEnd -lPaceTuner -lPacePosixApi -lsec -lPaceDsgIf -lPaceMfrApi -lPaceEcmApi -lPaceNvramApi)
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@

MediaStreamer_stub:
ifeq ($(RDK_VERSION),RDK2DOT0)
	@$(eval CFLAGS += -DRMF_OSAL_LITTLE_ENDIAN)
	@$(eval INCLUDES  += -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/lib/glib-2.0/include/  -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/mediaplayersink/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/gstreamer-0.10/ -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/hnsource/ -I$(RDK_BUILD_DIR)/mediaframework/osal/include/ -I$(RDK_BUILD_DIR)/mediaframework/dvr/common/dvrmgr/soc/intel/ -I$(RDK_BUILD_DIR)/mediaframework/platform/soc/mediaplayersink/)
endif
ifeq ($(RDK_VERSION),RDK1DOT3)
	mkdir -p $(TDK_BIN_PATH)/scripts
	cp -r $(CURRENT_PATH)/MediaStreamer_stub/scripts/* $(TDK_BIN_PATH)/scripts
endif
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@
SM_stub:
	@$(eval LDOPTS =$(SM_LDOPTS))
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@
TDKIntegration_Stub:
	@$(eval CFLAGS= -DHYBRID)
ifeq ($(RDK_VERSION),RDK2DOT0)
	@$(eval CFLAGS+=  -DGCC4_XXX -DRMFAGENT -DRMF_OSAL_LITTLE_ENDIAN -DENABLE_HYBRID_CODECOMPILE) 
	@$(eval INCLUDES  += -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/gstreamer-0.10/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/glib-2.0/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/gstreamer-0.10/ -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/lib/glib-2.0/include/ -I$(RDK_BUILD_DIR)/mediaframework/core/ -I$(RDK_BUILD_DIR)/mediaframework/mediaplayersink/ -I$(RDK_BUILD_DIR)/mediaframework/hnsource/ -I$(RDK_BUILD_DIR)/mediaframework/qamsource/main/ -I$(RDK_BUILD_DIR)/mediaframework/init/ -I$(RDK_BUILD_DIR)/mediaframework/osal/include/ -I$(PLATFORM_SDK)/lib/glib-2.0/include -I$(PLATFORM_SDK)/include/glib-2.0 -I$(PLATFORM_SDK)/include/gstreamer-0.10 -I$(PLATFORM_SDK)/usr/local/include  -I$(PLATFORM_SDK)/usr/include -I$(PLATFORM_SDK)/include/linux_user -I$(PLATFORM_SDK)/include/libxml2)
	@$(eval SOURCES= $(RDK_BUILD_DIR)/mediaframework/core/rmfbase.cpp $(RDK_BUILD_DIR)/mediaframework/mediaplayersink/mediaplayersink.cpp)
	@$(eval LDOPTS =  -L $(IMAGE_PATH)/mnt/nfs/lib -L $(IMAGE_PATH)/mnt/nfs/bin/ -L $(IMAGE_PATH)/mnt/nfs/bin/target-snmp/lib -ltinyxml -lgstapp-0.10 -lgobject-2.0 -lgstbase-0.10 -llog4c -lgmodule-2.0 -lgthread-2.0 -lglib-2.0 -lgstreamer-0.10 -luuid -ldvrmgr -lqamsrc -lhnsource -ltrm)
endif
ifeq ($(RDK_VERSION),RDK1DOT3)
	cp -r $(T2P_SCRIPT_PATH)/T2p* $(TDK_BIN_PATH)
endif
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@


RDKLogger_stub:
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@

rmfApp_stub:
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@

TRM_stub:
	@$(eval INCLUDES  = -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/lib/glib-2.0/include -I$(RDK_BUILD_DIR)/sdk/toolchain/staging_dir/include/glib-2.0 -I$(RDK_BUILD_DIR)/mediaframework/osal/include)
	@$(eval LDOPTS = -L$(IMAGE_PATH)/mnt/nfs/lib -L$(IMAGE_PATH)/mnt/nfs/bin -L$(IMAGE_PATH)/mnt/nfs/bin/target-snmp/lib -lgthread-2.0 -lglib-2.0 -luuid -losal)
	$(MAKE) -C $(DEF_PATH)/$@
	@echo "BUILD SUCCESS :" $@

export LDOPTS:=${LDOPTS}
export COPTS:=$(COPTS)
export CFLAGS:=$(CFLAGS)
export INCLUDES:=$(INCLUDES)
export SOURCES:=$(SOURCES)
export PLATFORM_SDK:=$(PLATFORM_SDK)

clean: $(CLEANDIRS)

$(CLEANDIRS): 
	@echo "CLEANING" $(@:clean-%=%)
	$(MAKE) -C $(DEF_PATH)/$(@:clean-%=%) clean

.PHONY: $(SUBDIRS)
.PHONY: $(CLEANDIRS)
