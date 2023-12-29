curl -s --location \
--request POST https://${ASTRA_DB_ID}-${ASTRA_DB_REGION}.apps.astra.datastax.com/api/json/v1/default_keyspace \
--header "X-Cassandra-Token: $ASTRA_DB_APPLICATION_TOKEN" \
--header "Content-Type: application/json" \
--header "Accept: application/json" \
--data '{"deleteCollection": {"name": "'${ASTRA_DB_COLLECTION_NAME}'"}}'