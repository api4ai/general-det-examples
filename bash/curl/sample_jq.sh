#!/bin/bash

######################################################
# NOTE:                                              #
#   This script requires "jq" command line tool!     #
#   See https://stedolan.github.io/jq/               #
######################################################


IMAGE=${1}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run base sample script to get raw output.
raw_response=$(bash ${DIR}/sample.sh "${IMAGE}")
echo -e "💬 Raw response:\n${raw_response}\n"

# Parse response and objects with confidence > 0.5.
count=$(jq "[.results[0].entities[0].objects[].entities[0].classes | select (.[] > 0.5)] | length" <<< ${raw_response})
echo "💬 ${count} objects found with confidence above 0.5:"
jq ".results[0].entities[0].objects[].entities[0].classes | select (.[] > 0.5)" <<< ${raw_response} | grep -v '{\|}'
