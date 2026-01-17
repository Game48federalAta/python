import urllib.request
import re


def get_data(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode("ISO-8859-1")
    return data


def parser(label, data):
    result = []  # String birleştirme yerine liste kullanıyoruz
    c_label = "</" + label
    o_label = "<" + label
    while o_label in data:
        o_label_index = data.index(o_label)
        c_label_index = data.index(c_label, o_label_index) + len(c_label)
        ldata = data[o_label_index:c_label_index]
        result.append(ldata)  # Her parçayı listeye ekliyoruz
        data = data[:o_label_index] + data[c_label_index:]  # İşlenen kısmı çıkarıyoruz
    return result


def find(label, data):
    result = parser(label=label, data=data)
    return " ".join(
        result
    )  # Listenin elemanlarını tek bir string olarak birleştiriyoruz


data = get_data("https://www.google.com.tr/")
print(find("a", data))
