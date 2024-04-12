## Obsrv Open source test suite

This is a test suite for the Obsrv open source project. It is designed to test the functionality of the Obsrv project and to ensure that it is working as expected. The test suite is designed to be run on a variety of different platforms and operating systems, and is designed to be easily extensible and customizable.

### Pre-requisites
- Python 3.6 or higher
- requests library

### Installation
- Clone the repository
- Install the required dependencies using the following command:
```code
pip install requests
```

### Configuring the test suite

The test suite is configured using a python file called `config.py`. This file contains the configuration settings for the test suite, such as the URL of the Obsrv server.

```
API_HOST
DRUID_HOST
ROUTES
```
The respective routes for the `API` and `Druid` are to be provided.
In the routes, the endpoints for the respective operations to be populated and `SUBMIT_INGESTION` is a druid service endpoint, as at the time of implementation. Submit ingestion was not part of the API, so we used druid routes.

### Configuring datasets

- The dataset schema files are present under `stubs/schemas/datasets`
- Similarly schema files for `master-datasets` are present under `stubs/schemas/master-datasets`

The schemas follow a specific format, which is used to generate the test data for the test suite. The schema files are written in JSON format, and contain the following fields:

```json
{
    "id": "name to identify the dataset in obsrv system",
    "data_key": "key in the data which can be used for possible denorm operations",
    "ts_key": "key in the data which can be used for ingestion based on event occurence time",
    "denorm_config": "array of fields which define what denorms are to be done for the datasets",
    "schema": "JSON Schema for the dataset for performing validations on the data",
    "ingestion_spec": "Ingestion spec to be used for ingesting data into druid"
}
```

### Configuring defaults

- The default values such as redis hosts and ports are present under `resources/defaults.py`
- The above file consists default values for both the `datasets` and `datasources`

## IMPORTANT
- By default the datasets are in a Live status which makes them available for realtime data ingestion and querying which are capabilities of obsrv system.
- Please export the kubeconfig, before running the test suite, as the test suite uses the kubernetes client to interact with the obsrv system.
- The test suite interacts with the obsrv system for refreshing the cache so the system can start processing of events according to dataset configurations.
- If the cluster does not have loadbalancers available for remote access of `API` and `Druid`. The services can be port-forwarded and respective urls can be updated in `config.py` 

### Running the test suite
To run the test suite, simply run the following command in the root directory of the project:

```code
python app.py
```
