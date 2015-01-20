QMAKE=$QT_PATH/bin/qmake
echo "PATH SET " $RDK_BUILD_DIR $QMAKE 
$QMAKE -nocache  -o Makefile *.pro
make
if [ $? -eq 0 ] ; then
	echo "SUCCESS in" $(pwd)
	return 0
else
	echo "FAILED in" $(pwd)
	return 1
fi
