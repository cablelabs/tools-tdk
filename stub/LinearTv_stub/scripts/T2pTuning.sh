#!/usr/bin/
ocapId="$1"
echo "OCAP ID: $ocapId"
telnet localhost 3773 << EOF
t2p:msg selectService
{ "selectService" : { "locator" : "$ocapId" } }
t2p:msg
echo "Done"
