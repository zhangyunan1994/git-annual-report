import csv


def read_csv():
    path = "abc.csv"
    with open(path,"r") as f:

        csv_read = csv.reader(f)
        result = []
        for line in csv_read:
            result.append({
                "name": line[0],
                'url': line[1]
            })
        return result


if __name__ == '__main__':
    print(read_csv())
