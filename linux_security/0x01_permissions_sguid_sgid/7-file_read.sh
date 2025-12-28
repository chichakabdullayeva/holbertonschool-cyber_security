#!/bin/bash
find $1 -type f chmod o=r -exec ls -l 2>/dev/null
