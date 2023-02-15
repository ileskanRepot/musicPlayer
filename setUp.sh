#!/usr/bin/env bash

[ ! -d ./psw ] && mkdir psw
[ ! -f ./psw/login.csv ] && echo "***REMOVED***" > ./psw/login.csv
[ ! -f ./psw/token.csv ] && echo "userName,token,lastUsed" > ./psw/token.csv
