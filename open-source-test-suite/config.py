API_HOST = "http://192.168.49.2:30500"
DRUID_HOST = "http://192.168.49.2:30503"

ROUTES = {
    "CREATE_DATASETS": "/datasets/v1/create",
    "LIST_DATASETS": "/datasets/v1/list",
    "CREATE_DATASOURCES": "/datasources/v1/create",
    "LIST_DATASOURCES": "/datasources/v1/list",
    "PUSH_DATA": "/data/v1/in",
    "SUBMIT_INGESTION": "/druid/indexer/v1/supervisor"
}

ENV = "dev"
