import json
from faker import Faker
from faker.providers import phone_number
import pandas as pd
from argparse import ArgumentParser


class AccountProfileMockGenerator:
    def __init__(self):
        self.fake = Faker(locale="en_IN")
        self.fake.add_provider(phone_number)
        self.index = 0
        self.occurance_ratio = 0
        self.active_account_prob = 80
        self.event_count = 1
        self.bank_codes = [
             "ANDB",
             "ARBN",
             "BARB",
             "BOIN",
             "CBIN",
             "CNRB",
             "CORP",
             "FBIN",
             "HDFC",
             "IDFB",
             "INRB",
             "ISBK",
             "KKBK",
             "KVCB",
             "SBHY",
             "SBIN",
             "SIBL",
             "UCBS",
             "UTIB",
             "SYNB"
        ]
        self.account_type_enum=["CURRENT", "SAVINGS"]
        self.account_status_enum=["ON_HOLD", "SUSPENDED", "CLOSED"]
        
    def generate_name_ifsc_combination(self):
        ifsc = self.fake.bothify(text="?", letters=self.bank_codes) + self.fake.bothify(
            text="0######"
        )
        name = self.fake.name()
        accno = self.fake.bothify(text="###############")
        return name, ifsc, accno

    def generate_events(self, event_count):
        self.event_count = event_count
        events = []
        event_count = int(event_count)
        for i in range(event_count):
            self.index = i
            self.occurance_ratio = (i / event_count) * 100
            events.append(self.generate_event())
        return events

    def get_account_status(self):
        if self.active_account_prob > self.occurance_ratio:
            return "ACTIVE"
        else:
            return self.fake.bothify(
                text="?", letters=self.account_status_enum
            )

    def generate_event(self):
        account_name, ifsc_code, account_number = self.generate_name_ifsc_combination()
        event = {
            "account_name": account_name,
            "ifsc_code": ifsc_code,
            "account_number": account_number,
            "account_type": self.fake.bothify(text="?", letters=self.account_type_enum),
            "account_status": self.get_account_status(),
        }
        return event

def write_events_to_output(events):
    df = pd.DataFrame(events)
    df.to_json("../sample-files/account_profile.json", lines=True, orient="records")

if __name__ == "__main__":
    parser = ArgumentParser("Mock Data Generator")
    parser.add_argument(
        "-n", "--event_count", type=int, default=1, help="Specify the number of events"
    )
    args = parser.parse_args()
    event_generator = AccountProfileMockGenerator()
    events = event_generator.generate_events(args.event_count)
    write_events_to_output(events)
