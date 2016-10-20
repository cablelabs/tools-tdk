##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
#/bin/sh
cd /home/snagarajan/ssltest/sslsplit-0.4.11
 ./sslsplit \
  -D \
  -L connections.log \
  -j /home/snagarajan/ssltest/logs/sslsplit/ \
  -S content/ \
  -k /home/snagarajan/ssltest/keys/ca.key \
  -c /home/snagarajan/ssltest/keys/ca.crt \
  -s AES128:SHA256:SHA-384:SHA-512:RSA \
  -r ssl3 \
   https 162.150.26.230 843 xconf.xcal.tv 443 \

