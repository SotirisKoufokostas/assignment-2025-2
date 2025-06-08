class SparseTable:
    def __init__(self, nn, mm, k, x):
        self.nn = nn
        self.mm = mm
        self.k = k
        self.keys = [x]
        self.build_table()
        
    def build_table(self):
        self.n = len(self.keys)
        self.m = int(self.nn[self.k - 1] * self.mm[self.k - 1])
        self.table = [None] * self.m
        self.key_positions = {}

        sorted_keys = self.manual_sort(self.keys[:])
        q = self.m // self.n
        r = self.m % self.n

        idx = 0
        for i in range(self.n):
            count_r_prev = (i * r) // self.n
            count_r_next = ((i + 1) * r) // self.n
            extra = 1 if count_r_next > count_r_prev else 0
            total = q + extra

            for j in range(total):
                pos = (idx + j) % self.m
                self.table[pos] = sorted_keys[i]
                if j == total - 1:
                    self.key_positions[sorted_keys[i]] = pos
            idx += total

        min_key = min(sorted_keys)
        start_pos = self.key_positions[min_key]
        self.head = start_pos

        self.table = [self.table[(start_pos + i) % self.m] for i in range(self.m)]

        new_positions = {}
        for key, old_pos in self.key_positions.items():
            new_pos = (old_pos - start_pos) % self.m
            new_positions[key] = new_pos
        self.key_positions = new_positions

        self.authentic_positions = sorted(self.key_positions.values())
    
    def find_authentic_keys(self):
        auth_indices = []
        for i in range(self.m):
            if i == self.m - 1 or self.table[i] != self.table[i + 1]:
                auth_indices.append(i)
        return auth_indices
    
    def is_authentic(self, index):
        return index in self.authentic_positions

    def binary_search_insert_pos(self, value):
        authentic_values = [self.table[i] for i in self.authentic_positions]
        left, right = 0, len(authentic_values) - 1
        pos = 0
        while left <= right:
            mid = (left + right) // 2
            if authentic_values[mid] < value:
                pos = mid + 1
                left = mid + 1
            else:
                right = mid - 1
        return (self.authentic_positions[pos - 1] + 1) % self.m if pos > 0 else self.authentic_positions[0]

    def shift_right(self, start_index):
        i = start_index
        originals_to_move = []
        while self.is_authentic(i):
            originals_to_move.append(i)
            i = (i + 1) % self.m
            if i == start_index:
                self.k += 1
                self.build_table()
                return
        for idx in reversed(originals_to_move):
            next_idx = (idx + 1) % self.m
            self.table[next_idx] = self.table[idx]
            self.authentic_positions.remove(idx)
            self.authentic_positions.append(next_idx)
        self.authentic_positions.sort()

    def manual_sort(self, array):
        array.sort()
        return array

    def print_table(self):
        l = 0
        output = []
        for i in range(self.m):
            val = self.table[i - 1]
            if l == 0 and val == min(self.table):
                output.append(f">{val}<")
                l += 1
            else:
                output.append(str(val))
        print("[" + ", ".join(output) + "]")

    def insert(self, key):
        if key in self.keys:
            print(f"INSERT {key}")
            self.print_table()
            return

        if self.n + 1 > self.nn[self.k]:
            self.k += 1
            self.build_table()

        insert_pos = self.binary_search_insert_pos(key)
        if self.is_authentic(insert_pos):
            self.shift_right(insert_pos)
        self.table[insert_pos] = key
        self.authentic_positions.append(insert_pos)
        self.authentic_positions.sort()
        self.key_positions[key] = insert_pos

        self.keys = [self.table[i] for i in self.authentic_positions]
        self.keys.sort()
        self.n += 1

        print(f"INSERT {key}")
        self.print_table()
    
    def find_position(self, key):
        for i, pos in enumerate(self.authentic_positions):
            if key <= self.table[pos]:
                return pos
        return self.authentic_positions[-1] + 1 if self.authentic_positions else 0

    def lookup(self, key):
        print(f"LOOKUP {key}")
        for i, pos in enumerate(self.authentic_positions):
            if self.table[pos] == key:
                print(f"Key {key} found at position {(pos + 1) % self.m}.")
                self.print_table()
                return
            elif self.table[pos] > key:
                print(f"Key {key} not found. It should be at position {pos + 1}.")
                self.print_table()
                return

        if self.authentic_positions:
            pos = self.authentic_positions[-1] + 1
        else:
            pos = 0
        print(f"Key {key} not found. It should be at position {(pos + 1) % self.m}.")
        self.print_table()

    def delete(self, key):
        s = -1
        for i in range(self.m):
            if self.table[i] == key and self.table[(i - 1) % self.m] != key:
                s = i
                break

        if s == -1:
            print(f"DELETE {key}")
            self.print_table()
            return

        L = 1
        while L < self.m:
            next_idx = (s + L) % self.m
            if self.table[next_idx] != key:
                break
            L += 1

        next_real_idx = (s + L) % self.m
        next_val = self.table[next_real_idx]

        for i in range(L):
            self.table[(s + i) % self.m] = next_val

        if key in self.key_positions:
            del self.key_positions[key]

        self.keys = [k for k in self.keys if k != key]
        self.n = len(self.keys)
        self.positions = self.find_authentic_keys()

        if self.k > 1 and self.n <= self.nn[self.k - 2]:
            self.k -= 1
            self.build_table()

        print(f"DELETE {key}")
        self.print_table()

def main():
    data = {
        "nn": [1, 2, 5, 10, 15, 20],
        "mm": [2, 2.5, 2, 1.5, 1.33],
        "k": 1,
        "x": 3,
        "actions": [
            {"action": "insert", "key": 5},
            {"action": "insert", "key": 6},
            {"action": "insert", "key": 3},
            {"action": "insert", "key": 4},
            {"action": "insert", "key": 10},
            {"action": "insert", "key": 8},
            {"action": "insert", "key": 7},
            {"action": "lookup", "key": 10},
            {"action": "lookup", "key": 15},
            {"action": "lookup", "key": 5},
            {"action": "lookup", "key": 0},
            {"action": "delete", "key": 3},
            {"action": "delete", "key": 10},
            {"action": "delete", "key": 10},
            {"action": "delete", "key": 4},
            {"action": "delete", "key": 5},
            {"action": "lookup", "key": 6.5},
            {"action": "lookup", "key": 6},
            {"action": "delete", "key": 6},
            {"action": "delete", "key": 7}
        ]
    }

    print(f"CREATE with k={data['k']}, n_k={data['nn']}, m_k={data['mm']}, key={data['x']}↪")
    table = SparseTable(data["nn"], data["mm"], data["k"], data["x"])
    table.print_table()

    for action in data["actions"]:
        act = action["action"]
        key = action["key"]
        if act == "insert":
            table.insert(key)
        elif act == "lookup":
            table.lookup(key)
        elif act == "delete":
            table.delete(key)

if __name__ == "__main__":
    main()
