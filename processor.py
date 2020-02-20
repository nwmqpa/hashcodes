import sys
import json


def process_input(file: str):
    with open(file, "r") as f:
        data = f.read()
    data = list(filter(len, data.split("\n")))
    new_data = {
        "books": int(data[0].split(" ")[0]),
        "libraries_nb": int(data[0].split(" ")[1]),
        "days": int(data[0].split(" ")[2]),
        "books_scores": list(map(int, data[1].split(" "))),
        "libraries": [{
            "books_nb": int(d1.split(" ")[0]),
            "signup_days": int(d1.split(" ")[1]),
            "books_per_day": int(d1.split(" ")[2]),
            "books": list(map(int, d2.split(" ")))
        } for d1, d2 in zip(data[2::2], data[3::2])]
    }
    return new_data



if __name__ == "__main__":
    data = process_input(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(json.dumps(data))
