
import mygraph


def main():
    G = mygraph.DirectedGraph(
        V = {i for i in range(10)},
        E = {(1,5), (2,8), (4,9), (5,1), (7,3), (7,2)},
        C = {
            (1,5): 10,
            (2,8): 100,
            (4,9): 13,
            (5,1): 45,
            (7,3): 9,
            (7,2): 1,
        },
        F = {},
        W = {}
    )
    pass


if __name__ == "__main__":
    main()
