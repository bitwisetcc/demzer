import csv, requests

"""
Inserts sample data into the database.
1 - Spin up the server
2 - Execute this script
3 - GET http://localhost:8000/api/u/students
"""


def read_csv(file_name: str) -> list[dict]:
    with open(file_name) as f:
        data = csv.reader(f)
        keys = []
        res = []

        for i, row in enumerate(data):
            if i == 0:
                keys = row
            elif row:
                res.append(dict(zip(keys, row)))

        return res


def store(csv, endpoint, transform = lambda o: o):
    print(f"http://localhost:8000/api/{endpoint}")
    for obj in read_csv(f"samples/{csv}.csv"):
        data = transform(obj)
        requests.post(f"http://localhost:8000/api/{endpoint}", json=data)
        print("->", data)
        


if __name__ == "__main__":
    store("subjects", "subjects/new/")
    store("courses", "courses/new/", lambda o: {**o, "subjects": o["subjects"].split()})
    store("teachers", "u/register/", lambda o: {**o, "user_type": "2"})
    store("classes", "classes/new/")
    store("students", "u/register/", lambda o: {**o, "user_type": "0"})
    # presence
    # assessment

    print("done")
