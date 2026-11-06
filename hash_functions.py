# hash_functions.py
# all the hash functions i tried. i kept every one instead of deleting the old
# ones so i can still run the earlier attempts and compare them.


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
