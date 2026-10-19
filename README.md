# Case Study 4: A Dictionary Application Using Hash Tables

**Course:** PCC-201-COM – Data Structures and Algorithms  
**Unit:** IV – Hashing  
**Prepared by:** Gunjan Maruti Kalewar · Roll No. 44 · Division B · Batch B

## 1. Abstract

A dictionary application stores words and their meanings and lets a user look up a word quickly. A hash table maps each key to a bucket using a hash function. Collisions occur when different keys map to the same bucket, so the design needs a collision-resolution strategy. This case study uses **separate chaining** to explain insertion, search, deletion, resizing, load factor, and the difference between a teaching implementation and Python's built-in dictionary.

## 2. Scenario and data model

A small offline glossary stores a word, its definition, and optionally a part of speech. The word is the key; the record containing definition and metadata is the value. A user can add a new word, search for a word, update its definition, remove an entry, and list all entries alphabetically.

Before hashing, the application may normalize case and trim surrounding whitespace, so `Queue`, `queue`, and ` queue ` map to the same logical key. Whether accents, punctuation, or plural forms are normalized must be a product decision; over-normalizing can merge words that should remain distinct.

## 3. Hash-table design

For a teaching version, create an array of `m` buckets. A hash function maps a word to a nonnegative integer, then the bucket index is `hash(word) mod m`. Each bucket is a linked collection of key-value entries. When two keys have the same index, both entries remain in that bucket; the application compares the full keys to find the correct one.

```text
PUT(word, meaning):
    key = NORMALIZE(word)
    index = HASH(key) mod bucket_count
    search bucket[index] for key
    if found: replace its meaning
    else: append (key, meaning) to bucket[index]

GET(word):
    key = NORMALIZE(word)
    index = HASH(key) mod bucket_count
    search bucket[index] for key
    return its meaning, or NOT_FOUND
```

A collision is expected behavior, not an error. For example, if a small table has 7 buckets and `hash("apple") mod 7` and `hash("grape") mod 7` both equal 3, the bucket at index 3 stores both entries and compares keys during lookup.

## 4. Load factor and performance

The **load factor** is `α = number_of_entries / number_of_buckets`. With a well-distributed hash function and controlled load factor, insertion, lookup, and deletion are expected to take **O(1)** on average. If many keys collide into one bucket, an operation can degrade to **O(n)**. Resizing allocates more buckets and redistributes entries; the resize itself takes O(n), but when performed occasionally, insertion remains amortized O(1) across a sequence of updates.

The CPython implementation of `dict` is a resizable hash table, but its internal collision strategy is not the separate-chaining design shown here. The custom bucket design is for explaining collision resolution; an ordinary Python application should generally use `dict` instead of reimplementing it. [Python's design FAQ describes dictionaries as resizable hash tables](https://docs.python.org/3/faq/design.html).

## 5. Functional and security considerations

- Distinguish “word not found” from an empty definition.
- Decide whether adding an existing word overwrites, appends a sense, or asks the user.
- Keep key equality checks after hash calculation; a hash value alone does not identify a word.
- Resize when the selected load-factor threshold is exceeded.
- Use a robust, well-tested hash implementation. Poor hash distributions harm performance; untrusted keys can create denial-of-service risks in poorly designed systems.
- Persist the glossary separately from the in-memory table and validate imported records.
- Alphabetical display requires sorting and is typically O(n log n), even if key lookup is expected O(1).

## 6. Conclusion

A dictionary is a natural use for a hash table because users search by a key and expect a corresponding value. Separate chaining makes collisions visible and illustrates how a table can preserve multiple entries that map to the same bucket. The case study also shows why load factor, resizing, equality checks, and key normalization matter—and why real applications should prefer a mature built-in dictionary unless hash-table implementation is itself the learning objective.

## 7. Runnable Python implementation

The accompanying [`hash_table_dictionary.py`](hash_table_dictionary.py) program implements a small dictionary with a custom hash table and separate chaining. Its menu supports adding or updating a meaning, searching, deleting, listing entries, and displaying bucket collisions. It starts with an empty in-memory table; entries are cleared when the program exits.

Run it from this folder with:

```bash
python3 hash_table_dictionary.py
```

## References

1. Python Software Foundation, [Design and History FAQ: dictionaries and hash tables](https://docs.python.org/3/faq/design.html).
2. Carter, J. L., and Wegman, M. N., [“Universal Classes of Hash Functions,” Journal of Computer and System Sciences, 18(2), 1979](https://doi.org/10.1016/0022-0000(79)90044-8).
3. Morin, P., *Open Data Structures*, [Hash Tables](https://opendatastructures.org/ods-java/5_Hash_Tables.html).
