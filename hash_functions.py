# hash_functions.py
# all the hash functions i tried. i kept every one instead of deleting the old
# ones so i can still run the earlier attempts and compare them.

# python ints never overflow, so the good hashes use this to stay at 32 bits
MASK = 0xFFFFFFFF


# ATTEMPT 1 - character sum (bad on purpose)
# just adds up the character codes. order doesn't matter so "stop" and "pots"
# get the same hash, and the numbers are way too small. the average title only
# adds up to around 1,500 and the average quote around 3,300, so most of the
# 15,013 buckets can never get anything in them.
# results: title 45,598 collisions / 75% empty, quote 56,718 collisions / 82% empty
def sum_hash(key):
    total = 0
    for ch in key:
        total += ord(ch)
    return total


# ATTEMPT 2 - polynomial rolling hash (good)
# h = 31*h + char for every character. now every character gets a different
# weight depending on where it is, so anagrams don't collide anymore and the
# number gets big fast which spreads keys over the whole table. 31 is what
# java's String.hashCode() uses (it's an odd prime so it doesn't lose bits).
# results: title 12,118 collisions / 47% empty, quote 7,650 collisions / 37% empty
def polynomial_hash(key):
    h = 0
    for ch in key:
        h = (31 * h + ord(ch)) & MASK
    return h
