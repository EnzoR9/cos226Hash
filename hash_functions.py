# hash_functions.py
# all the hash functions i tried. i kept every one instead of deleting the old
# ones so i can still run the earlier attempts and compare them.

# python ints never overflow, so the good hashes use this to stay at 32 bits
# (same thing that happens automatically in java or c)
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


# ATTEMPT 3 - first 3 characters only (bad on purpose)
# treats the first 3 characters like a base 128 number and ignores the rest.
# different from the sum because order matters, but tons of keys start the
# same way. the quotes only have 78 different starts (718 start with "Pro")
# and 375 titles start with "The", so huge groups land on the same spot.
# results: title 5,629,514 collisions, quote 5,960,729 collisions (yikes)
def first_three_hash(key):
    h = 0
    for ch in key[:3]:
        h = h * 128 + ord(ch)
    return h


# ATTEMPT 4 - FNV-1a (good)
# start at a big fixed number, then for each character XOR it in and multiply
# by the FNV prime. different from the polynomial one because it XORs then
# multiplies instead of multiplying then adding. it's a real hash people use
# because it's fast and spreads out short similar strings well.
# results: title 38,096 collisions, quote 21,329 collisions
def fnv1a_hash(key):
    h = 2166136261
    for ch in key:
        h = h ^ ord(ch)
        h = (h * 16777619) & MASK
    return h


# ATTEMPT 5 - FNV-1a + an extra mixing step
# runs FNV-1a and then the "finalizer" from MurmurHash3, which shuffles the
# bits around so every input bit affects every output bit. used with the tail
# pointer version of the linked list table (see hash_tables.py).
# results: title 7,092 collisions, quote 5,567 collisions
def fnv1a_mixed_hash(key):
    h = fnv1a_hash(key)
    h = h ^ (h >> 16)
    h = (h * 0x85EBCA6B) & MASK
    h = h ^ (h >> 13)
    h = (h * 0xC2B2AE35) & MASK
    h = h ^ (h >> 16)
    return h
