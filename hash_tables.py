# hash_tables.py
# the hash table classes.
#
# collisions are counted: any time i look at a spot
# and something is already there, that's 1 collision. so walking past 4 nodes
# in a linked list to get to the end = 4 collisions.
#
# duplicate keys don't overwrite each other. there are only 11,309 different
# titles out of 15,000 movies, so every movie gets its own node/slot and get()
# just returns the first match.


class Node:
    def __init__(self, key, movie):
        self.key = key
        self.movie = movie
        self.next = None


# linked list (chaining) table: every bucket is the start of a linked list
class ChainingTable:
    def __init__(self, size, hash_func):
        self.size = size
        self.hash_func = hash_func
        self.buckets = [None] * size
        self.count = 0
        self.collisions = 0

    def insert(self, key, movie):
        index = self.hash_func(key) % self.size
        new_node = Node(key, movie)
        self.count += 1

        # empty bucket, no collision
        if self.buckets[index] is None:
            self.buckets[index] = new_node
            return

        # bucket is taken so walk to the end of the list
        current = self.buckets[index]
        self.collisions += 1
        while current.next is not None:
            current = current.next
            self.collisions += 1
        current.next = new_node

    def get(self, key):
        current = self.buckets[self.hash_func(key) % self.size]
        while current is not None:
            if current.key == key:
                return current.movie
            current = current.next
        return None

    def wasted_space(self):
        empty = 0
        for b in self.buckets:
            if b is None:
                empty += 1
        return empty

    def longest(self):
        longest = 0
        for b in self.buckets:
            length = 0
            while b is not None:
                length += 1
                b = b.next
            if length > longest:
                longest = length
        return longest

    def name(self):
        return "linked list (chaining)"
