#!/bin/bash -x 
python3 -m pip install --upgrade pip
python3 -m pip install grpcio
pip install grpcio-tools
npm install -g grpc-tools

# chmod +x $GOPATH/bin/protoc

echo "SUCCESS"
#end