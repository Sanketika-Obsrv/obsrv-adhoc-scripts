API_HOST = "http://localhost:3000"
DRUID_HOST = "http://localhost:8888"

ROUTES = {
    "CREATE_DATASETS": "/v1/datasets",
    "LIST_DATASETS": "/v1/datasets/list",
    "CREATE_DATASOURCES": "/v1/datasources",
    "LIST_DATASOURCES": "/v1/datasources/list",
    "PUSH_DATA": "/v1/data",
    "SUBMIT_INGESTION": "/druid/indexer/v1/supervisor"
}
