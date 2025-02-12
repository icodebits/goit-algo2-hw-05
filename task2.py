import json
import timeit
import hyperloglog
from tabulate import tabulate

LOG_FILE_PATH = 'lms-stage-access.log'

# Завантаження IP-адрес із лог-файлу
def load_ips_from_log(file_path):
    unique_ips = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                ip = log_entry.get("remote_addr")
                if ip:
                    unique_ips.add(ip)
            except json.JSONDecodeError:
                continue                                            # Ігноруємо некоректні рядки
    return unique_ips

# Точний підрахунок унікальних IP-адрес
def exact_count(ips):
    return len(set(ips))

# Підрахунок унікальних IP-адрес за допомогою HyperLogLog
def hyperloglog_count(ips):
    hll = hyperloglog.HyperLogLog(0.01)                             # 1% похибка
    for ip in ips:
        hll.add(ip)
    return len(hll)

if __name__ == "__main__":
    ips = load_ips_from_log(LOG_FILE_PATH)
    
    # Вимірювання продуктивності та збереження результатів
    exact_result = None
    hll_result = None
    
    def measure_exact():
        global exact_result
        exact_result = exact_count(ips)
    
    def measure_hll():
        global hll_result
        hll_result = hyperloglog_count(ips)
    
    exact_time = timeit.timeit(measure_exact, number=100)
    hll_time = timeit.timeit(measure_hll, number=100)
    
    # Результати
    results = [["Унікальні елементи", exact_result, hll_result],
               ["Час виконання (сек.)", round(exact_time, 6), round(hll_time, 6)]]
    print("Результати порівняння:")
    print(tabulate(results, headers=["", "Точний підрахунок", "HyperLogLog"]))
