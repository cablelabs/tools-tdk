rm -rf $1/*
for i in ./qtest*/; do
        cd $i
        find . -type f ! -name "*.*" -perm -og+rx -exec cp  {} $1  \;
        echo "##########moveall DONE WITH $i  "$(pwd)
        cd ..
done




