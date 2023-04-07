import csv
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 filter_cheaters.py <csv file>")
        sys.exit(1)

    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        seen = set()
        print("id,email,first_name,last_name,dob,low_income,timestamp,ip,cookie,browser")
        for row in reader:
            key = (row['first_name'], row['last_name'], row['dob'], row['cookie'])
            if key not in seen:
                seen.add(key)
                print(f"{row['id']},{row['email']},{row['first_name']},{row['last_name']},{row['dob']},{row['low_income']},{row['timestamp']},{row['ip']},{row['cookie']},{row['browser']}".format(row))


if __name__ == '__main__':
    main()
