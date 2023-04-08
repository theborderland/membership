#!/usr/bin/env python3

import csv
import sys

if len(sys.argv) != 2:
    print("Usage: python3 split_registrations.py <csv file>")
    sys.exit(1)

with open(sys.argv[1], newline='') as lottery_file:
    with open('regular_memberships.csv', 'w') as regular_memberships_file:
        with open('low_income_memberships.csv', 'w') as low_income_memberships_file:
            registered = csv.DictReader(lottery_file)
            low_income_memberships_file.write("id,email,first_name,last_name,dob,low_income,timestamp,ip,cookie,browser\n")
            regular_memberships_file.write("id,email,first_name,last_name,dob,low_income,timestamp,ip,cookie,browser\n")
            for line in registered:
                if eval(line['low_income']):
                    low_income_memberships_file.write(f"""{line['id']},{line['email']},"{line['first_name']}","{line['last_name']}",{line['dob']},{line['low_income']},{line['timestamp']},{line['ip']},{line['cookie']},"{line['browser']}"\n""")
                else:
                    regular_memberships_file.write(f"""{line['id']},{line['email']},"{line['first_name']}","{line['last_name']}",{line['dob']},{line['low_income']},{line['timestamp']},{line['ip']},{line['cookie']},"{line['browser']}"\n""")
