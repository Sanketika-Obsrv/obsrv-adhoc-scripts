import datetime

REDIS_DEDUPE_HOST = "obsrv-redis-dedup-master.redis.svc.cluster.local"
REDIS_DENORM_HOST = "obsrv-redis-denorm-master.redis.svc.cluster.local"


def dataset_defaults(
    dataset_type, dataset_id, data_schema, ts_key, data_key, denorm_config, env
):
    return {
        "id": dataset_id,
        "dataset_id": dataset_id,
        "type": dataset_type,
        "name": dataset_id,
        "validation_config": {
            "validate": True,
            "mode": "Strict",
            "validation_mode": "Strict",
        },
        "extraction_config": {
            "is_batch_event": True,
            "extraction_key": "events",
            "dedup_config": {
                "drop_duplicates": True,
                "dedup_key": "id",
                "dedup_period": 1036800,
            },
            "batch_id": "id",
        },
        "dedup_config": {
            "drop_duplicates": False,
            "dedup_key": "",
            "dedup_period": 1036800,
        },
        "data_schema": data_schema,
        "denorm_config": {
            "redis_db_host": REDIS_DENORM_HOST,
            "redis_db_port": 6379,
            "denorm_fields": denorm_config if denorm_config else [],
        },
        "router_config": {"topic": dataset_id},
        "dataset_config": {
            "data_key": data_key,
            "timestamp_key": ts_key,
            "exclude_fields": [],
            "entry_topic": env + ".ingest",
            "redis_db_host": (
                REDIS_DENORM_HOST
                if dataset_type == "master-dataset"
                else REDIS_DEDUPE_HOST
            ),
            "redis_db_port": 6379,
            "index_data": True,
            "redis_db": 3 if dataset_type == "master-dataset" else 0,
        },
        "tags": [],
        "data_version": None,
        "status": "Live",
        "created_by": "SYSTEM",
        "updated_by": "SYSTEM",
        "created_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "published_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }


def datasource_defaults(dataset_id, ingestion_spec, ts_key):
    ingestion_spec["spec"]["dataSchema"]["dataSource"] = dataset_id + ".1_DAY"
    ingestion_spec["spec"]["dataSchema"]["timestampSpec"] = {
        "format": "auto",
        "column": ts_key
    }
    ingestion_spec["spec"]["ioConfig"]["topic"] = dataset_id
    return {
        "id": dataset_id + ".1_DAY",
        "datasource": dataset_id + ".1_DAY",
        "dataset_id": dataset_id,
        "ingestion_spec": ingestion_spec,
        "datasource_ref": dataset_id + ".1_DAY",
        "retention_period": {"enabled": "false"},
        "archival_policy": {"enabled": "false"},
        "purge_policy": {"enabled": "false"},
        "backup_config": {"enabled": "false"},
        "status": "Live",
        "created_by": "SYSTEM",
        "updated_by": "SYSTEM",
        "created_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "published_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "metadata": {"aggregated": False},
    }
