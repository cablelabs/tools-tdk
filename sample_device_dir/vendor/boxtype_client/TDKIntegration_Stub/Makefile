include ../../def.inc

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

#The PKG_CONFIG_PATH needs to be changed based on the toolchain on user's environment
export PKG_CONFIG_PATH =$(RDK_BUILD_DIR)/workXI3/Refsw/AppLibs/target/97428b0.mipsel-linux.release/usr/local/lib/pkgconfig
PLAYERCFLAGS    := `pkg-config gstreamer-0.10 libffi --cflags`
PLAYERLIBS      := `pkg-config gstreamer-0.10 libffi --libs`
CC	  := gcc

SOURCE_APP:= $(PLAYER_SRC_PATH)/*.c
PLAYER_EXE:= mplayer

all : 
	mkdir -p $(TARGETDIR)
	$(CROSSCOMPILE)$(CC) $(PLAYERCFLAGS) $(SOURCE_APP) -o $(PLAYER_EXE) $(PLAYERLIBS)
	mv $(PLAYER_EXE) $(TDK_BIN_PATH)

build: all

