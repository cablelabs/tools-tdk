#/bin/sh
cd /home/snagarajan/ssltest/sslsplit-0.4.11
 ./sslsplit \
  -D \
  -L connections.log \
  -j /home/snagarajan/ssltest/logs/sslsplit/ \
  -S content/ \
  -k /home/snagarajan/ssltest/keys/ca.key \
  -c /home/snagarajan/ssltest/stbcerts/ca-certificates.crt \
   https 162.150.26.230 843 fkps.ccp.xcal.tv 443 \

#  -s !AES128:!SHA256:!SHA-384:!SHA-512:!RSA \
#-r tls11 \
