#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast. It may
#  not be used, copied, distributed or otherwise disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2014 Comcast. All rights reserved.
#  ============================================================================

######################################################################################################
# DEBUG_LEVEL shall be TRACE/ERROR/LOG                                                               #
# RDK_VERSION shall be RDK1DOT2/RDK1DOT3/RDK2DOT0 based on the RDK version in the target box         #
# RDK_BUILD_DIR is the location where RDK source code is located                                     #
# COMPILER :Specify the compiler excluded gcc,For ex: i686-cm-linux-                                 #
# TARGETDIR :specify the folder where bianries has to be copied                                      #
# LIBDIR :specify the folder where libs has to copied                                                #
# TOOLCHAIN_DIR :Specify the toolchain folder path												     #
######################################################################################################
DEBUG_LEVEL=TRACE
#RDK_BUILD_DIR=
#TOOLCHAIN_DIR=
#COMPILER=
#RDK_VERSION=
#TARGETDIR=
#LIBDIR=
##############################Uncomment the following the following parameters##########################################
#CROSSCOMPILE=$(TOOLCHAIN_DIR)/$(COMPILER)
#RDK_PROJECT_ROOT_PATH=$(RDK_BUILD_DIR)
#JSONRPC_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/jsonrpc
#JSONCPP_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/jsoncpp
#CURL_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/curl/include
#TDK_BIN_PATH=$(TARGETDIR)
##############################Uncomment the following parameters in case of Gateway######################################
#CURL_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/curl/include
#ROOTFS_INCLUDE=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/usr/include/
###############################Uncomment the following parameters in case of client#########################################
#PLATFORM_SDK=(Export the sdk path)
#CURL_PATH=$(PLATFORM_SDK)/include
#ROOTFS_INCLUDE=$(PLATFORM_SDK)/include
