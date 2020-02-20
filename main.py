import sys

def process_input(file: str):
    with open(file, "r") as f:
        data = f.read()
    return data


def main(data):
    pass


if __name__ == "__main__":
    data = process_input(sys.argv[1])
    data = main(data)
    process_output(data, sys.argv[2])