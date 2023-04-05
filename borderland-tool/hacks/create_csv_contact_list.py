#!/usr/bin/env python3
import re
import sys
import json

if len(sys.argv) != 2:
    print("Usage: python3 create_csv_contact_list.py <csv file>")
    sys.exit(1)

with open(sys.argv[1], newline='') as lottery_file:
    with open('contact_list.csv', 'w') as contact_list_file:
        contact_list_file.write("first_name;last_name;email\n")

        for line in lottery_file:
            line = re.sub(r"'([^']*)'([:,}])", r'"\1"\2', line)

            contact = json.loads(line)
            contact_list_file.write(f"{contact['first_name']};{contact['last_name']};{contact['email']}\n")
