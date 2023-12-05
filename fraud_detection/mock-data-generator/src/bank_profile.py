import json
from faker import Faker
from faker.providers import phone_number
from argparse import ArgumentParser
import pandas as pd

class BankProfileMockGenerator:
    def __init__(self):
        self.fake = Faker(locale='en_IN')
        self.fake.add_provider(phone_number)
        self.index = 0
        self.acc_array=[]
        self.load_name_ifsc_combinations()
        self.bank_array=[]
        self.load_bank_details()
        self.bank_profiles=[]
        self.generate_bank_combination()
    
    def load_bank_details(self):
        try:
            with open('../data/bank_details.json', 'r') as file:
                self.bank_array = json.load(file)
        except FileNotFoundError:
            self.bank_array = []

    def load_name_ifsc_combinations(self):
        try:
            with open('../sample-files/account_profile.json', 'r') as file:
                for line in file:   
                    self.acc_array.append(json.loads(line))
        except FileNotFoundError:
            self.acc_array = []

    def generate_bank_combination(self):
        for index in range(0, len(self.acc_array)-1):
            temp_ifsc = self.acc_array[index]['ifsc_code'][:4]
            for item in range (0, len(self.bank_array)-1):
                if self.bank_array[item]['ifsc'] == temp_ifsc:
                    self.bank_profiles.append({
                        "ifsc_code": self.acc_array[index]['ifsc_code'],
                        "bank_name": self.bank_array[item]['name'],
                        "bank_code": self.bank_array[item]['ifsc']
                    })  
    def generate_events(self, event_count):
        self.event_count=event_count
        events = []
        event_count= int(event_count)
        for i in range(event_count-1):
            self.index=i
            event = self.generate_event()
            if event==None:
                continue
            events.append(event)
        return events

    def generate_event(self):
        bank_combination = self.bank_profiles[self.index]
        if bank_combination=={}:
            return None
        event = {'ifsc_code': bank_combination['ifsc_code'], 'bank_name': bank_combination['bank_name'], 
                'bank_code': bank_combination['bank_code'], 'branch_location': self.fake.city()}
        return event
    
def write_events_to_output(events):
    df = pd.DataFrame(events)
    df.to_json("../sample-files/bank_profile.json", lines=True, orient="records")

if __name__ == '__main__':
    parser = ArgumentParser('Mock Data Generator')
    parser.add_argument('-n', '--event_count', type=int, default=200, help='Specify the number of events')
    args = parser.parse_args()
    event_generator = BankProfileMockGenerator()
    events = event_generator.generate_events(args.event_count)
    write_events_to_output(events)
