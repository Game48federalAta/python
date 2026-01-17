import math


def KNN(*args: tuple, tahmin: tuple,predict_with_class=False,class_name:dict=None):
    mesafeler = []
    if predict_with_class==False:
        for veri_noktası in args:
            if len(veri_noktası) != len(tahmin):
                raise ValueError("Veri noktası ve tahmin noktası aynı uzunlukta olmalıdır")

            # Euclidean mesafeyi hesapla
            mesafe = math.sqrt(
                sum((tahmin[i] - veri_noktası[i]) ** 2 for i in range(len(tahmin)))
            )
            mesafeler.append(mesafe)

        # En küçük mesafeyi ve ilgili veri noktasını bul
        en_yakın_index = mesafeler.index(min(mesafeler))
        en_yakın_veri_noktası = args[en_yakın_index]

        return en_yakın_veri_noktası
    elif predict_with_class==True and type(class_name) !=None and type(class_name)==dict:
        for veri_noktası in args:
            if len(veri_noktası) != len(tahmin):
                raise ValueError(
                    "Veri noktası ve tahmin noktası aynı uzunlukta olmalıdır"
                )

            # Euclidean mesafeyi hesapla
            mesafe = math.sqrt(
                sum((tahmin[i] - veri_noktası[i]) ** 2 for i in range(len(tahmin)))
            )
            mesafeler.append(mesafe)

        # En küçük mesafeyi ve ilgili veri noktasını bul
        en_yakın_index = mesafeler.index(min(mesafeler))
        en_yakın_veri_noktası = args[en_yakın_index]

        return f"{en_yakın_veri_noktası} verisi şu sınıfa ait {list(class_name)[en_yakın_index]}"
