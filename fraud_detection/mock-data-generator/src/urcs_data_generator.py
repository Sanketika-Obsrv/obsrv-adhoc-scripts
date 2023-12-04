import json
from faker import Faker
from faker.providers import phone_number
from jsonschema import validate
from argparse import ArgumentParser
import pandas as pd

class EventGenerator:
    def __init__(self, json_schema):
        self.json_schema = json_schema
        self.fake = Faker(locale='en_IN')
        self.fake.add_provider(phone_number)
        self.index = 0
        self.occurance_ratio = 0
        self.pr_array = []
        self.py_array = []
        self.payment_platforms = [
            'paytm',
            'googlepay',
            'phonepe',
            'amazonpay',
            'bhim',
            'mobikwik',
            'freecharge',
            'airtelbank',
            'yapl',
            'apl',
            'abfspay',
            'axisb',
            'rmhdfcbank',
            'okaxis',
            'oksbi',
            'okhdfcbank',
            'jupiteraxis',
            'indus',
            'ikwik',
            'pingpay'
            'ybl'
        ]
        self.bank_codes = [
        "ABHY",
        "ADCB",
        "AIBK",
        "ALLA",
        "ANDB",
        "ANZB",
        "ARBN",
        "BARB",
        "BBKM",
        "BKDN",
        "BMBL",
        "BMSB",
        "BNPA",
        "BOFA",
        "BOIN",
        "BOTM",
        "CBIN",
        "CCBL",
        "CBIH",
        "CITI",
        "CITB",
        "CIUB",
        "CNRB",
        "CORP",
        "CRPK",
        "DBSS",
        "DCBL",
        "DENA",
        "DEUT",
        "DHAN",
        "DLSC",
        "DLXB",
        "DNBC",
        "EIBI",
        "FBIN",
        "FSCB",
        "GBCB",
        "GSCB",
        "HDFC",
        "HSBC",
        "ICBK",
        "IDFB",
        "IDIB",
        "IDUK",
        "INDB",
        "INRB",
        "ISBK",
        "ITAU",
        "JAKA",
        "JNBA",
        "KACE",
        "KKBK",
        "KLGB",
        "KNSB",
        "KSCB",
        "KVCB",
        "KVGB",
        "LAVB",
        "MAHB",
        "MCBL",
        "MGCB",
        "MHCB",
        "MSCB",
        "MSCR",
        "NAIN",
        "NASB",
        "NKGS",
        "ORBC",
        "PMCB",
        "PSIB",
        "PUNB",
        "RATN",
        "RBCA",
        "SBBJ",
        "SBHY",
        "SBIN",
        "SBTR",
        "SCBL",
        "SIBL",
        "SMBC",
        "SRSR",
        "STBP",
        "SUCO",
        "SURY",
        "SVBL",
        "SYNB",
        "TMBL",
        "TNSC",
        "UCBA",
        "UCBS",
        "UOVB",
        "UTBI",
        "UTIB",
        "UTKS",
        "VIJB",
        "YESB"
    ]
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
            with open('./resources/pr.json', 'r') as file:
                self.pr_array = json.load(file)
            with open('./resources/py.json', 'r') as file:
                self.py_array = json.load(file)
        except FileNotFoundError:
            self.name_ifsc_combinations = {}

    def generate_name_ifsc_combination(self, prdata):
        if(prdata==True):
            index = self.fake.random_int(0, 199)
            name = self.pr_array[index]['name']
            ifsc = self.pr_array[index]['ifsc']
            accno = self.pr_array[index]['accno']
            return name, ifsc, accno
        else:
            index = self.fake.random_int(0, 199)
            name = self.py_array[index]['name']
            ifsc = self.py_array[index]['ifsc']
            accno = self.py_array[index]['accno']
            return name, ifsc, accno
        
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

    def generate_data(self, field_schema):
        field_type = field_schema.get("type")
        if field_type == "string":
            return self.generate_string(field_schema)
        elif field_type == "number" or field_type == 'integer' or field_type == 'long':
            return self.generate_number(field_schema)
        elif field_type == "timestamp":
            return self.generate_date(field_schema)
        
    def generate_ifsc(self):
        return self.fake.bothify(text='?', letters=self.bank_codes) + self.fake.bothify(text='0######')
    
    def generate_string(self, field_schema):  
        probability  = field_schema.get('probability', 100)
        if 'default' in field_schema and probability > self.occurance_ratio:
            if type(field_schema['default']) == 'list':
                return self.fake.bothify(text = '?', letters=field_schema['default'])
            else: 
                return field_schema['default']
        elif 'format' in field_schema: 
            enum = field_schema.get("enum", [])
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
                case 'ifsc':
                    return self.generate_ifsc()
                case 'phone_number':
                    return "+91" + self.fake.msisdn()[3:]
                case _:
                    if len(enum)>0:
                        return self.fake.bothify(text = field_schema['format'], letters= enum)
                    else:
                        return self.fake.bothify(text= field_schema['format'])
                    
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
        prname, prifsc, pracc = self.generate_name_ifsc_combination(True)
        pyname, pyifsc, pyacc = self.generate_name_ifsc_combination(False)
        event = {'praccname': prname, 'prifsccode': prifsc, 'praccno': pracc, 'pyaccname': pyname, 'pyifsccode': pyifsc, 'pyaccno': pyacc}
        for field in self.json_schema:
            event[field["name"]] = self.generate_data(field)
        return event


def write_events_to_output(events, output_file):
    df = pd.DataFrame(events)
    df.to_json(output_file, compression="gzip", lines=True, orient="records")


def main():
    parser = ArgumentParser('Mock Data Generator')
    parser.add_argument('-c', '--config_file', default='input.json', help='Specify a config file to use')
    parser.add_argument('-o', '--output_file', default='output.json', help='Specify the name of the output file')
    parser.add_argument('-n', '--event_count', type=int, default=1, help='Specify the number of events')
    args = parser.parse_args()
    file = open(args.config_file)
    json_schema = json.load(file)
    event_generator = EventGenerator(json_schema)
    # Generate events
    events = event_generator.generate_events(args.event_count)
    # Write events to the output JSON file
    write_events_to_output(events, args.output_file)

if __name__ == '__main__':
    main()
