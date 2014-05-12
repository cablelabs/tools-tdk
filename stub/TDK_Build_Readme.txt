+---------------------------------------------------------------+
|Build and deployment instructions for RDK Test Agent and Stubs |
|																|
+---------------------------------------------------------------+

---------------------------------------------------------------------
Building and Deploying the TDK Agent and stubs can be doable by 2 ways.
---------------------------------------------------------------------

1.TDK is integrated with RDK Build framework. so it can be build using RDK Build scripts itself.
	i)While building the RDK image using rdk_build.sh ,use "--tdk-options="--enable""to enable the TDK to build along with RDK.
	For Example:
		   ./rdk_build --build-type hybrid --tdk-options="--enable"
	
        As far as now,TDK is integrated with hybrid and default build types of X1.TDK is integrated with xi3 default build type.

	ii)TDK has two dependent opensource components like jsonrpc and jsoncpp.So Building those two components are part of open source build script(build/components/opensource/rdk_build.sh).
	iii)On TDK integrated image,TDK folder will be present under the /opt/
	iv)Starting tdk agent is added on the sysint scripts , so it will automatically triggered on the background during boot-up.

2.TDK and Opensource components has to be build with out using rdk build framework.To do achive that , please go with following instrctions.

Pre-requisites
==============
1. RDK build environment should be present ,RDK should be built and SDK dir should be present.
						
		                      	     	        ===============
							   SECTION I
							===============
Setting the Build work space:
=============================
1.Create one local setup folder "tdkbuildenv"
	i)mkdir tdkbuildenv
	ii)cd tdkbuildenv
	iii)Exporting RDK_PROJECT_ROOT_PATH to create shared libraries in to it
		export RDK_PROJECT_ROOT_PATH=$PWD

Building Opensource components jsoncpp & jsonrpc:
=================================================
1.Create a folder for open source building and check out the jsoncpp and jsonrpc in to it...
	i)mkdir opensrc
	ii)cd opensrc
	For Gateway :
	iii)svn co https://svn5.teamccp.com/svn/rdk/components/opensource/jsonrpc/generic/trunk opensource/src/jsonrpc
	iv)svn co https://svn5.teamccp.com/svn/rdk/components/opensource/jsoncpp/generic/trunk  opensource/src/jsoncpp
	v) svn co https://svn5.teamccp.com/svn/rdk/components/opensource/curl/generic/trunk opensource/src/curl
	For Client :
	iii)svn co https://svn5.teamccp.com/svn/rdk/components/opensource/jsonrpc/generic/trunk opensource/jsonrpc
	iv)svn co https://svn5.teamccp.com/svn/rdk/components/opensource/jsoncpp/generic/trunk  opensource/jsoncpp
2.Export the following varibles as per your local setup.
	i)Export the cross toolchain 
	For example:
		 export CC=/home/XG1/trunk/sdk/toolchain/staging_dir/bin/i686-cm-linux-gcc
	For Gateway:	 
		ii)Export the APP_PATH till curl folder
		For example:
			export APP_PATH=~opensource/src/curl/
	For Client:
		ii)Export the APP_PATH to sdk path without including include folder
		For example:
			export APP_PATH=/home/XI3/trunk/workXI3/Refsw/AppLibs/target/97428b0.mipsel-linux.release/usr/local/
		
	iii)Export the LDFLAGS to find the libcurl shared library
	For example:
		export LDFLAGS="-L /home/XG1/trunk/sdk/fsroot/ramdisk/usr/local/lib/"
	For Client:
		export LDFLAGS="-L /home/XI3/trunk/workXI3/Refsw/AppLibs/target/97428b0.mipsel-linux.release/usr/local/lib/"
		 
3.Move to the Particular opensource folder and do make
	i)cd ~/opensource/src/jsoncpp
	ii)make
	iii)cd ~/opensource/src/jsonrpc
	iv)make

4.Accoring to this , jsoncpp and jsonrpc shared libraries will be created under ~tdkbuildenv/opensource/lib


Building TDK Agent and Test stubs:
=================================
1.Downloading the tdk folder and device specific tdk folder
	i)cd tdkbuildenv
	ii)svn co https://svn5.teamccp.com/svn/rdk/components/generic/tdk/generic/trunk/stub  tdk 
For X1:	
	iii)svn co https://svn5.teamccp.com/svn/rdk/components/generic/tdk/devices/pace/pace_x1/trunk/stub  tdk/platform
For Xi3:
	iv)iii)svn co https://svn5.teamccp.com/svn/rdk/components/generic/tdk/devices/pace/pace_xi3/trunk/stub  tdk/platform

2.Add the values in to def.inc for the following parameters.
	RDK_BUILD_DIR=(Specify the RDK root path on the local machine)
	TOOLCHAIN_DIR=(Specify the toolchain folder path)
        COMPILER=(Specify the compiler excluded gcc,For ex: i686-cm-linux-)
	RDK_VERSION=(RDK1DOT3 or RDK2DOT0,but image should be same as that of mentioned version)
	TARGETDIR=(specify the folder where bianries has to be copied)
	LIBDIR=(specify the folder where libs has to copied)
	ROOTFS_INCLUDE=(Specify the root file system include path for ex: $RDK_BUILD_DIR/sdk/toolchain/staging_dir/usr/include/)
Uncomment the following the following parameters
	CROSSCOMPILE=$(TOOLCHAIN_DIR)/$(COMPILER)
	RDK_PROJECT_ROOT_PATH=$(RDK_BUILD_DIR)
	JSONRPC_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/jsonrpc
	JSONCPP_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/jsoncpp
	CURL_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/curl/include
	TDK_BIN_PATH=$(TARGETDIR)
Uncomment the following parameters in case of Gateway
	CURL_PATH=$(RDK_PROJECT_ROOT_PATH)/opensource/src/curl/include
	ROOTFS_INCLUDE=$RDK_BUILD_DIR/sdk/toolchain/staging_dir/usr/include/
Uncomment the following parameters in case of client
	PLATFORM_SDK=(Export the sdk path)
	CURL_PATH=$(PLATFORM_SDK)/include
	ROOTFS_INCLUDE=$(PLATFORM_SDK)/include

3.Navigate to platform folder under tdk
	i)cd tdkbuildenv/tdk/platform
	ii)make
		
 Note : All the stubs and agent will be build by this. The stubs and agent can be build independantly also by using the same Makefile.
  by using following commands. 

	make agent
	make IARMBUS_stub
	make MediaStreamer_stub
	make Mediaframework_stub
	make OpenSourceComponent_Stub
	make RDKLogger_stub
	make SM_stub
	make e2e_rmf_stub
	make rmfApp_stub