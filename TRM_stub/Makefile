CC      = g++
CFLAGS  = -Wall -g -DGCC4_XXX -Wno-format -Wunused -DUSE_CC_GETTIMEOFDAY -DRMF_OSAL_FEATURE_IPV6 -DRMF_OSAL_LITTLE_ENDIAN -DDEBUG_CONF_FILE="\"/etc/debug.ini\""

SRC_DIR = src
OBJ_DIR = ./
TRM_LIB = libtrmstub.so

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

OBJS       = $(OBJ_DIR)/TRMAgent.o $(OBJ_DIR)/TunerReservationHelper.o

INCLUDES+= -I./include \
	-I../agent/include \
	-I$(JSONRPC_PATH)/include \
	-I$(JSONCPP_PATH)/include \
	-I$(CURL_PATH)\
	-I$(CURL_PATH)/../ \
	-I$(RDK_BUILD_DIR)/opensource/include \
	-I$(RDK_BUILD_DIR)/opensource/include/uuid \
	-I$(RDK_BUILD_DIR)/rdklogger/include \
	-I$(RDK_BUILD_DIR)/trm/common/include

CFLAGS  += $(INCLUDES)

LDOPTS  += -L $(IMAGE_PATH)/usr/local/lib \
           -L $(IMAGE_PATH)/usr/lib \
           -lrmfosal -lrmfosalutils -ltrm -lpthread -lrdkloggers -ljansson -llog4c

all: clean library install
	@echo "Build Finished...."

library: $(OBJS)
	@echo "Building $(TRM_LIB) ...."
	$(CROSSCOMPILE)$(CC) $(OBJS) $(CFLAGS) $(COPTS) $(LDOPTS) -shared -Wl,-rpath -o $(TRM_LIB)
	rm -rf $(OBJS)

$(OBJ_DIR)/%.o:$(SRC_DIR)/%.cpp
	$(CROSSCOMPILE)$(CC) -c $< $(CFLAGS) $(COPTS) -o $@

install:
	mv $(TRM_LIB) $(LIBDIR)

clean :
	rm -rf *.o $(TRM_LIB)
