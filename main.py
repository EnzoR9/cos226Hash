# COS 226 - Hash
# Author: Enzo Russillo
#
# Loads the 15,000 fake movies from MOCK_DATA.csv and builds two hash tables for
# each attempt: one with the movie title as the key and one with the quote as
# the key. After each table is built it prints the stats
# for wasted space, collisions, build time plus a few extra ones that helped
# me understand what was going on (load factor, longest chain/probe, and a
# lookup test to make sure every movie can be found again)
#
# Each attempt is one table type + one hash function (see hash_functions.py):
#   1 - linked list + character sum hash (bad)
#
# Table sizes:
#   linked list: first prime >= number of movies (15,013) so ~1 movie per bucket
# I used primes because hash % size spreads keys out better with a prime size.
#
# Edge cases in the data: titles with commas are wrapped in quotes, one title
# has "" inside it, some titles have accented letters, and one quote is about
# 49,000 characters long. The csv module takes care of the quoting, the file
# is read as utf-8, blank/broken rows get skipped, and a movie with an empty
# title or quote just gets left out of that one table.
#
# How to run:
#   python main.py        all attempts
#   python main.py 3      just attempt 3
import csv
import sys
import time

from hash_functions import *
from hash_tables import *

FILENAME = "MOCK_DATA.csv"
TITLE = 0   # column numbers in the csv
QUOTE = 8
DEBUG = False


def load_movies(filename):
    movies = []
    skipped = 0
    csv.field_size_limit(1000000)  # one quote is huge, just in case

    with open(filename, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return movies, skipped

        for row in reader:
            # skip blank lines
            if len(row) == 0:
                continue
            # skip rows that don't have all 9 columns
            if len(row) != 9:
                skipped += 1
                if DEBUG:
                    print("skipped row:", row)
                continue

            row = [x.strip() for x in row]
            movies.append(row)

    #print(movies[0])
    return movies, skipped


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def next_prime(n):
    while not is_prime(n):
        n += 1
    return n


def build_and_print(label, table, movies, col):
    # time just the building part
    start = time.perf_counter()
    for movie in movies:
        table.insert(movie[col], movie)
    build_ms = (time.perf_counter() - start) * 1000

    # make sure every movie can actually be found again
    found = 0
    for movie in movies:
        result = table.get(movie[col])
        if result is not None and result[col] == movie[col]:
            found += 1

    wasted = table.wasted_space()
    if found == len(movies):
        test = "PASS"
    else:
        test = "FAIL"

    print()
    print(label)
    print("  table type:      ", table.name())
    print("  table size:      ", format(table.size, ","))
    print("  movies inserted: ", format(table.count, ","))
    print("  load factor:     ", round(table.count / table.size, 3))
    print("  wasted space:    ", format(wasted, ","), "empty spots",
          "(" + str(round(100 * wasted / table.size, 1)) + "%)")
    print("  collisions:      ", format(table.collisions, ","))
    print("  avg per insert:  ", round(table.collisions / table.count, 2))
    print("  longest run:     ", format(table.longest(), ","))
    print("  build time:      ", round(build_ms, 2), "ms")
    print("  lookup test:     ", found, "/", len(movies), "found -", test)


def run_attempt(num, titles, quotes):
    chain_size = next_prime(max(len(titles), len(quotes)))

    if num == 1:
        desc = "linked list + character sum hash (bad)"
        table1 = ChainingTable(chain_size, sum_hash)
        table2 = ChainingTable(chain_size, sum_hash)
    else:
        print("no attempt", num)
        return

    print()
    print("=" * 60)
    print("ATTEMPT " + str(num) + ": " + desc)
    print("=" * 60)
    build_and_print("Hash Table 1 (key = movie title)", table1, titles, TITLE)
    build_and_print("Hash Table 2 (key = movie quote)", table2, quotes, QUOTE)


def main():
    filename = FILENAME
    which = 0  # 0 means run all of them
    for arg in sys.argv[1:]:
        if arg.isdigit():
            which = int(arg)
        else:
            filename = arg

    try:
        movies, skipped = load_movies(filename)
    except FileNotFoundError:
        print("couldn't find", filename, "- put it in the same folder as main.py")
        return

    if len(movies) == 0:
        print("no movies found in", filename)
        return

    # movies with an empty title/quote can't go in that table
    titles = [m for m in movies if m[TITLE] != ""]
    quotes = [m for m in movies if m[QUOTE] != ""]

    print("loaded", format(len(movies), ","), "movies from", filename,
          "(" + str(skipped) + " bad rows skipped)")
    print("usable titles:", format(len(titles), ","), " usable quotes:", format(len(quotes), ","))

    if which != 0:
        run_attempt(which, titles, quotes)
    else:
        run_attempt(1, titles, quotes)


main()
