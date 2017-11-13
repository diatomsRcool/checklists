#!/bin/sh
# generates checklist_status.sh using wkt_string.tsv
# the generated checklist_status.sh produces checklist_status.tsv
# checklist_status.tsv contains a status overview of all checklists associated with wkt_string.tsv
cat wkt_string.tsv | awk -F '\t'  '{ print "curl -s -o /dev/null -w \"%{http_code}\" \"http://api.effechecka.org/checklist?limit=1&wktString=" $2 "\"| xargs echo " $1 "\\\t$(date -Is)\\\t >> checklist_status.tsv"; }' >> checklist_status.sh
