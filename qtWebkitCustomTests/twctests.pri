QT -= webkitwidgets webkit  
QT += widgets 
message("PATHS Set is  ::" $$system(env | echo $QT_PATH))
QT_DIR_PATH=$$system(env | echo $QT_PATH)
message("Got the path ::" $$QT_DIR_PATH)
#QT_DIR_PATH=/opt/UbuntuCodeBase/Xi3/master
PUBLISHER_IP_PATH=$$system(env | echo $PUBLISHER_IP)
message("Got the PUBLISHER_IP ::" $$PUBLISHER_IP_PATH)

CROSS_COMPILE=$$system(env | echo $CROSS_COMPILE)
message("CROSS_COMPILE ::" $$CROSS_COMPILE)

QT_TMTGTBUILDROOT=$$system(env | echo $IMAGE_PATH)
QT_ROOTFS_TMPLT_DIR=$$system(env | echo $IMAGE_PATH)
#QT_ROOTFS_TMPLT_DIR=/opt/UbuntuCodeBase/Xi3/master/workXI3/rootfs
#QT_TMTGTBUILDROOT=/opt/UbuntuCodeBase/Xi3/master/workXI3/rootfs
#LIBS += -L$/lib -lQt5WebKit -lQt5WebKitWidgets -lQt5Quick -lQt5Qml -lQt5Sensors -lQt5PrintSupport -lQt5OpenGL -lQt5V8 -lQt5Sql

#Before Qt5.2:-  
LIBS += -L$$QT_ROOTFS_TMPLT_DIR/usr/local/Qt/lib -lQt5WebKit -lQt5WebKitWidgets -lQt5OpenGL  -lQt5Sql -lQt5WebRTC -lQt5Network -lQt5Core -lQt5Gui
LIBS += -L/opt/UbuntuCodeBase/Xi3/master/workXI3/rootfs/usr/local/lib -lfontconfig
#LIBS += -L$$QT_ROOTFS_TMPLT_DIR/usr/local/Qt/lib -lQt5WebKit -lQt5WebKitWidgets -lQt5Quick -lQt5Qml -lQt5Sensors -lQt5PrintSupport -lQt5OpenGL -lQt5Sql -lQt5Positioning

LIBS += -L$$QT_TMTGTBUILDROOT/comps/generic_apps/usr/lib -lsqlite3

INCLUDEPATH += $$QT_DIR_PATH/include/QtWebKitWidgets
INCLUDEPATH += $$QT_DIR_PATH/include/QtWebKit
INCLUDEPATH += $$QT_DIR_PATH/include
INCLUDEPATH += $$QT_DIR_PATH/include/QtNetwork
#INCLUDEPATH +=$$QT_DIR_PATH/include/QtWebKitWidgets/QWebFrame

INCLUDEPATH += $$QT_DIR_PATH/opensources/qt-everywhere-opensource-src-5.2.1/qtwebkit/include/QtWebKit
INCLUDEPATH += $$QT_DIR_PATH/opensources/qt-everywhere-opensource-src-5.2.1/qtwebkit/include/QtWebKitWidgets 
INCLUDEPATH += $$QT_DIR_PATH/opensources/qt-everywhere-opensource-src-5.2.1/qtsensors/include/QtSensors 
INCLUDEPATH += $$QT_DIR_PATH/opensources/qt-everywhere-opensource-src-5.2.1/qtjsbackend/include
INCLUDEPATH += $$QT_DIR_PATH/opensources/qt-everywhere-opensource-src-5.2.1/qtwebkit/include
INCLUDEPATH += $$QT_DIR_PATH/opensources/qt-everywhere-opensource-src-5.2.1/qtlocation/include/QtPositioning/


