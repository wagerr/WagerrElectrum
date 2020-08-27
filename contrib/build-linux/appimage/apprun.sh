#!/bin/bash

set -e

APPDIR="$(dirname "$(readlink -e "$0")")"
APPNAME="$(basename "$ARGV0")"

export LD_LIBRARY_PATH="${APPDIR}/usr/lib/:${APPDIR}/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH+:$LD_LIBRARY_PATH}"
export PATH="${APPDIR}/usr/bin:${PATH}"
export LDFLAGS="-L${APPDIR}/usr/lib/x86_64-linux-gnu -L${APPDIR}/usr/lib"

if [[ $APPNAME == *"testnet"* ]];
then
  exec "${APPDIR}/usr/bin/python3.7" -s "${APPDIR}/usr/bin/electrum" "--testnet"
else
  exec "${APPDIR}/usr/bin/python3.7" -s "${APPDIR}/usr/bin/electrum" "$@"
fi

