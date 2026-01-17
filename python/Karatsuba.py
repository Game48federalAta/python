def karatsuba(x, y):
    # Sayılar küçükse normal çarpma kullan
    if x < 10 or y < 10:
        return x * y

    # Basamak sayısını belirle
    n = max(len(str(x)), len(str(y)))
    m = n // 2  # Sayıyı ortadan böl

    # Sayıları parçala
    a, b = divmod(x, 10**m)
    c, d = divmod(y, 10**m)

    # Karatsuba adımları
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    ad_plus_bc = karatsuba(a + b, c + d) - ac - bd

    # Sonucu birleştir
    return (10 ** (2 * m) * ac) + (10**m * ad_plus_bc) + bd


# Örnek kullanım
x = 56897
y = 56464
print(karatsuba(x, y))

