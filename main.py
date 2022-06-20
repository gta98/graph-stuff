
from graph import *


def main():
    G = DirectedGraph(
        V = {i for i in range(10)},
        E = {(1,5), (2,8), (4,9), (5,1), (7,3), (7,2)},
        C = {
            (4,9): 8,
            (5,1): 11
        }
    )
    pass


if __name__ == "__main__":
    main()
