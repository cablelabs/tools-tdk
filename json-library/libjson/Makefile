include ../../def.inc
default: build

LIBDIR=$(RDK_PROJECT_ROOT_PATH)/tdk/build/libs
TARGETDIR=$(RDK_PROJECT_ROOT_PATH)/tdk/build/bin
IMAGE_PATH=$(RDK_PROJECT_ROOT_PATH)/sdk/fsroot/ramdisk/
CROSSCOMPILE=$(RDK_TOOLCHAIN_PATH)/bin/i686-cm-linux-


#
# Source files
#
SRC_DIR   := ./src/lib_json/
OBJDIR	  := obj
COPTS     := -c

COPTS     += -Wall -pedantic -O2 -std=c++0x
		 
INCLUDES  +=    -I./include/

LIBOPTS   := -shared
CC	  := g++
TARGETLIB	:= libjson.so
	
#
# Library built by this makefile
#
LIB        = $(LIBDIR)/$(TARGETLIB)
SOURCES   := $(SRC_DIR)*.cpp

#
# Intermediate files
#
OBJS       =$(OBJDIR)/*.o

#
# Compile source files into intermediate files
#
$(OBJS): $(SOURCES) 
	mkdir -p $(OBJDIR)
	$(CROSSCOMPILE)$(CC) $(INCLUDES) -fPIC $(COPTS) $^
	mv *.o $(OBJDIR)


#
# Build the library from intermediate files
#
$(LIB): $(OBJS)
	$(CROSSCOMPILE)$(CC) $(OBJS) -fPIC $(LIBOPTS) -o $(TARGETLIB)
	rm -rf $(OBJDIR)
	mkdir -p $(LIBDIR)
	mv $(TARGETLIB) $(LIBDIR)
#
# Build everything
#
build: $(LIB) 

#
# Clean 
#
clean:
	rm -rf $(LIB)
	rm -rf $(OBJDIR)

