for i in ./*/; do
	cd $i
	rm *.o
	rm *.moc
	rm Makefile
	rm qrc_*.cpp
        find . -type f ! -name "*.*" -perm -og+rx -delete

	echo "##########cleanall DONE WITH $i  "$(pwd)
	cd ..
done
