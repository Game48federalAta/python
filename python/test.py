import asyncio
import time
import sys
def squares_normal():
    return [i**2 for i in range(1, 2501)]


def squares_generator():
    for i in range(1, 2501):
        yield i**2


async def squares_async():
    return [i**2 for i in range(1, 2501)]

# 1. Normal fonksiyonun hafıza kullanımı ve hızı
start_time = time.time_ns()
normal_result = squares_normal()
normal_time = (time.time_ns() - start_time)/1_000_000
normal_memory = sys.getsizeof(normal_result)

# 2. yield kullanan jeneratör fonksiyonun hafıza kullanımı ve hızı
start_time = time.time_ns()
gen = squares_generator()
all_squares=list(gen)
generator_time = (time.time_ns() - start_time) / 1_000_000
generator_memory = sys.getsizeof(gen)

# 3. Asenkron fonksiyonun hafıza kullanımı ve hızı
start_time = time.time_ns()
async_result = asyncio.run(squares_async())
async_time = (time.time_ns() - start_time) /1_000_000
async_memory = sys.getsizeof(async_result)

# Sonuçları yazdır
print(f"Normal fonksiyon - Zaman: {normal_time} ms, Hafıza: {normal_memory} bytes")
print(
    f"Jeneratör fonksiyon - Zaman: {generator_time} ms, Hafıza: {generator_memory} bytes"
)
print(f"Asenkron fonksiyon - Zaman: {async_time} ms, Hafıza: {async_memory} bytes")
