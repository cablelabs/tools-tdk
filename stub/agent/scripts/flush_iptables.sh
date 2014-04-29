#Abort if there are errors.
set -e
set -o pipefail

echo "Flushing filter table..."
iptables -t filter -F
echo "Done."

echo "Flushing NAT table..."
iptables -t nat -F
echo "Done. Flushed iptables."
