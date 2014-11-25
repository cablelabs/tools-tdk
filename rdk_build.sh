#!/bin/bash
#
# ============================================================================
# COMCAST C O N F I D E N T I A L AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of Comcast.  It may
# not be used, copied, distributed or otherwise  disclosed in whole or in part
# without the express written permission of Comcast.
# ============================================================================
# Copyright (c) 2014 Comcast. All rights reserved.
# ============================================================================
#

#######################################
#
# Build Framework standard script for
#
#RDKTDK Test tool

# use -e to fail on any shell issue
# -e is the requirement from Build Framework
########################################
set -x


# default PATHs - use `man readlink` for more info
# the path to combined build
export RDK_PROJECT_ROOT_PATH=${RDK_PROJECT_ROOT_PATH-`readlink -m ..`}
export COMBINED_ROOT=$RDK_PROJECT_ROOT_PATH
echo "path":$RDK_PROJECT_ROOT_PATH
# path to build script (this script)
export RDK_SCRIPTS_PATH=${RDK_SCRIPTS_PATH-`readlink -m $0 | xargs dirname`}

# path to components sources and target
export RDK_SOURCE_PATH=${RDK_SOURCE_PATH-`readlink -m .`}
export RDK_TARGET_PATH=${RDK_TARGET_PATH-$RDK_SOURCE_PATH}

# fsroot and toolchain (valid for all devices)
export RDK_FSROOT_PATH=${RDK_FSROOT_PATH-`readlink -m $RDK_PROJECT_ROOT_PATH/sdk/fsroot/ramdisk`}
export RDK_TOOLCHAIN_PATH=${RDK_TOOLCHAIN_PATH-`readlink -m $RDK_PROJECT_ROOT_PATH/sdk/toolchain/staging_dir`}

# default component name
export RDK_COMPONENT_NAME=${RDK_COMPONENT_NAME-`basename $RDK_SOURCE_PATH`}

# parse arguments
INITIAL_ARGS=$@

ENABLE_TDK=0
function usage()
{
    set +x
    echo "Usage: `basename $0` [-h|--help] [-v|--verbose] [iaction]"
    echo "    -h    --help                  : this help"
    echo "    -v    --verbose               : verbose output"
    echo
    echo "Supported actions:"
    echo "      configure, clean, build (DEFAULT), rebuild, install"
}

echo "Option received : $1"
# options may be followed by one colon to indicate they have a required argument
if ! GETOPT=$(getopt -n "build.sh" -o hvp: -l help,enable,verbose: -- "$@")
then
    usage
    exit 1
fi

eval set -- "$GETOPT"

while true; do
  case "$1" in
    -h | --help ) usage; exit 0 ;;
    -v | --verbose ) set -x ;;
    --enable ) ENABLE_TDK=1 ;;
    -- ) shift; break;;
    * ) break;;
  esac
  shift
done

ARGS=$@

#source ${RDK_PROJECT_ROOT_PATH}/build_scripts/setBCMenv.sh

#COMPILER=mipsel-linux-
# component-specific vars
#export PATH=$PATH:$RDK_PROJECT_ROOT_PATH/tools/stbgcc-4.5.3-2.4/bin:$RDK_PROJECT_ROOT_PATH/sdk/toolchain/staging_dir
export TDK_PATH=$RDK_SOURCE_PATH
export RDK_BUILD_DIR=$RDK_SOURCE_PATH/../
export FSROOT=${RDK_FSROOT_PATH}
export TOOLCHAIN_DIR=${RDK_TOOLCHAIN_PATH}
export OPENSOURCE_PATH=$RDK_PROJECT_ROOT_PATH/opensource
#export RDK_PLATFORM_SOC=${RDK_PLATFORM_SOC-broadcom}
#export PLATFORM_SOC=$RDK_PLATFORM_SOC

if [ "x"$RDK_PLATFORM_SOC == "xintel" ]; then
	export TOOLCHAIN_DIR=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/bin
        export CROSS_COMPILE=i686-cm-linux-
	export ROOTFS_INCLUDE=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/usr/include/
	if [ "x"$BUILD_CONFIG == "x" ]; then
	  export RDK_VERSION=RDK1DOT3
	elif [ "x"$BUILD_CONFIG == "xhybrid" ]; then
	  export RDK_VERSION=RDK2DOT0
	fi
        export PLATFORM_SDK=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/
	export JSONRPC_PATH=$RDK_PROJECT_ROOT_PATH/opensource/src/jsonrpc
        export JSONCPP_PATH=$RDK_PROJECT_ROOT_PATH/opensource/src/jsoncpp
        export CURL_PATH=$RDK_PROJECT_ROOT_PATH/opensource/src/curl/include
        COMPILER=i686-cm-linux-
	export CROSS_TOOLCHAIN=$TOOLCHAIN_DIR
	export CROSS_COMPILE=$CROSS_TOOLCHAIN/$COMPILER
elif [ "x"$RDK_PLATFORM_SOC = "xbroadcom" ]; then
	export WORK_DIR=$RDK_PROJECT_ROOT_PATH/work${RDK_PLATFORM_DEVICE^^}
	source ${RDK_PROJECT_ROOT_PATH}/build_scripts/setBCMenv.sh
        echo $BCMAPP 
	export PLATFORM_SDK=$BCMAPP
	export RDK_VERSION=RDK2DOT0
	COMPILER=mipsel-linux-
	export JSONRPC_PATH=$RDK_PROJECT_ROOT_PATH/opensource/jsonrpc/
	export JSONCPP_PATH=$RDK_PROJECT_ROOT_PATH/opensource/jsoncpp/
	export CROSS_TOOLCHAIN=$TOOLCHAIN_DIR
	export CROSS_COMPILE=$COMPILER
	export ROOTFS_INCLUDE=$PLATFORM_SDK/include/
	if [ "x"$BUILD_CONFIG == "xhybrid" ]; then
                export WORK_DIR=${RDK_PROJECT_ROOT_PATH}/work${RDK_PLATFORM_DEVICE^^}
                export IMAGE_PATH=${RDK_PROJECT_ROOT_PATH}/work${RDK_PLATFORM_DEVICE^^}/rootfs/
                export CURL_PATH=$RDK_PROJECT_ROOT_PATH/opensource/include
		export TOOLCHAIN_DIR=$BCM_TOOLCHAIN/bin/
        else
                export CURL_PATH=$PLATFORM_SDK/include/curl
        fi
fi
#export PLATFORM_SOC=$TDK_PLATFORM
#export TOOLCHAIN_DIR=$RDK_BUILD_PATH/sdk/toolchain/staging_dir
#export CROSS_TOOLCHAIN=$TOOLCHAIN_DIR
#export CROSS_COMPILE=$COMPILER
export CROSSCOMPILE=$CROSS_COMPILE
echo $CROSSCOMPILE
export TDK_LIB_PATH=$TDK_PATH/build/libs
export TDK_BIN_PATH=$TDK_PATH/build/bin

export LIBDIR=$TDK_LIB_PATH
export TARGETDIR=$TDK_BIN_PATH
TDK_PATH=$TDK_PATH/platform/
# functional modules

function configure()
{
    true #use this function to perform any pre-build configuration
}

function clean()
{
    cd $TDK_PATH
    make clean
    true #use this function to provide instructions to clean workspace
}

function build()
{
    cd $TDK_PATH
    make
}

function rebuild()
{
    clean
    build
}

function install()
{
    true	
}


# run the logic

#these args are what left untouched after parse_args
HIT=false
if [ "$ENABLE_TDK" == 1 ]; then
       touch $RDK_PROJECT_ROOT_PATH/build/packager_scripts/enable_tdk   
	for i in "$ARGS"; do
    		case $i in
        		configure)  HIT=true; configure ;;
        		clean)      HIT=true; clean ;;
        		build)      HIT=true; build ;;
        		rebuild)    HIT=true; rebuild ;;
        		install)    HIT=true; install ;;
        		*)
            		#skip unknown
        		;;
    		esac
	done

# if not HIT do build by default
	if ! $HIT; then
  		build
	fi
else
echo "##TDK OPTION is not set to build the TDK##"
echo "##Use --tdk-option="enable" to build the TDK ##"
fi
