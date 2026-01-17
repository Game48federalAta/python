from pathlib import Path


hash_alfabe={
    "A":"01","a":"02","B":"12","b":"15","C":"03",
    "D":"56","d":"45","E":"44","e":"06","F":"55",
    "f":"07","G":"08","g":"09","Ğ":"11","ğ":"13",
    "H":"14","h":"78","I":"88","ı":"16","İ":"79",
    "i":"33","J":"17","j":"21","K":"27","k":"20",
    "L":"22","l":"26","M":"25","m":"30","N":"90",
    "n":"66","O":"65","o":"69","Ö":"67","ö":"64",
    "P":"80","p":"81","R":"82","r":"85","S":"83",
    "s":"23","Ş":"87","ş":"84","T":"89","t":"86",
    "U":"51","u":"56","Ü":"57","ü":"59","V":"60",
    "v":"71","Y":"58","y":"77","Z":"41","z":"42",
    "W":"43","w":"46","X":"62","x":"63","0":"00",
    "1":"99","2":"98","3":"96","4":"97","5":"95",
    "6":"91","7":"93","8":"92","9":"94","_":"24",
    "-":"28","'":"29","^":"31","+":"32","-":"34",
    "*":"35","/":"36","?":"38","(":"37",")":"39",
    ",":"49",";":"48",":":"47","<":"40",">":"53",
    "|":"61","{":"73","}":"74","&":"75","%":"68",
    "#":"18","$":"19",'!':"70",'"':"54","[":"52",
    "]":"50","\n":"72","=":"76"," ":"b0","\t":"b1",
    "é":"bb","10":"b2"



}

class Hash:
    def __init__(self,hash_value,hash_alphet=None):
        self.hash_alphet=hash_alphet
        if len(hash_value) %2 !=0:
            hash_value=hash_value+"é"
        self.hashing_value=self.hash_(hash_value)
        self.decode_value=""
    def hash_(self,content):
        for i in content:
            if self.hash_alphet==None:
                if i in hash_alfabe:
                    content = content.replace(i, hash_alfabe[i])
                else:raise ValueError(f"Karakter {i} tanımlanmamış")
            elif self.hash_alphet !=None and type(self.hash_alphet)==dict:
                if i in self.hash_alphet:content=content.replace(i,self.hash_alphet[i])
                else:raise ValueError(f"Karakter {i} tanımlanmamış")
        return content
    def find_dict_keys_value(self,value):
        if self.hash_alphet ==None:
            for anahtar, values in hash_alfabe.items():
                if values == value:
                    return anahtar
            raise ValueError(f"{value} Değer e karşılık gelen bir anahtar yok")
        elif self.hash_alphet !=None and type(self.hash_alphet)==dict:
            for anahtar, values in self.hash_alphet.items():
                if values == value:
                    return anahtar
            raise ValueError(f"{value} Değer e karşılık gelen bir anahtar yok")


    def decode_(self,content):
        if self.hash_alphet==None:
                bloklar = [content[i:i+2] for i in range(0, len(content), 2)]
                for i in bloklar:
                    if i=="bb":continue
                    self.decode_value+=self.find_dict_keys_value(i)
        elif self.hash_alphet !=None and type(self.hash_alphet)==dict:
            bloklar = [content[i:i+2] for i in range(0, len(content), 2)]
            for i in bloklar:
                self.decode_value+=self.find_dict_keys_value(i)
        return self.decode_value

def read_file(filepath):
    with open(filepath,"r") as file:
        data=file.read()
    return data

def get_size(filepath):
    file_size=Path(filepath).stat().st_size
    return f"{file_size} byte"

def create_file(filename,content):
    with open(filename,"w") as file:
        file.writelines(content)

veri=Hash("10selam")
create_file("example.pt",veri.hashing_value)
print(get_size("example.pt"))

print(veri.decode_(veri.hashing_value))