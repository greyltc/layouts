#!/usr/bin/env bash

# a directory with .step files to maks smaller
LOOK_IN_HERE="$1"

_ensmall_threads=1

export EXT="step"

# first use stepreduce
find -name "*.${EXT}" -print0 | xargs -0 -P ${_ensmall_threads} -I % sh -c 'stepreduce % %.reduced; mv %.reduced %'

# then use zip
# find -name "*.${EXT}" -print0 | xargs -0 -P ${_ensmall_threads} -I % sh -c 'zip --move $(dirname %)/$(basename % ${EXT})stpz %' # deletes origional
find -name "*.${EXT}" -print0 | xargs -0 -P ${_ensmall_threads} -I % sh -c 'zip $(dirname %)/$(basename % ${EXT})stpz %'  # keeps origional
