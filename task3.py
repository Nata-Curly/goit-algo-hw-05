import timeit


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def compute_lps(pattern):
    """Алгоритм Кнута-Морріса-Пратта"""
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def build_shift_table(pattern):
    """Алгоритм Боєра-Мура"""
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def polynomial_hash(s, base=256, modulus=101):
    """Алгоритм Рабіна-Карпа"""
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i : i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def measure_performance(text, real_pattern, fake_pattern):
    algorithms = [kmp_search, boyer_moore_search, rabin_karp_search]
    results = {}

    for algorithm in algorithms:
        real_time = timeit.timeit(lambda: algorithm(text, real_pattern), number=100)
        fake_time = timeit.timeit(lambda: algorithm(text, fake_pattern), number=100)
        results[algorithm.__name__] = {
            "real_pattern_time": real_time,
            "fake_pattern_time": fake_time,
        }

    return results

text_article_1 = read_file("article1.txt")
text_article_2 = read_file("article2.txt")

real_pattern = "алгоритм"
fake_pattern = "штучний інтелект"

results_article_1 = measure_performance(text_article_1, real_pattern, fake_pattern)
results_article_2 = measure_performance(text_article_2, real_pattern, fake_pattern)

print("Results for Article 1:")
print(results_article_1)
print("\nResults for Article 2:")
print(results_article_2)
