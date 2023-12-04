import json
from datetime import datetime

import redis2
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.functions import RuntimeContext, MapFunction


conf = {
	"kafka": {
        "brokers": "obsrv-kafka-headless.kafka.svc.cluster.local:9092",
  		"source_topic": "financial_data_nov",
  		"sink_topic": "transformed.financial_data_nov"
  	},
	"redis": {
		"host": "obsrv-redis-master.redis.svc.cluster.local",
		"port": 6379,
		"db": 3
	}
}

class FraudDetector(MapFunction):
	def open(self, runtime_context: RuntimeContext):
		self.r = redis2.Redis(host=conf['redis']['host'], port=conf['redis']['port'], db=conf['redis']['db'])
		self.ctx = runtime_context.get_metrics_group()
		return super().open(runtime_context)

	def map(self, value):
		event = json.loads(value)
		redis_data = self.r.get(event['sender_account_number'])
		if redis_data is None:
			metadata = {
				"fraud_processed": "False", 
				"isFraud": "False",
				"description": "Profile not found"
			}
		else:
			fraud_profile = json.loads(redis_data)
			# DT like rules:
			# if receiver account is not active
			try:
				if event["receiver_account_details"]["account_status"] != "ACTIVE":
					metadata = {
						"fraud_processed": "True", 
						"isFraud": "True",
						"severity": "Severe",
						"description": "Receiver is a suspected mule account."
					}
					# If txn amount is higher than the net spend across 3 months
				elif event["txn_amount"] >= fraud_profile["net_amount_spent"]:
					if (datetime.now() - fraud_profile["latest_txn_date"]).days > 30:
						metadata = {
							"fraud_processed": "True", 
							"isFraud": "True",
							"severity": "Severe",
							"description": "High spend from an dormant amount."
						}
					else:
						metadata = {
							"fraud_processed": "True", 
							"isFraud": "True",
							"severity": "Severe",
							"description": "Transaction amount higher than net spend."
						}
				# if txn amount is higher than 3 std dev of daily avg amount
				elif event["txn_amount"] >= ((3 * fraud_profile["std_dev_net_amount_spent"]) + fraud_profile["daily_avg_amount_spent"]):
					metadata = {
						"fraud_processed": "True", 
						"isFraud": "True",
						"severity": "Medium",
						"description": "Transaction amount considerably higher than daily average spend."
					}
				# If daily avg cashflow is close to 0
				elif (fraud_profile["daily_avg_cashflow"] > 10000) and (fraud_profile["daily_avg_cashflow"] < -10000):
					metadata = {
						"fraud_processed": "True", 
						"isFraud": "True",
						"severity": "Medium",
						"description": "High transactions yet low cashflow."
					}
				# If daily avg transaction count is high
				elif fraud_profile["daily_avg_transactions"] > 50:
					metadata = {
						"fraud_processed": "True", 
						"isFraud": "True",
						"severity": "Low",
						"description": "High daily avg transactions."
					}
			except KeyError:
				metadata = {
					"fraud_processed": "False", 
					"isFraud": "False",
					"description": "metric unavailable."
				}
			except TypeError:
				metadata = {
					"fraud_processed": "False", 
					"isFraud": "False",
					"description": "metric unavailable."
				}
		# None of rules satisifed, hence not a fraud
			else:
				metadata = {
					"fraud_processed": "True", 
					"isFraud": "False"
				}
		event["meta"] = metadata
		if metadata["isFraud"] == "True":
			self.ctx.add_group("txn_type", "fraud_txn").add_group("txn_id",event["txn_id"]).counter("txn_count").inc(1)
		updatedValue = json.dumps(event, separators=(',', ':'))
		return updatedValue

	def close(self):
		return super().close()


def main():
	env = StreamExecutionEnvironment.get_execution_environment()
	deserialization_schema = SimpleStringSchema()
	serialization_schema = SimpleStringSchema() 
	kafka_consumer = FlinkKafkaConsumer(
	    topics=conf['kafka']['source_topic'],
	    deserialization_schema=deserialization_schema,
	    properties={'bootstrap.servers': conf['kafka']['brokers'], 'group.id': 'processor_python_group', 'auto.offset.reset': 'earliest'})
	kafka_sink = FlinkKafkaProducer(
        topic=conf['kafka']['sink_topic'],
        serialization_schema=serialization_schema,
        producer_config={'bootstrap.servers': conf['kafka']['brokers'], 'group.id': 'producer_group'})
	ds = env.add_source(kafka_consumer)
	ds.map(FraudDetector(), output_type=Types.STRING()).add_sink(kafka_sink)
	env.execute('fraud-detector')

if __name__ == '__main__':
    main()
