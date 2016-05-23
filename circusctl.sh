#!/bin/bash
endpoint=$(grep "^endpoint" circus.conf | sed "s/^.* = \(.*\)$/\1/g")
bin/circusctl --endpoint $endpoint $*

