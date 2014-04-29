HOME_NETWORK_INTERFACE=eth1
#echo "Generating list of MoCA device MACs..."
if [ $# -lt 1 ]; then
	echo "Error! Insufficient arguments. Format is $0 <output file path>"
	exit 1
fi
arp -n -i $HOME_NETWORK_INTERFACE | grep "?" | awk '{print $4}' > $TDK_PATH/$1
#echo "Done"
