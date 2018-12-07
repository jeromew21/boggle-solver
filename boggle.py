import random
from collections import namedtuple
from populate import sqlite3, DB, LETTERS

CUBES = (
    list("rulwig"),
    ["qu"] + list("jobam"),
    list("ivgetn"),
    list("yelguk"),
    list("zadven"),
    list("yifeeh"),
    list("dacpem"),
    list("todkun"),
    list("newsod"),
    list("smahor"),
    list("siphen"),
    list("putles"),
    list("tilbay"),
    list("lascre"),
    list("coitaa"),
    list("xirfob"),
)

class Boggle:

    def __init__(self):
        indexes = list(range(16))
        random.shuffle(indexes)
        self.board = [[random.choice(CUBES[indexes.pop(0)]) for _ in range(4)] for _ in range(4)] #naive board
    
    def show(self):
        def pad(r):
            if len(r) == 1:
                return r + ""
            return r
        print("--")
        print("\n".join(" ".join(pad(r)) for r in self.board))
        print("--")
    
    def paths(self):
        DIRS = (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1), #^STRAIGHTS \/ DIAGONALS
            (-1, 1),
            (1, -1),
            (1, 1),
            (-1, -1),
        )
        Node = namedtuple("Node", ["coords", "character", "parent", "path"])
        size = 4
        for y, row in enumerate(self.board):
            for x, character in enumerate(row):
                queue = []
                queue.append(Node((x, y), character, None, []))
                while queue:
                    node = queue.pop(0)
                    if len(node.path) > 5:
                        break
                    for dx, dy in DIRS:
                        child_coords = (node.coords[0]+dx, node.coords[1]+dy)
                        if child_coords[0] < 0 or child_coords[0] >= size or child_coords[1] < 0 or child_coords[1] >= size:
                            continue
                        if child_coords not in node.path:
                            child = Node(child_coords, self.board[child_coords[1]][child_coords[0]], node, node.path + [node.coords])
                            queue.append(child)
                            word = ""
                            while child:
                                word = child.character + word
                                child = child.parent
                            yield word

    def words(self):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        for path in self.paths():
            c.execute("SELECT value FROM commonwords WHERE value = ?", (path,))
            fetch = c.fetchone()
            if fetch:
                yield fetch[0]
        conn.commit()
        conn.close()

if __name__ == "__main__":
    num_words_observed = []
    for i in range(100):
        b = Boggle()
        b.show()
        num_words = len(list(b.words()))
        print(f"Has {num_words} words")
        num_words_observed.append(num_words)
        print(f"Average: {sum(num_words_observed) / len(num_words_observed)}")