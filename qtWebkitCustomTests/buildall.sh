export QT_PATH=$RDK_BUILD_DIR/opensource/qt/stage/usr/local/Qt
export QMAKESPEC=$QT_PATH/mkspecs/devices/linux-platfrom-rdk-g++/
export FAILED=0
source ./cleanall.sh
for i in ./qtest*/; do
	cd $i
	source ../build.sh
        if [ $? -eq 0 ] ; then
                echo "buildall SUCCESS in" $(pwd)
        else
                echo "buildall FAILED in" $(pwd)
		export FAILED=1
        fi

	echo "########## DONE WITH $i  "$(pwd)
	cd ..
done
if [ $FAILED == 1 ]
then
	echo "BUILD FAILED";
fi
