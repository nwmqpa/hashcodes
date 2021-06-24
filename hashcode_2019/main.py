"""Main file for the hashcode application."""
import sys
import random
import json
from numba import jit, jitclass
from numba import int32, float32
import numba

spec = [
    ("number_vertical", int32),
    ("number_horizontal", int32),
    ("mean", float32)
]

print(spec)

def parse_file(file):
    """Parse file."""
    photos = []
    lines = file.split("\n")
    for line, index in zip(lines[1:-1], range(0, len(lines[1:-1]))):
        elems = line.split(" ")
        photos.append([
            index,
            True if elems[0] == 'V' else False,
            elems[2:]
        ])
    return photos


def parse_photos(photos):
    """Get the list of tags."""
    tags = {}
    for photo in photos:
        for tag in photo[2]:
            try:
                tags[tag] += 1
            except:
                tags[tag] = 1
    return tags


def parse_side(photos):
    """Get the side."""
    vertical = 0
    horizontal = 0
    for photo in photos:
        vertical += 1 if photo[1] else 0
        horizontal += 1 if not photo[1] else 0
    return vertical, horizontal


def parse_mean(photos):
    """Get the mean."""
    return sum([len(photo[2]) for photo in photos]) / len(photos)


def unparse_slides(slides):
    """Unparse slides."""
    data = "{}\n".format(len(slides))
    for slide in slides:
        if type(slide[0]) == type([]):
            data += "{} {}\n".format(slide[0][0], slide[0][1])
        else:
            data += "{}\n".format(slide[0])
    return data

@jit
def compute_photo(photo1, photo2):
    common = len(set(photo1[2]) & set(photo2[2]))
    s1 = len(photo1[2]) - common
    s2 = len(photo2[2]) - common
    return min([common, s1, s2])

@jit
def compute_vertical(photo1, photo2) -> int:
    return len(set(photo1[2]) & set(photo2[2]))

def couple_vertical(photos):
    all_photos = list(filter(lambda x: not x[1], photos)) 
    verticals = list(filter(lambda x: x[1], photos))
    while len(verticals):
        stats = list(map(lambda x: compute_vertical(verticals[0], x), verticals[1:]))
        vertical = verticals[0]
        vertical[0] = (vertical[0], verticals[1:][stats.index(min(stats))][0])
        verticals.pop(stats.index(min(stats)) + 1)
        verticals.pop(0)
        all_photos.append(vertical)
        print(len(verticals))
    return all_photos

@jitclass(spec)
class Application(object):
    """Class defining the hashcode application."""

    def __init__(self):
        """Initialize the application."""

    def parse_file(self):
        """Parse file."""
        try:
            with open(sys.argv[1], "r") as file:
                self.photos = parse_file(file.read())
                self.tags = parse_photos(self.photos)
                self.number_vertical, self.number_horizontal = parse_side(self.photos)
                self.mean = parse_mean(self.photos)
        except:
            print("Error")

    def make_stats(self):
        """Make stats."""
        photos = [self.photos[0]]
        dup_photos = json.loads(json.dumps(self.photos[1:]))
        while len(dup_photos):
            stats = list(map(lambda x: compute_photo(photos[-1], x), dup_photos))
            photos.append(dup_photos[stats.index(max(stats))])
            dup_photos.pop(stats.index(max(stats)))
            print(len(dup_photos))

        return photos

    def output_slides(self, slides):
        """Output photos."""
        try:
            with open(sys.argv[2], "w") as file:
                file.write(unparse_slides(slides))
        except:
            print("No file")

    def run(self):
        """Run the application."""
        self.parse_file()
        self.photos = couple_vertical(self.photos)
        slides = self.make_stats()
        self.output_slides(slides)

if __name__ == "__main__":
    app = Application()
    app.run()
