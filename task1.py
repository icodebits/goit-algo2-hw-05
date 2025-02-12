import mmh3
import bitarray

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size                                            # Розмір бітового масиву
        self.num_hashes = num_hashes                                # Кількість хеш-функцій
        self.bit_array = bitarray.bitarray(size)
        self.bit_array.setall(0)
    
    #Генеруємо декілька хешів для заданого елемента
    def _hashes(self, item):
        hashes = []
        for i in range(self.num_hashes):
            hash_value = mmh3.hash(item, i) % self.size
            hashes.append(hash_value)
        return hashes
    
    #Додаємо елемент у фільтр Блума
    def add(self, item):
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1
    
    #Перевіряємо, чи може елемент бути у фільтрі Блума
    def __contains__(self, item):
        return all(self.bit_array[hash_value] for hash_value in self._hashes(item))

#Перевіряє унікальність паролів за допомогою фільтра Блума
def check_password_uniqueness(bloom_filter, passwords):
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "некоректний пароль"
            continue
        
        if password in bloom_filter:
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None, "   "]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
