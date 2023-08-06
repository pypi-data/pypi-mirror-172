# This is a sample Python script.
import math
import random
from .cakes import cakes as get_cakes


def main():
    cakes = get_cakes()
    print(cakes[math.floor(random.Random().random()*len(cakes))])


if __name__ == '__main__':
    main()
