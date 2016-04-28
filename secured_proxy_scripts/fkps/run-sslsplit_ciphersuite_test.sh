#/bin/sh
cd /home/snagarajan/ssltest/sslsplit-0.4.11
 ./sslsplit \
  -D \
  -L connections.log \
  -j /home/snagarajan/ssltest/logs/sslsplit/ \
  -S content/ \
  -k /home/snagarajan/ssltest/keys/ca.key \
  -c /home/snagarajan/ssltest/keys/ca.crt \
  -s ALL:!AES128:!SHA256:!SHA-384:!SHA-512:!RSA \
   https 162.150.26.230 843 fkps.ccp.xcal.tv 443 \

#-r tls11 \
