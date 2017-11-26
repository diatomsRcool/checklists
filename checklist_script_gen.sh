#!/bin/bash
# generates checklist_status.sh using wkt_string.tsv
# the generated checklist_status.sh produces checklist_status.tsv
# checklist_status.tsv contains a status overview of all checklists associated with wkt_string.tsv

generate_status_script() {
  echo "echo \"geonames_id\\\tchecked_at\\\thttp_status_code\" > checklist_status.tsv" > checklist_status.sh
  cat wkt_string.tsv | awk -F '\t'  '{ print "curl -s -o /dev/null -w \"%{http_code}\" \"http://api.effechecka.org/checklist.csv?limit=1&wktString=" $2 "\"| xargs echo " $1 "\\\t$(date -Is)\\\t >> checklist_status.tsv"; }' >> checklist_status.sh
}

generate_download_script() {
  script_name="checklist_download.sh"
  echo "mkdir checklist" >> $script_name
  cat wkt_string.tsv | awk -F '\t'  '{ print "curl -o checklist/" $1 ".tsv \"http://api.effechecka.org/checklist.tsv?wktString=" $2 "\""; }' >> $script_name
  echo "tar czf checklist.tar.gz wkt_string.tsv checklist_* checklist/*" >> $script_name
}

generate_status_script
generate_download_script
