#!/usr/bin/env python3
import csv
import sys

if len(sys.argv) != 2:
    print("Usage: python3 create_csv_contact_list.py <csv file>")
    sys.exit(1)

with open(sys.argv[1], newline='') as lottery_file:
    with open('contact_list.csv', 'w') as contact_list_file:
        registered = csv.DictReader(lottery_file)
        contact_list_file.write("first_name;last_name;email\n")
        for line in registered:
            contact_list_file.write(f"{line['first_name']};{line['last_name']};{line['email']}\n")
