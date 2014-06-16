#!/usr/bin/
trickPlayRate="$1"
echo "Trick Play rate: $trickPlayRate"
telnet localhost 3773 << EOF
t2p:msg trickModeRequest
{ "trickModeRequest" : { "rate" : $trickPlayRate } }
t2p:msg
echo "Done"
