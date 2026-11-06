# COS 226 - Hash Something Out

Two hash tables for 15,000 fake movies from `MOCK_DATA.csv`. Table 1 uses the movie title as the key and table 2 uses the quote. Each commit is one attempt at a different hash table setup, and the program prints wasted space, collisions, and build time for both tables.

## How to run

```
python main.py      # every attempt
python main.py 2    # just attempt 2
```

(`python3` on Mac.) `MOCK_DATA.csv` needs to be in the same folder. No extra packages needed.

## Files

* `main.py` - loads the csv, builds the tables for each attempt, prints the stats
* `hash_tables.py` - the hash table classes
* `hash_functions.py` - every hash function I tried, with comments on each one

## How I measured things

* **Collisions:** every time I look at a spot and something's already there. In a linked list, walking past 4 nodes to get to the end counts as 4.
* **Wasted space:** empty buckets/slots left after all 15,000 movies are in.
* **Build time:** only the time to insert everything, not reading the file. It changes a little every run, but collisions and wasted space are the same every time.
* After building, every movie gets looked up again to make sure the table actually works (the "lookup test" line).

## Stuff I noticed in the data

* Only 11,309 of the 15,000 titles are unique, so a lot of titles repeat. I keep every movie instead of overwriting duplicates.
* About 3,500 titles have commas in them, so a plain `split(",")` breaks. I used the `csv` module instead.
* One "quote" is around 49,000 characters long. It doesn't break anything, it just takes longer to hash.

## Results

Linked list tables have 15,013 buckets.
Linear probing tables have 20,011 slots (about 75% full).

| # | Attempt | Table | Collisions | Wasted space | Longest chain/probe | Build time |
|---|---|---|---:|---:|---:|---:|
| 1 | Linked list + character sum (bad) | Title | 45,598 | 11,262 (75.0%) | 25 | ~15 ms |
| 1 | | Quote | 56,718 | 12,290 (81.9%) | 22 | ~22 ms |
| 2 | Linked list + polynomial (good) | Title | 12,118 | 7,063 (47.0%) | 10 | ~25 ms |
| 2 | | Quote | 7,650 | 5,555 (37.0%) | 7 | ~40 ms |
| 3 | Linear probing + first 3 chars (bad) | Title | 5,629,514 | 5,011 (25.0%) | 7,042 | ~260 ms |
| 3 | | Quote | 5,960,729 | 5,011 (25.0%) | 4,686 | ~270 ms |

## Screenshots

![Attempt 1](screenshots/attempt-1.png)
![Attempt 2](screenshots/attempt-2.png)
![Attempt 3](screenshots/attempt-3.png)

## Reflection

### Attempt 1: linked list + character sum

I started with a bad hash on purpose so I'd have something to compare against. Adding up the characters gives really small numbers (most titles land around 1,500), so most of the table never gets used. 75% of the title buckets and 82% of the quote buckets were empty, and the longest chain was 25. It was still fast though, since adding numbers is about as cheap as a hash gets.

### Attempt 2: linked list + polynomial hash

Same table, but the hash multiplies by 31 before adding each character, so where a letter is actually matters. This cut collisions by about 73% for titles and 87% for quotes. There are still around 40% empty buckets, but from what I read that's normal for chaining when you have about as many buckets as keys, even with a really good hash. Titles had more collisions than quotes because duplicate titles always end up in the same bucket no matter what. It was a little slower to build since there's more math per character.

### Attempt 3: linear probing + first 3 characters

I switched to linear probing and tried a different kind of bad hash that only looks at the first 3 letters. Wasted space dropped to 25% because I sized the table myself, but collisions went over 5.6 million. Hundreds of quotes start with the same few letters ("Pro", "Syn", etc.), so they all want the same spot, spill into the next ones, and form huge clusters. One insert had to step over 7,042 full slots. It was also about 10 times slower than everything else.
