import requests

spec = {
    "type": "kafka",
    "spec": {
        "dataSchema": {
            "dataSource": "<DATASOURCE>",
            "dimensionsSpec": {
                "dimensions": [
                    { "type": "string", "name": "eid" },
                    { "type": "string", "name": "ver" },
                    { "type": "string", "name": "mid" },
                    { "type": "string", "name": "actor_id" },
                    { "type": "string", "name": "actor_type" },
                    { "type": "string", "name": "context_channel" },
                    { "type": "string", "name": "context_pdata_id" },
                    { "type": "string", "name": "context_pdata_pid" },
                    { "type": "string", "name": "context_pdata_ver" },
                    { "type": "string", "name": "context_pdata_platform" },
                    { "type": "string", "name": "context_env" },
                    { "type": "string", "name": "context_sid" },
                    { "type": "string", "name": "context_did" },
                    { "type": "array", "name": "context_cdata_type" },
                    { "type": "array", "name": "context_cdata_id" },
                    { "type": "string", "name": "context_rollup_l1" },
                    { "type": "string", "name": "context_rollup_l2" },
                    { "type": "string", "name": "context_rollup_l3" },
                    { "type": "string", "name": "context_rollup_l4" },
                    { "type": "string", "name": "context_uid" },
                    { "type": "string", "name": "object_id" },
                    { "type": "string", "name": "object_type" },
                    { "type": "string", "name": "object_ver" },
                    { "type": "string", "name": "object_rollup_l1" },
                    { "type": "string", "name": "object_rollup_l2" },
                    { "type": "string", "name": "object_rollup_l3" },
                    { "type": "string", "name": "object_rollup_l4" },
                    { "type": "string", "name": "edata_type" },
                    { "type": "string", "name": "edata_subtype" },
                    { "type": "string", "name": "edata_pageid" },
                    { "type": "string", "name": "edata_uri" },
                    { "type": "long", "name": "edata_duration" },
                    { "type": "long", "name": "edata_visits" },
                    { "type": "string", "name": "edata_id" },
                    { "type": "string", "name": "edata_target_id" },
                    { "type": "string", "name": "edata_target_type" },
                    { "type": "string", "name": "edata_target_ver" },
                    { "type": "string", "name": "edata_plugin" },
                    { "type": "array", "name": "edata_extra_pos_x" },
                    { "type": "array", "name": "edata_extra_pos_y" },
                    { "type": "array", "name": "edata_extra_pos_z" },
                    { "type": "array", "name": "edata_extra_values" },
                    { "type": "string", "name": "edata_dspec_id" },
                    { "type": "string", "name": "edata_uaspec_agent" },
                    { "type": "string", "name": "edata_loc" },
                    { "type": "string", "name": "edata_mode" },
                    { "type": "array", "name": "edata_summary_progress" },
                    { "type": "array", "name": "edata_summary_nodesModified" },
                    { "type": "string", "name": "edata_query" },
                    { "type": "string", "name": "edata_filters_dialcodes" },
                    { "type": "array", "name": "edata_filters_channel_ne" },
                    { "type": "json", "name": "edata_sort" },
                    { "type": "string", "name": "edata_correlationid" },
                    { "type": "long", "name": "edata_size" },
                    { "type": "array", "name": "edata_topn_identifier" },
                    { "type": "array", "name": "edata_props" },
                    { "type": "string", "name": "edata_state" },
                    { "type": "string", "name": "edata_prevstate" },
                    { "type": "string", "name": "edata_err" },
                    { "type": "string", "name": "edata_errtype" },
                    { "type": "string", "name": "edata_stacktrace" },
                    { "type": "string", "name": "edata_item_desc" },
                    { "type": "long", "name": "edata_item_exlength" },
                    { "type": "string", "name": "edata_item_id" },
                    { "type": "long", "name": "edata_item_maxscore" },
                    { "type": "array", "name": "edata_item_params_foo" },
                    { "type": "array", "name": "edata_item_params_bar" },
                    { "type": "array", "name": "edata_item_params_bike" },
                    { "type": "array", "name": "edata_item_params_a" },
                    { "type": "array", "name": "edata_item_params_b" },
                    { "type": "array", "name": "edata_item_params_name" },
                    { "type": "array", "name": "edata_item_params_prop" },
                    { "type": "string", "name": "edata_item_uri" },
                    { "type": "string", "name": "edata_pass" },
                    { "type": "array", "name": "edata_resvalues_ans34" },
                    { "type": "array", "name": "edata_resvalues_ans80" },
                    { "type": "array", "name": "edata_resvalues_ans100" },
                    { "type": "array", "name": "edata_resvalues_ans92" },
                    { "type": "array", "name": "edata_resvalues_ans52" },
                    { "type": "array", "name": "edata_resvalues_ans89" },
                    { "type": "array", "name": "edata_resvalues_ans6" },
                    { "type": "array", "name": "edata_resvalues_ans72" },
                    { "type": "array", "name": "edata_resvalues_ans14" },
                    { "type": "array", "name": "edata_resvalues_ans40" },
                    { "type": "array", "name": "edata_resvalues_ans28" },
                    { "type": "array", "name": "edata_resvalues_ans53" },
                    { "type": "array", "name": "edata_resvalues_ans41" },
                    { "type": "array", "name": "edata_resvalues_ans84" },
                    { "type": "array", "name": "edata_resvalues_ans17" },
                    { "type": "array", "name": "edata_resvalues_ans58" },
                    { "type": "array", "name": "edata_resvalues_ans3" },
                    { "type": "array", "name": "edata_resvalues_ans11" },
                    { "type": "array", "name": "edata_resvalues_ans55" },
                    { "type": "array", "name": "edata_resvalues_ans13" },
                    { "type": "array", "name": "edata_resvalues_ans23" },
                    { "type": "array", "name": "edata_resvalues_ans74" },
                    { "type": "long", "name": "edata_score" },
                    { "type": "string", "name": "edata_data" },
                    { "type": "long", "name": "edata_rating" },
                    { "type": "string", "name": "edata_comments" },
                    { "type": "string", "name": "edata_level" },
                    { "type": "string", "name": "edata_message" },
                    { "type": "array", "name": "edata_params_foo" },
                    { "type": "array", "name": "edata_params_bar" },
                    { "type": "array", "name": "edata_params_bike" },
                    { "type": "array", "name": "edata_params_a" },
                    { "type": "array", "name": "edata_params_b" },
                    { "type": "array", "name": "edata_params_name" },
                    { "type": "array", "name": "edata_params_prop" },
                    { "type": "string", "name": "edata_eius" },
                    { "type": "string", "name": "edata_qui" },
                    { "type": "string", "name": "edata_recusandae" },
                    { "type": "string", "name": "edata_beatae" },
                    { "type": "string", "name": "edata_tempore" },
                    { "type": "string", "name": "edata_omnis" },
                    { "type": "string", "name": "edata_odit" },
                    { "type": "string", "name": "edata_quisquam" },
                    { "type": "string", "name": "edata_consectetur" },
                    { "type": "string", "name": "edata_ex" },
                    { "type": "string", "name": "edata_necessitatibus" },
                    { "type": "string", "name": "edata_praesentium" },
                    { "type": "string", "name": "edata_totam" },
                    { "type": "string", "name": "edata_occaecati" },
                    { "type": "string", "name": "edata_molestias" },
                    { "type": "string", "name": "edata_velit" },
                    { "type": "string", "name": "edata_quis" },
                    { "type": "string", "name": "edata_eos" },
                    { "type": "string", "name": "edata_ipsam" },
                    { "type": "string", "name": "edata_repellat" },
                    { "type": "string", "name": "edata_ipsa" },
                    { "type": "string", "name": "edata_officiis" },
                    { "type": "string", "name": "edata_doloremque" },
                    { "type": "string", "name": "edata_suscipit" },
                    { "type": "string", "name": "edata_vero" },
                    { "type": "string", "name": "edata_illum" },
                    { "type": "string", "name": "edata_ab" },
                    { "type": "string", "name": "edata_error" },
                    { "type": "string", "name": "edata_saepe" },
                    { "type": "string", "name": "edata_natus" },
                    { "type": "string", "name": "edata_adipisci" },
                    { "type": "string", "name": "edata_quod" },
                    { "type": "string", "name": "edata_commodi" },
                    { "type": "string", "name": "edata_facere" },
                    { "type": "string", "name": "edata_optio" },
                    { "type": "string", "name": "edata_libero" },
                    { "type": "string", "name": "edata_veritatis" },
                    { "type": "string", "name": "edata_nobis" },
                    { "type": "string", "name": "edata_itaque" },
                    { "type": "string", "name": "edata_dolorum" },
                    { "type": "string", "name": "edata_rem" },
                    { "type": "string", "name": "edata_quos" },
                    { "type": "string", "name": "edata_vitae" },
                    { "type": "string", "name": "edata_ducimus" },
                    { "type": "string", "name": "edata_pariatur" },
                    { "type": "string", "name": "edata_explicabo" },
                    { "type": "string", "name": "edata_animi" },
                    { "type": "string", "name": "edata_quae" },
                    { "type": "string", "name": "edata_aperiam" },
                    { "type": "string", "name": "edata_voluptates" },
                    { "type": "string", "name": "edata_mollitia" },
                    { "type": "string", "name": "edata_excepturi" },
                    { "type": "string", "name": "edata_atque" },
                    { "type": "string", "name": "edata_neque" },
                    { "type": "string", "name": "edata_sapiente" },
                    { "type": "string", "name": "edata_repellendus" },
                    { "type": "string", "name": "edata_minima" },
                    { "type": "string", "name": "edata_rerum" },
                    { "type": "string", "name": "edata_deleniti" },
                    { "type": "string", "name": "edata_debitis" },
                    { "type": "array", "name": "edata_values_lhs" },
                    { "type": "array", "name": "edata_values_rhs" },
                    { "type": "string", "name": "edata_dir" },
                    { "type": "array", "name": "edata_items_ver" },
                    { "type": "array", "name": "edata_items_origin_id" },
                    { "type": "array", "name": "edata_items_origin_type" },
                    { "type": "array", "name": "edata_items_id" },
                    { "type": "array", "name": "edata_items_to_id" },
                    { "type": "array", "name": "edata_items_to_type" },
                    { "type": "array", "name": "edata_items_type" },
                    {
                        "type": "array",
                        "name": "edata_items_params[*]_transfers"
                    },
                    { "type": "array", "name": "edata_items_params[*]_count" },
                    { "type": "long", "name": "edata_starttime" },
                    { "type": "long", "name": "edata_endtime" },
                    { "type": "long", "name": "edata_timespent" },
                    { "type": "long", "name": "edata_pageviews" },
                    { "type": "long", "name": "edata_interactions" },
                    { "type": "array", "name": "edata_envsummary_env" },
                    { "type": "array", "name": "edata_envsummary_timespent" },
                    { "type": "array", "name": "edata_envsummary_visits" },
                    { "type": "array", "name": "edata_eventssummary_id" },
                    { "type": "array", "name": "edata_eventssummary_count" },
                    { "type": "array", "name": "edata_pagesummary_id" },
                    { "type": "array", "name": "edata_pagesummary_type" },
                    { "type": "array", "name": "edata_pagesummary_env" },
                    { "type": "array", "name": "edata_pagesummary_timespent" },
                    { "type": "array", "name": "edata_pagesummary_visits" },
                    { "type": "array", "name": "tags" },
                    { "type": "long", "name": "syncts" },
                    { "type": "string", "name": "@timestamp" },
                    { "type": "string", "name": "devicedata_fcm_token" },
                    { "type": "string", "name": "devicedata_city" },
                    { "type": "string", "name": "devicedata_device_id" },
                    { "type": "string", "name": "devicedata_device_spec" },
                    { "type": "string", "name": "devicedata_state" },
                    { "type": "string", "name": "devicedata_uaspec_agent" },
                    { "type": "string", "name": "devicedata_uaspec_ver" },
                    { "type": "string", "name": "devicedata_uaspec_system" },
                    { "type": "string", "name": "devicedata_uaspec_raw" },
                    { "type": "string", "name": "devicedata_country" },
                    { "type": "string", "name": "devicedata_country_code" },
                    { "type": "string", "name": "devicedata_producer_id" },
                    { "type": "long", "name": "devicedata_state_code_custom" },
                    { "type": "string", "name": "devicedata_state_code" },
                    { "type": "string", "name": "devicedata_state_custom" },
                    { "type": "string", "name": "devicedata_district_custom" },
                    { "type": "long", "name": "devicedata_first_access" },
                    {
                        "type": "long",
                        "name": "devicedata_api_last_updated_on"
                    },
                    {
                        "type": "string",
                        "name": "devicedata_user_declared_district"
                    },
                    {
                        "type": "string",
                        "name": "devicedata_user_declared_state"
                    },
                    { "type": "long", "name": "contentdata_ets" },
                    { "type": "string", "name": "contentdata_channel" },
                    { "type": "array", "name": "contentdata_ownershipType" },
                    { "type": "string", "name": "contentdata_code" },
                    { "type": "string", "name": "contentdata_description" },
                    { "type": "array", "name": "contentdata_organisation" },
                    { "type": "array", "name": "contentdata_language" },
                    { "type": "string", "name": "contentdata_mimeType" },
                    { "type": "string", "name": "contentdata_idealScreenSize" },
                    { "type": "string", "name": "contentdata_createdOn" },
                    { "type": "string", "name": "contentdata_appId" },
                    {
                        "type": "string",
                        "name": "contentdata_contentDisposition"
                    },
                    { "type": "string", "name": "contentdata_lastUpdatedOn" },
                    { "type": "string", "name": "contentdata_contentEncoding" },
                    { "type": "string", "name": "contentdata_contentType" },
                    {
                        "type": "string",
                        "name": "contentdata_dialcodeRequired"
                    },
                    { "type": "string", "name": "contentdata_creator" },
                    { "type": "array", "name": "contentdata_createdFor" },
                    {
                        "type": "string",
                        "name": "contentdata_lastStatusChangedOn"
                    },
                    { "type": "array", "name": "contentdata_audience" },
                    {
                        "type": "string",
                        "name": "contentdata_IL_SYS_NODE_TYPE"
                    },
                    { "type": "string", "name": "contentdata_visibility" },
                    { "type": "array", "name": "contentdata_os" },
                    { "type": "string", "name": "contentdata_consumerId" },
                    { "type": "string", "name": "contentdata_mediaType" },
                    { "type": "string", "name": "contentdata_osId" },
                    { "type": "long", "name": "contentdata_version" },
                    { "type": "string", "name": "contentdata_versionKey" },
                    {
                        "type": "string",
                        "name": "contentdata_idealScreenDensity"
                    },
                    { "type": "string", "name": "contentdata_license" },
                    { "type": "string", "name": "contentdata_framework" },
                    { "type": "string", "name": "contentdata_createdBy" },
                    {
                        "type": "long",
                        "name": "contentdata_compatibilityLevel"
                    },
                    {
                        "type": "string",
                        "name": "contentdata_IL_FUNC_OBJECT_TYPE"
                    },
                    { "type": "string", "name": "contentdata_name" },
                    { "type": "string", "name": "contentdata_IL_UNIQUE_ID" },
                    { "type": "string", "name": "contentdata_resourceType" },
                    { "type": "string", "name": "contentdata_status" },
                    { "type": "string", "name": "contentdata_mid" },
                    { "type": "string", "name": "contentdata_label" },
                    { "type": "string", "name": "contentdata_nodeType" },
                    { "type": "string", "name": "contentdata_userId" },
                    { "type": "string", "name": "contentdata_objectType" },
                    { "type": "string", "name": "contentdata_nodeUniqueId" },
                    { "type": "string", "name": "contentdata_requestId" },
                    { "type": "string", "name": "contentdata_operationType" },
                    { "type": "long", "name": "contentdata_nodeGraphId" },
                    { "type": "string", "name": "contentdata_graphId" }
                ]
            },
            "timestampSpec": { "column": "ets", "format": "auto" },
            "metricsSpec": [],
            "granularitySpec": {
                "type": "uniform",
                "segmentGranularity": "DAY",
                "queryGranularity": "none",
                "rollup": False
            },
            "transformSpec": {}
        },
        "tuningConfig": {
            "type": "kafka",
            "maxBytesInMemory": 134217728,
            "maxRowsPerSegment": 5000000,
            "logParseExceptions": True
        },
        "ioConfig": {
            "type": "kafka",
            "topic": "<TOPIC>",
            "consumerProperties": {
                "bootstrap.servers": "obsrv-kafka-headless.kafka.svc.cluster.local:9092"
            },
            "taskCount": 1,
            "replicas": 1,
            "taskDuration": "PT1H",
            "useEarliestOffset": True,
            "completionTimeout": "PT1H",
            "inputFormat": {
                "type": "json",
                "flattenSpec": {
                    "useFieldDiscovery": True,
                    "fields": [
                        { "type": "path", "expr": "$.eid", "name": "eid" },
                        { "type": "path", "expr": "$.ets", "name": "ets" },
                        { "type": "path", "expr": "$.ver", "name": "ver" },
                        { "type": "path", "expr": "$.mid", "name": "mid" },
                        {
                            "type": "path",
                            "expr": "$.actor.id",
                            "name": "actor_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.actor.type",
                            "name": "actor_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.channel",
                            "name": "context_channel"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.pdata.id",
                            "name": "context_pdata_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.pdata.pid",
                            "name": "context_pdata_pid"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.pdata.ver",
                            "name": "context_pdata_ver"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.pdata.platform",
                            "name": "context_pdata_platform"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.env",
                            "name": "context_env"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.sid",
                            "name": "context_sid"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.did",
                            "name": "context_did"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.cdata[*].type",
                            "name": "context_cdata_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.cdata[*].id",
                            "name": "context_cdata_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.rollup.l1",
                            "name": "context_rollup_l1"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.rollup.l2",
                            "name": "context_rollup_l2"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.rollup.l3",
                            "name": "context_rollup_l3"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.rollup.l4",
                            "name": "context_rollup_l4"
                        },
                        {
                            "type": "path",
                            "expr": "$.context.uid",
                            "name": "context_uid"
                        },
                        {
                            "type": "path",
                            "expr": "$.object.id",
                            "name": "object_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.object.type",
                            "name": "object_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.object.ver",
                            "name": "object_ver"
                        },
                        {
                            "type": "path",
                            "expr": "$.object.rollup.l1",
                            "name": "object_rollup_l1"
                        },
                        {
                            "type": "path",
                            "expr": "$.object.rollup.l2",
                            "name": "object_rollup_l2"
                        },
                        {
                            "type": "path",
                            "expr": "$.object.rollup.l3",
                            "name": "object_rollup_l3"
                        },
                        {
                            "type": "path",
                            "expr": "$.object.rollup.l4",
                            "name": "object_rollup_l4"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.type",
                            "name": "edata_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.subtype",
                            "name": "edata_subtype"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pageid",
                            "name": "edata_pageid"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.uri",
                            "name": "edata_uri"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.duration",
                            "name": "edata_duration"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.visits",
                            "name": "edata_visits"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.id",
                            "name": "edata_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.target.id",
                            "name": "edata_target_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.target.type",
                            "name": "edata_target_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.target.ver",
                            "name": "edata_target_ver"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.plugin",
                            "name": "edata_plugin"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.extra.pos[*].x",
                            "name": "edata_extra_pos_x"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.extra.pos[*].y",
                            "name": "edata_extra_pos_y"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.extra.pos[*].z",
                            "name": "edata_extra_pos_z"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.extra.values[*]",
                            "name": "edata_extra_values"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.dspec.id",
                            "name": "edata_dspec_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.uaspec.agent",
                            "name": "edata_uaspec_agent"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.loc",
                            "name": "edata_loc"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.mode",
                            "name": "edata_mode"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.summary[*].progress",
                            "name": "edata_summary_progress"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.summary[*].nodesModified",
                            "name": "edata_summary_nodesModified"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.query",
                            "name": "edata_query"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.filters.dialcodes",
                            "name": "edata_filters_dialcodes"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.filters.channel[*].ne",
                            "name": "edata_filters_channel_ne"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.sort",
                            "name": "edata_sort"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.correlationid",
                            "name": "edata_correlationid"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.size",
                            "name": "edata_size"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.topn[*].identifier",
                            "name": "edata_topn_identifier"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.props[*]",
                            "name": "edata_props"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.state",
                            "name": "edata_state"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.prevstate",
                            "name": "edata_prevstate"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.err",
                            "name": "edata_err"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.errtype",
                            "name": "edata_errtype"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.stacktrace",
                            "name": "edata_stacktrace"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.desc",
                            "name": "edata_item_desc"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.exlength",
                            "name": "edata_item_exlength"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.id",
                            "name": "edata_item_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.maxscore",
                            "name": "edata_item_maxscore"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.params[*].foo",
                            "name": "edata_item_params_foo"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.params[*].bar",
                            "name": "edata_item_params_bar"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.params[*].bike",
                            "name": "edata_item_params_bike"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.params[*].a",
                            "name": "edata_item_params_a"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.params[*].b",
                            "name": "edata_item_params_b"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.params[*].name",
                            "name": "edata_item_params_name"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.params[*].prop",
                            "name": "edata_item_params_prop"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.item.uri",
                            "name": "edata_item_uri"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pass",
                            "name": "edata_pass"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans34",
                            "name": "edata_resvalues_ans34"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans80",
                            "name": "edata_resvalues_ans80"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans100",
                            "name": "edata_resvalues_ans100"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans92",
                            "name": "edata_resvalues_ans92"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans52",
                            "name": "edata_resvalues_ans52"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans89",
                            "name": "edata_resvalues_ans89"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans6",
                            "name": "edata_resvalues_ans6"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans72",
                            "name": "edata_resvalues_ans72"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans14",
                            "name": "edata_resvalues_ans14"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans40",
                            "name": "edata_resvalues_ans40"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans28",
                            "name": "edata_resvalues_ans28"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans53",
                            "name": "edata_resvalues_ans53"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans41",
                            "name": "edata_resvalues_ans41"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans84",
                            "name": "edata_resvalues_ans84"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans17",
                            "name": "edata_resvalues_ans17"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans58",
                            "name": "edata_resvalues_ans58"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans3",
                            "name": "edata_resvalues_ans3"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans11",
                            "name": "edata_resvalues_ans11"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans55",
                            "name": "edata_resvalues_ans55"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans13",
                            "name": "edata_resvalues_ans13"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans23",
                            "name": "edata_resvalues_ans23"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.resvalues[*].ans74",
                            "name": "edata_resvalues_ans74"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.score",
                            "name": "edata_score"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.data",
                            "name": "edata_data"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.rating",
                            "name": "edata_rating"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.comments",
                            "name": "edata_comments"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.level",
                            "name": "edata_level"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.message",
                            "name": "edata_message"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.params[*].foo",
                            "name": "edata_params_foo"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.params[*].bar",
                            "name": "edata_params_bar"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.params[*].bike",
                            "name": "edata_params_bike"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.params[*].a",
                            "name": "edata_params_a"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.params[*].b",
                            "name": "edata_params_b"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.params[*].name",
                            "name": "edata_params_name"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.params[*].prop",
                            "name": "edata_params_prop"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.eius",
                            "name": "edata_eius"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.qui",
                            "name": "edata_qui"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.recusandae",
                            "name": "edata_recusandae"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.beatae",
                            "name": "edata_beatae"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.tempore",
                            "name": "edata_tempore"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.omnis",
                            "name": "edata_omnis"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.odit",
                            "name": "edata_odit"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.quisquam",
                            "name": "edata_quisquam"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.consectetur",
                            "name": "edata_consectetur"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.ex",
                            "name": "edata_ex"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.necessitatibus",
                            "name": "edata_necessitatibus"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.praesentium",
                            "name": "edata_praesentium"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.totam",
                            "name": "edata_totam"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.occaecati",
                            "name": "edata_occaecati"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.molestias",
                            "name": "edata_molestias"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.velit",
                            "name": "edata_velit"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.quis",
                            "name": "edata_quis"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.eos",
                            "name": "edata_eos"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.ipsam",
                            "name": "edata_ipsam"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.repellat",
                            "name": "edata_repellat"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.ipsa",
                            "name": "edata_ipsa"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.officiis",
                            "name": "edata_officiis"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.doloremque",
                            "name": "edata_doloremque"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.suscipit",
                            "name": "edata_suscipit"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.vero",
                            "name": "edata_vero"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.illum",
                            "name": "edata_illum"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.ab",
                            "name": "edata_ab"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.error",
                            "name": "edata_error"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.saepe",
                            "name": "edata_saepe"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.natus",
                            "name": "edata_natus"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.adipisci",
                            "name": "edata_adipisci"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.quod",
                            "name": "edata_quod"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.commodi",
                            "name": "edata_commodi"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.facere",
                            "name": "edata_facere"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.optio",
                            "name": "edata_optio"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.libero",
                            "name": "edata_libero"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.veritatis",
                            "name": "edata_veritatis"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.nobis",
                            "name": "edata_nobis"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.itaque",
                            "name": "edata_itaque"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.dolorum",
                            "name": "edata_dolorum"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.rem",
                            "name": "edata_rem"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.quos",
                            "name": "edata_quos"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.vitae",
                            "name": "edata_vitae"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.ducimus",
                            "name": "edata_ducimus"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pariatur",
                            "name": "edata_pariatur"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.explicabo",
                            "name": "edata_explicabo"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.animi",
                            "name": "edata_animi"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.quae",
                            "name": "edata_quae"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.aperiam",
                            "name": "edata_aperiam"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.voluptates",
                            "name": "edata_voluptates"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.mollitia",
                            "name": "edata_mollitia"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.excepturi",
                            "name": "edata_excepturi"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.atque",
                            "name": "edata_atque"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.neque",
                            "name": "edata_neque"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.sapiente",
                            "name": "edata_sapiente"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.repellendus",
                            "name": "edata_repellendus"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.minima",
                            "name": "edata_minima"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.rerum",
                            "name": "edata_rerum"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.deleniti",
                            "name": "edata_deleniti"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.debitis",
                            "name": "edata_debitis"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.values[*].lhs",
                            "name": "edata_values_lhs"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.values[*].rhs",
                            "name": "edata_values_rhs"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.dir",
                            "name": "edata_dir"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].ver",
                            "name": "edata_items_ver"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].origin.id",
                            "name": "edata_items_origin_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].origin.type",
                            "name": "edata_items_origin_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].id",
                            "name": "edata_items_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].to.id",
                            "name": "edata_items_to_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].to.type",
                            "name": "edata_items_to_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].type",
                            "name": "edata_items_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].params[*].transfers",
                            "name": "edata_items_params[*]_transfers"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.items[*].params[*].count",
                            "name": "edata_items_params[*]_count"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.starttime",
                            "name": "edata_starttime"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.endtime",
                            "name": "edata_endtime"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.timespent",
                            "name": "edata_timespent"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pageviews",
                            "name": "edata_pageviews"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.interactions",
                            "name": "edata_interactions"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.envsummary[*].env",
                            "name": "edata_envsummary_env"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.envsummary[*].timespent",
                            "name": "edata_envsummary_timespent"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.envsummary[*].visits",
                            "name": "edata_envsummary_visits"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.eventssummary[*].id",
                            "name": "edata_eventssummary_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.eventssummary[*].count",
                            "name": "edata_eventssummary_count"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pagesummary[*].id",
                            "name": "edata_pagesummary_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pagesummary[*].type",
                            "name": "edata_pagesummary_type"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pagesummary[*].env",
                            "name": "edata_pagesummary_env"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pagesummary[*].timespent",
                            "name": "edata_pagesummary_timespent"
                        },
                        {
                            "type": "path",
                            "expr": "$.edata.pagesummary[*].visits",
                            "name": "edata_pagesummary_visits"
                        },
                        { "type": "path", "expr": "$.tags[*]", "name": "tags" },
                        {
                            "type": "path",
                            "expr": "$.syncts",
                            "name": "syncts"
                        },
                        {
                            "type": "path",
                            "expr": "$.@timestamp",
                            "name": "@timestamp"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.fcm_token",
                            "name": "devicedata_fcm_token"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.city",
                            "name": "devicedata_city"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.device_id",
                            "name": "devicedata_device_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.device_spec",
                            "name": "devicedata_device_spec"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.state",
                            "name": "devicedata_state"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.uaspec.agent",
                            "name": "devicedata_uaspec_agent"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.uaspec.ver",
                            "name": "devicedata_uaspec_ver"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.uaspec.system",
                            "name": "devicedata_uaspec_system"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.uaspec.raw",
                            "name": "devicedata_uaspec_raw"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.country",
                            "name": "devicedata_country"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.country_code",
                            "name": "devicedata_country_code"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.producer_id",
                            "name": "devicedata_producer_id"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.state_code_custom",
                            "name": "devicedata_state_code_custom"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.state_code",
                            "name": "devicedata_state_code"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.state_custom",
                            "name": "devicedata_state_custom"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.district_custom",
                            "name": "devicedata_district_custom"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.first_access",
                            "name": "devicedata_first_access"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.api_last_updated_on",
                            "name": "devicedata_api_last_updated_on"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.user_declared_district",
                            "name": "devicedata_user_declared_district"
                        },
                        {
                            "type": "path",
                            "expr": "$.devicedata.user_declared_state",
                            "name": "devicedata_user_declared_state"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.ets",
                            "name": "contentdata_ets"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.channel",
                            "name": "contentdata_channel"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.ownershipType[*]",
                            "name": "contentdata_ownershipType"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.code",
                            "name": "contentdata_code"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.description",
                            "name": "contentdata_description"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.organisation[*]",
                            "name": "contentdata_organisation"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.language[*]",
                            "name": "contentdata_language"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.mimeType",
                            "name": "contentdata_mimeType"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.idealScreenSize",
                            "name": "contentdata_idealScreenSize"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.createdOn",
                            "name": "contentdata_createdOn"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.appId",
                            "name": "contentdata_appId"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.contentDisposition",
                            "name": "contentdata_contentDisposition"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.lastUpdatedOn",
                            "name": "contentdata_lastUpdatedOn"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.contentEncoding",
                            "name": "contentdata_contentEncoding"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.contentType",
                            "name": "contentdata_contentType"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.dialcodeRequired",
                            "name": "contentdata_dialcodeRequired"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.creator",
                            "name": "contentdata_creator"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.createdFor[*]",
                            "name": "contentdata_createdFor"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.lastStatusChangedOn",
                            "name": "contentdata_lastStatusChangedOn"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.audience[*]",
                            "name": "contentdata_audience"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.IL_SYS_NODE_TYPE",
                            "name": "contentdata_IL_SYS_NODE_TYPE"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.visibility",
                            "name": "contentdata_visibility"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.os[*]",
                            "name": "contentdata_os"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.consumerId",
                            "name": "contentdata_consumerId"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.mediaType",
                            "name": "contentdata_mediaType"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.osId",
                            "name": "contentdata_osId"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.version",
                            "name": "contentdata_version"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.versionKey",
                            "name": "contentdata_versionKey"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.idealScreenDensity",
                            "name": "contentdata_idealScreenDensity"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.license",
                            "name": "contentdata_license"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.framework",
                            "name": "contentdata_framework"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.createdBy",
                            "name": "contentdata_createdBy"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.compatibilityLevel",
                            "name": "contentdata_compatibilityLevel"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.IL_FUNC_OBJECT_TYPE",
                            "name": "contentdata_IL_FUNC_OBJECT_TYPE"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.name",
                            "name": "contentdata_name"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.IL_UNIQUE_ID",
                            "name": "contentdata_IL_UNIQUE_ID"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.resourceType",
                            "name": "contentdata_resourceType"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.status",
                            "name": "contentdata_status"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.mid",
                            "name": "contentdata_mid"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.label",
                            "name": "contentdata_label"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.nodeType",
                            "name": "contentdata_nodeType"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.userId",
                            "name": "contentdata_userId"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.objectType",
                            "name": "contentdata_objectType"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.nodeUniqueId",
                            "name": "contentdata_nodeUniqueId"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.requestId",
                            "name": "contentdata_requestId"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.operationType",
                            "name": "contentdata_operationType"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.nodeGraphId",
                            "name": "contentdata_nodeGraphId"
                        },
                        {
                            "type": "path",
                            "expr": "$.contentdata.graphId",
                            "name": "contentdata_graphId"
                        }
                    ]
                }
            },
            "appendToExisting": False
        }
    }
}

DATASOURCES_LIST = {
    "ingestion-bm-5n-ds9-1": "records-5m-2",
    "ingestion-bm-5n-ds9-2": "records-5m-2",
    "ingestion-bm-5n-ds9-3": "records-5m-2",
    "ingestion-bm-5n-ds9-4": "records-5m-2",
    "ingestion-bm-5n-ds9-5": "records-5m-2",
    "ingestion-bm-5n-ds9-6": "records-5m-2",
    "ingestion-bm-5n-ds9-7": "records-5m-2",
    "ingestion-bm-5n-ds9-8": "records-5m-2",
    "ingestion-bm-5n-ds9-9": "records-5m-2",
    #"ingestion-bm-5n-ds10-10": "records-5m-2",
}
DRUID_HOST = "http://10.244.1.28:8888"

if __name__ == "__main__":
    for datasource, topic in DATASOURCES_LIST.items():
        spec_copy = spec
        spec_copy["spec"]["dataSchema"]["dataSource"] = datasource
        spec_copy["spec"]["ioConfig"]["topic"] = topic

        # Submit ingestion
        response = requests.post(
            f"{DRUID_HOST}/druid/indexer/v1/supervisor",
            json=spec_copy
        )
        response.raise_for_status()
