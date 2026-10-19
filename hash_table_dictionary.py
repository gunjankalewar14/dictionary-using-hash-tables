"""Interactive word dictionary implemented with a hash table and chaining."""


class HashTableDictionary:
    """A small educational hash table that resolves collisions by chaining."""

    def __init__(self, capacity=7, max_load_factor=0.75):
        self.capacity = capacity
        self.max_load_factor = max_load_factor
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    @staticmethod
    def normalize(word):
        return word.strip().casefold()

    def _hash(self, key):
        """Compute a simple polynomial hash for demonstrating bucket mapping."""
        value = 0
        for character in key:
            value = (value * 31 + ord(character)) % self.capacity
        return value

    def _bucket_index(self, key):
        return self._hash(key)

    @property
    def load_factor(self):
        return self.size / self.capacity

    def put(self, word, meaning):
        """Add a word or update its meaning; return whether it was new."""
        key = self.normalize(word)
        if not key:
            raise ValueError("The word cannot be empty.")
        if not meaning.strip():
            raise ValueError("The meaning cannot be empty.")

        index = self._bucket_index(key)
        bucket = self.buckets[index]
        for position, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket[position] = (key, meaning.strip())
                return False

        bucket.append((key, meaning.strip()))
        self.size += 1
        if self.load_factor > self.max_load_factor:
            self._resize()
        return True

    def get(self, word):
        """Return the meaning, or None if the normalized word is absent."""
        key = self.normalize(word)
        if not key:
            return None
        for stored_key, meaning in self.buckets[self._bucket_index(key)]:
            if stored_key == key:
                return meaning
        return None

    def remove(self, word):
        """Remove and return True if the word existed."""
        key = self.normalize(word)
        if not key:
            return False
        bucket = self.buckets[self._bucket_index(key)]
        for position, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                del bucket[position]
                self.size -= 1
                return True
        return False

    def entries(self):
        """Return all word-meaning pairs in alphabetical word order."""
        all_entries = [entry for bucket in self.buckets for entry in bucket]
        return sorted(all_entries, key=lambda entry: entry[0])

    def bucket_contents(self):
        """Return bucket contents for demonstrating collisions."""
        return self.buckets

    def _resize(self):
        old_entries = [entry for bucket in self.buckets for entry in bucket]
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        for key, meaning in old_entries:
            self.buckets[self._bucket_index(key)].append((key, meaning))


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def show_menu():
    print("\n=== Hash Table Dictionary ===")
    print("1. Add a word or update its meaning")
    print("2. Search for a word")
    print("3. Remove a word")
    print("4. Display all words")
    print("5. Show hash-table buckets")
    print("6. Exit")


def display_entries(dictionary):
    entries = dictionary.entries()
    if not entries:
        print("The dictionary is empty.")
        return

    print("\nWord                 Meaning")
    print("-" * 62)
    for word, meaning in entries:
        print(f"{word:<20} {meaning}")


def display_buckets(dictionary):
    print("\nHash-table buckets (words in the same bucket are collisions)")
    for index, bucket in enumerate(dictionary.bucket_contents()):
        words = ", ".join(word for word, _ in bucket) if bucket else "(empty)"
        print(f"Bucket {index:>2}: {words}")
    print(f"Entries: {dictionary.size} | Capacity: {dictionary.capacity} | "
          f"Load factor: {dictionary.load_factor:.2f}")


def main():
    dictionary = HashTableDictionary()

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            word = read_non_empty("Enter the word: ")
            meaning = read_non_empty("Enter its meaning: ")
            try:
                was_new = dictionary.put(word, meaning)
                action = "Added" if was_new else "Updated"
                print(f"{action} the meaning for '{word}'.")
            except ValueError as error:
                print(error)
        elif choice == "2":
            word = read_non_empty("Enter the word to search: ")
            meaning = dictionary.get(word)
            if meaning is None:
                print(f"'{word}' was not found.")
            else:
                print(f"{word}: {meaning}")
        elif choice == "3":
            word = read_non_empty("Enter the word to remove: ")
            if dictionary.remove(word):
                print(f"Removed '{word}' from the dictionary.")
            else:
                print(f"'{word}' was not found.")
        elif choice == "4":
            display_entries(dictionary)
        elif choice == "5":
            display_buckets(dictionary)
        elif choice == "6":
            print("Exiting the dictionary. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
