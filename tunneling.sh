#!/bin/bash

print_help(){
    remote=$(dig +short myip.opendns.com @resolver1.opendns.com)
    local=$(hostname -I)
    echo "Usage: bash tunneling.sh $remote $local"
}
if [ "$1" == "--help" ]; then
    print_help
    exit 0
    
elif [ "$#" -ne 2 ]; then
    echo "Wrong args, --help"
    exit 0
fi

ip link add gt0 type gretap remote $1 local $2 key 1

ip addr add 10.0.0.1/24 dev gt0
ip addr add 10.0.0.2/24 dev gt0
ip addr add 10.0.0.3/24 dev gt0

ip link set dev gt0 up