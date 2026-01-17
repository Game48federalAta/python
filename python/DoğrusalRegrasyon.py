import functools
class ListError(Exception):
    def __init__(self,list_x:list,list_y:list ):
        self.list_x=list_x
        self.list_y=list_y
        self.msg()
    def msg(self):
        if len(self.list_x) > len(self.list_y):
            lens = "".join(str(self.list_x))
            print("File 'D:\python\DoğrusalRegrasyon.py'")
            print(self.list_x)
            print("^" * (lens.index("]") + 1))
            print("ListError: liste 1[x] liste 2[y] den fazla düzeltmelisin regrasyon hesaplamak için eşit olması gerek")
        else:
            lens="".join(str(self.list_y))
            print(
                "File 'D:\python\DoğrusalRegrasyon.py'"
            )
            print(" ",self.list_y)
            print(" ","^"*(lens.index("]")+1))
            print("ListError: Liste 2[y] liste 1[x] den büyük regrasyon hesaplanması için eşit olması gerekir")


def LinearRegrassion(x:list,y:list):
    add_x=0
    add_y=0
    mul_res=0
    karesi_x=0
    eğim=0
    kesişim=0
    if len(x)==len(y):
        for i in range(len(x)):
            add_x+=x[i]
            add_y+=y[i]
            mul_res +=x[i]*y[i]
            karesi_x+=x[i]**2
        eğim = ((len(x) * mul_res) - (add_x * add_y)) / (
            (len(x) * karesi_x) - (add_x**2)
        )
        kesişim += (add_y - (eğim * add_x)) / len(x)
    else:
        ListError(x,y)
    return eğim,kesişim


def PropertyLinearRegarassion(x:tuple,y:tuple):
    kesişim = 0
    katsayılar = []
    args_ort_x = []
    args_ort_y = []

    for i in range(len(list(x))):
        args_ort_x.append(sum(x[i]) / len(x[i]))
    for i in range(len(list(y))):
        args_ort_y.append(sum(y[i]) / len(y[i]))

    # Katsayıları hesapla
    for i in range(len(x)):
        sapma_x = [(xi - args_ort_x[i]) for xi in x[i]]
        sapma_y = [(yi - args_ort_y[i]) for yi in y[i]]

        # Katsayıyı hesapla (eğim)
        pay = sum([sx * sy for sx, sy in zip(sapma_x, sapma_y)])
        payda = sum([sx**2 for sx in sapma_x])
        katsayı = pay / payda
        katsayılar.append(katsayı)

    # Kesişim noktası
    kesişim = args_ort_y[0] - sum(
        [katsayılar[i] * args_ort_x[i] for i in range(len(katsayılar))]
    )

    return kesişim, katsayılar


def predict(x,eğim,kesişim,özellikli=False):
    if not özellikli:return kesişim +eğim*x
    else:
        if isinstance(x, (int, float)):
            return kesişim + sum([e * x for e in eğim])
        # Eğer x bir liste ise, her bir eleman için tahmin yap
        elif isinstance(x, list):
            return [kesişim + sum([e * xi for e, xi in zip(eğim, x)])]


# Örnek veriler
x = ([1, 2, 3], [1, 2, 43, 5, 567, 567])
y = ([1, 2, 3, 4], [1, 2, 3, 4, 5])

# Hesaplama
eğim, kesişim = LinearRegrassion([1, 2, 3, 4], [2, 4, 5, 5])
kesişim, katsayılar = PropertyLinearRegarassion(x, y)

# Tahmin yapma
x_test = [2024, 555]
predictions=[]
for i in katsayılar:
    predictions.append(predict(x_test, i, kesişim,True))
print(predictions)
