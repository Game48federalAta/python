import time


alfabe=["a","b","c","ç","d","e","f","g","ğ","h","i","j","k","l","m","n","o","ö","p","r","s","ş","t","u","ü","v","y","z"]
# sezar şifreleme mesala a harfini girdik onun 3 kademe ilerisindeki harf d |örnek ata = dvd
def şifrele(data):
    şifre=[]
    for i in data:
        şifre.append(alfabe[alfabe.index(i)+3])
    else:return ''.join(şifre)

print(şifrele("ssaaaaaaaaaaaaaaaaaaaafghjkljuşs"))
print(time.time())