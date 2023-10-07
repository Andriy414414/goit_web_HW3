import time
from multiprocessing import Pool, current_process, cpu_count


#
# def factorize(*numbers):
#
#     results = []  # Список для збереження результатів
#
#     for num in numbers:
#         divisors = []  # Список для збереження дільників
#         for i in range(1, num + 1):
#             if num % i == 0:
#                 divisors.append(i)
#
#         results.append((num, divisors))  # Зберігаємо результат
#
#
#
#     return results  # Повертаємо список результатів
#
#
# def callback(result):
#     print(result)
#
#
# if __name__ == '__main__':
#     start_time = time.time()
#     a = factorize(12800000, 254522645, 99999, 10651060)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"\ntime: {elapsed_time} seconds\n")
#     print(a) #- час 1.40 без pool для заданих чисел, час 41.5 без pool для більших чисел

def factorize_one_num(num):
    result_num = []
    for i in range(1, num + 1):
        if num % i == 0:
            result_num.append(i)

    return result_num


def callback(result):
    print(result)


def factorize(*numbers):
    print(f"Count CPU: {cpu_count()}")
    with Pool(cpu_count()) as p:
        results = p.map_async(factorize_one_num, numbers, callback=callback, )

        p.close()  # перестати виділяти процеси в пулл
        p.join()  # дочекатися закінчення всіх процесів
    return results.get()


if __name__ == '__main__':
    print("hello")
    start_time = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end_time = time.time()
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    elapsed_time = end_time - start_time

    print(f"\ntime: {elapsed_time} seconds\n")  # час 1.95 з pool для заданих чисел, час 33.6 з pool для більших чисел,

    print(a, b, c, d, sep="\n")
