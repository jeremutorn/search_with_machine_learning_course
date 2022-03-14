#!/bin/bash

# Sets up an index and runs logstash to index the data.  Takes the required
# parameters as arguments.

function usage() {
	echo "Usage: ${0##*/} <name> <mappings_file> <logstash_conf_file> <logstash_data_dir>"
	exit 2
}

NAME="$1"    ; shift
MAPPING="$1" ; shift
LOGCONF="$1" ; shift
LOGDATA="$1" ; shift
if [ -z "$NAME" -o -z "$MAPPING" -o -z "$LOGCONF" -o -z "$LOGDATA" ] ; then
	usage
fi

echo "Using logstash data directory ${LOGDATA}."
if [ -e "$LOGDATA" ] ; then
	while true ; do
		echo "${LOGDATA} exists.  Remove?"
		echo -n 'Y/N?  '
		read INPUT
		if [    "$INPUT" == 'y' -o "$INPUT" == 'yes' \
		     -o "$INPUT" == 'Y' -o "$INPUT" == 'YES' ] ; then
			rm -rf -- "$LOGDATA"
			break
		elif [    "$INPUT" == 'n' -o "$INPUT" == 'no' \
		       -o "$INPUT" == 'N' -o "$INPUT" == 'NO' ] ; then
			echo 'Refusing to overwrite data.  Quitting.'
			exit 2
		fi
		echo 'Need y/Y/yes/YES/n/N/no/NO.'
	done
fi

# Start with a clean slate by removing any previous index.
# This may fail if the index does not already exist.  That is OK.
echo "Deleting index ${NAME} ..."
curl -k -X DELETE -u admin "https://localhost:9200/${NAME}" \
|| {
	ret="$?"
	echo "Curl failed ($ret)."
	exit "$ret"
}
echo

echo "Creating index ${NAME} with mappings from ${MAPPING} ..."
curl -k -X PUT -u admin -H 'Content-Type: application/json' -d "@${MAPPING}" \
     --fail "https://localhost:9200/${NAME}" \
|| {
	ret="$?"
	echo "Curl failed ($ret)."
	exit "$ret"
}
echo

echo "Indexing using conf file ${LOGCONF} ..."
exec logstash --pipeline.workers 1 --path.data "$LOGDATA" -f "$LOGCONF"
