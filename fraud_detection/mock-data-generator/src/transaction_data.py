import json
from faker import Faker
from faker.providers import phone_number
from jsonschema import validate
from argparse import ArgumentParser
import pandas as pd

class MockTransactionGenerator:
    def __init__(self, json_schema):
        self.json_schema = json_schema
        self.fake = Faker(locale='en_IN')
        self.fake.add_provider(phone_number)
        self.index = 0
        self.occurance_ratio = 0
        self.sender_array = []
        self.receiver_array = []
        # Validate the JSON schema against a predefined schema for the schema itself
        schema_validator = json.loads('''
                {
                    "type": "array",
                    "items":  {
                    "type": "object",
                    "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "enum": {
                        "type": "array" 
                            },
                    "probability":{"type":"integer"},
                    "format": {"type": "string"},
                    "length": {"type": "integer"},
                    "min": {"type": "number"},
                    "max": {"type": "number"},
                    "start":{"type":"string"},
                    "end":{"type":"string"}
                },
                "required": ["name"]
            }
        }
        ''')
        validate(self.json_schema, schema_validator)
        self.load_name_ifsc_combinations()

    def load_name_ifsc_combinations(self):
        try:
            with open('../sample-files/account_profile.json', 'r') as file:
                for line in file:
                    self.sender_array.append(json.loads(line))
                    self.receiver_array.append(json.loads(line))
        except FileNotFoundError:
            self.name_ifsc_combinations = {}

    def generate_name_ifsc_combination(self, prdata):
        if(prdata==True):
            index = self.fake.random_int(0, len(self.sender_array)-1)
            ifsc = self.sender_array[index]['ifsc_code']
            accno = self.sender_array[index]['account_number']
            return ifsc, accno
        else:
            index = self.fake.random_int(0, len(self.receiver_array)-1)
            ifsc = self.receiver_array[index]['ifsc_code']
            accno = self.receiver_array[index]['account_number']
            return ifsc, accno
        
        
    def generate_vpa(self):
        random_platform = self.fake.bothify(text="?", letters=self.payment_platforms)
        return self.fake.user_name() + '@' + random_platform

    def generate_events(self, event_count):
        events = []
        event_count= int(event_count)
        for i in range(event_count):
            self.index = i
            self.occurance_ratio = ((i/event_count)*100)
            events.append(self.generate_event())
        return events

    def generate_data(self, field_schema, current_event):
        field_type = field_schema.get("type")
        if field_type == "string":
            return self.generate_string(field_schema, current_event)
        elif field_type == "number" or field_type == 'integer' or field_type == 'long':
            return self.generate_number(field_schema)
        elif field_type == "timestamp":
            return self.generate_date(field_schema)
        
   
    def generate_string(self, field_schema, current_event):  
        probability  = field_schema.get('probability', 100)
        if 'default' in field_schema and probability > self.occurance_ratio:
            if type(field_schema['default']) == 'list':
                return self.fake.bothify(text = '?', letters=field_schema['default'])
            else: 
                return field_schema['default']
        elif 'format' in field_schema: 
            enum = field_schema.get("enum", [])
            if field_schema['format'] == 'errorcode' and current_event.get('currstatusdesc') != 'FAILED':
                return "\\N"
            elif field_schema['format'] == 'errorcode' and current_event.get('currstatusdesc') == 'FAILED':
                return self.fake.bothify(text='?', letters=enum)
            else:
                match(field_schema['format']):
                    case 'name':
                        return self.fake.name()
                    case 'sha256':
                        return self.fake.sha256()
                    case 'address':
                        return self.fake.address().replace('\n', '  ')
                    case 'ipv4':
                        return self.fake.ipv4()
                    case 'md5':
                        return self.fake.md5()
                    case 'payervpa' | 'payeevpa':
                        return self.generate_vpa()
                    case 'phone_number':
                        return "+91" + self.fake.msisdn()[3:]
                    case 'coordinates':
                        return self.fake.latlng()
                    case _:
                        if len(enum)>0:
                            return str(self.fake.bothify(text = field_schema['format'], letters= enum))
                        else:
                            return str(self.fake.bothify(text= field_schema['format']))          
        else:
            return self.fake.word()

    def generate_number(self, field_schema):
        if 'length' in field_schema:
            length = field_schema.get("length", 15)
            return self.fake.random_number(digits=length)
        else:
            min_value = field_schema.get("min", 0)
            max_value = field_schema.get("max", 1000)
            return self.fake.random_int(min=min_value, max=max_value)

    def generate_date(self, field_schema):
        start_date = field_schema.get('start', '-3M')
        end_date = field_schema.get('end', 'now')
        date_obj = self.fake.date_time_between(start_date=start_date, end_date=end_date)
        formatted_time = '{}+05:30'.format(date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + date_obj.strftime('%z'))
        return formatted_time
    
    def generate_event(self):
        sender_ifsc_code, sender_account_number = self.generate_name_ifsc_combination(True)
        receiver_ifsc_code, receiver_account_number = self.generate_name_ifsc_combination(False)
        event = {'sender_ifsc_code': sender_ifsc_code, 'sender_account_number': sender_account_number, 
                'receiver_ifsc_code': receiver_ifsc_code, 'receiver_account_number': receiver_account_number, 
                'sender_contact_email': str(self.fake.email())}
        for field in self.json_schema:
            event[field["name"]] = self.generate_data(field, event)
        return event


def write_events_to_output(events, output_file):
    df = pd.DataFrame(events)
    df.to_json(output_file, lines=True, orient="records")
    
if __name__ == '__main__':
    parser = ArgumentParser('Mock Data Generator')
    parser.add_argument('-c', '--config_file', default='../data/transaction_schema.json', help='Specify a config file to use')
    parser.add_argument('-o', '--output_file', default='../sample-files/transaction_data.json', help='Specify the name of the output file')
    parser.add_argument('-n', '--event_count', type=int, default=1, help='Specify the number of events')
    args = parser.parse_args()
    file = open(args.config_file)
    json_schema = json.load(file)
    event_generator = MockTransactionGenerator(json_schema)
    events = event_generator.generate_events(args.event_count)
    write_events_to_output(events, args.output_file)
