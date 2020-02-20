import sys
import json

"""

"""


def preprocess_data(data):
    result = [str(len(data["libraries"]))]
    for library in data["libraries"]:
        result += [
            "{} {}".format(library["id"], len(library["books"])),
            " ".join(map(str, library["books"]))
        ]
    return "\n".join(result)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        data = json.loads(f.read())
    #data = main(data)
    data = {
        "libraries": [
            {
                "id": 0,
                "books": [0, 1, 2, 3, 4]
            },
            {
                "id": 1,
                "books": [5]
            }
        ]
    }
    data = preprocess_data(data)
    with open(sys.argv[2], "w") as f:
        f.write(data)
