import re


def group_tokens_by_type(tokens):
    grouped = {}

    for token in tokens:
        if token.type not in grouped:
            grouped[token.type] = []  # Eğer tür yoksa liste oluştur

        grouped[token.type].append(token)  # Token'i ekle

    return grouped
def run_code_in_terminal(code):
    # Yeni bir isim alanı oluştur
    local_vars = {}
    exec(code, {}, local_vars)  # exec ile kodu çalıştır
    return local_vars  # Değişkenleri döndür


class SemicolonExpectedError(SyntaxError):
    def __init__(self, message, line, column):
        super().__init__(message)
        self.line = line
        self.column = column
        self.__str__
    def __str__(self):
        return f"SemicolonExpectedError:Satır {self.line} de index {self.column} da noktali virgül bekleniyor"


class Token:
    def __init__(self,type_,value,index):
        self.type=type_
        self.value=value
        self.index=index
    def __repr__(self):
        return f"Token({self.type}, {self.value} , {self.index})"


class Lexer:
    def __init__(self,file_text):
        self.code=file_text
        self.tokens=[]
        self.tokenize()
        self.grouped = {}

    def tokenize(self):
        token_spec = [
            ("STR", r'"[a-zA-Z_][a-zA-Z0-9_]*"'),
            ("STR_2", r"'[a-zA-Z_][a-zA-Z0-9_]*'"),
            ("NUMBER", r"\d+"),  # Sayılar (örneğin: 123, 42)
            ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),  # Değişken, fonksiyon adları
            ("OP", r"[+\-*/]"),  # Operatörler (+, -, *, /)
            ("EQUALS", r"="),  # Atama operatörü (=)
            ("NEWLINE", r"\n"),  # Yeni satır karakteri
            ("SKIP", r"[ \t]+"),  # Boşlukları atla
            ("VİRGÜL", r","),
            ("NOKTALI_VİRGÜL", r";"),
            ("SÜSLÜ_PARANTEZ_ACIK", r"{"),
            ("SÜSLÜ_PARANTEZ_KAPALI", r"}"),
            ("SINIF", r"class"),
            ("function", r"function"),
            ("BAĞLAC", r"&"),
            ("PARANTEZ_ACIK", r"("),
            ("PARANTEZ_KAPALI", r")"),
            ("KÖSELI_PARANTEZ_ACIK", r"["),
            ("KÖSELI_PARANTEZ_KAPALI", r"]"),
            ("INCLUDE", r"::"),
            ("GET", r"<<"),
            ("SEND", r">>"),
            ("KUCUK_ISARETI", r"<"),
            ("BUYUK_ISARETI", r">"),
            ("PYTHON_CODE", r"//"),
        ]
        token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_spec)

        # Kaynak kodu satır satır tarayarak token'lara ayır
        for match in re.finditer(token_regex, self.code):
            kind = match.lastgroup  # Eşleşen token türü
            value = match.group()  # Eşleşen string değeri
            index=match.start()
            if kind == "SKIP":
                continue  # Boşlukları atla

            # Token nesnesini oluştur ve listeye ekle
            self.tokens.append(Token(kind, value,index))

    def get_tokens(self):
        return self.tokens
    def group_tokens_by_type(self):

        for token in self.tokens:
            if token.type not in self.grouped:
                self.grouped[token.type] = []  # Eğer tür yoksa liste oluştur

            self.grouped[token.type].append(token)  # Token'i ekle

        return self.grouped

    def get_group_token(self,category):
        try:
            if self.grouped !={}:
                return self.grouped[category]
            else:
                self.grouped=self.group_tokens_by_type()
                return self.grouped[category]
        except Exception:
            print(f"Girilen {category} isimli token mevcut değil başka token deneyin.")


class Parser:
    def __init__(self,tokens,exceptinon):
        self.tokens=tokens
        self.index=0
        self.variable={}
        self.exception=exceptinon

    def parse(self):
        while self.index <len(self.tokens):
            token = self.tokens[self.index]
            if token.type == "IDENTIFIER":
                if (self.index + 1 < len(self.tokens) and self.tokens[self.index + 1].type == "EQUALS"):
                    self.parse_variable()
            elif token.type == "SINIF":
                if self.index +1 <len(self.tokens) and self.tokens[self.index+1].type == "IDENTIFIER":
                    self.parse_class()
            elif token.value == "&":
                print(run_code_in_terminal(self.tokens[self.index+5].value))
            self.index+=1

    def parse_variable(self):
        if self.exception ==False:
            if self.tokens[self.index+2].type=="STR" or "STR_2":
                var_name=self.tokens[self.index].value
            if self.tokens[self.index+3].type == "OP" and self.tokens[self.index+3].value == "+":
                var_name=self.tokens[self.index].value
                if self.tokens[self.index+2].type =="IDENTIFIER":
                    firs_value = int(self.tokens[self.index + 2].value)
                else:
                    firs_value=int(self.tokens[self.index+2].value)
                if self.tokens[self.index + 4].type == "IDENTIFIER":
                    second_value = self.variable[self.tokens[self.index+4].value]
                else:
                    second_value = int(self.tokens[self.index + 4].value)
                self.variable[var_name]=int(firs_value)+int(second_value)
                self.index+=5
            elif self.tokens[self.index+3].type == "OP" and self.tokens[self.index+3].value == "-":
                var_name = self.tokens[self.index].value
                if self.tokens[self.index + 2].type == "IDENTIFIER":
                    firs_value = self.variable[var_name]
                else:
                    firs_value = int(self.tokens[self.index + 2].value)
                if self.tokens[self.index + 4].type == "IDENTIFIER":
                    second_value = int(self.variable[var_name])
                else:
                    second_value = int(self.tokens[self.index + 4].value)
                self.variable[var_name] = int(firs_value) - int(second_value)

            elif self.tokens[self.index + 3].type == "OP" and self.tokens[self.index+3].value == "/":
                var_name = self.tokens[self.index].value
                if self.tokens[self.index + 2].type == "IDENTIFIER":
                    firs_value = self.variable[var_name]
                else:
                    firs_value = int(self.tokens[self.index + 2].value)
                if self.tokens[self.index + 4].type == "IDENTIFIER":
                    second_value = int(self.variable[var_name])
                else:
                    second_value = int(self.tokens[self.index + 4].value)

                try:

                    self.variable[var_name] = int(firs_value) / int(second_value)
                except ZeroDivisionError as e:
                    print(f"ZeroDivisionError: {var_name} adlı değişkende 2.argüman 0 değerini almış ")

            elif (
                self.tokens[self.index + 3].type == "OP"
                and self.tokens[self.index + 3].value == "*"
            ):
                var_name=self.tokens[self.index].value
                if self.tokens[self.index + 2].type == "IDENTIFIER":
                    firs_value = self.variable[self.tokens[self.index+2].value]

                else:
                    firs_value = int(self.tokens[self.index + 2].value)
                if self.tokens[self.index + 4].type == "IDENTIFIER":
                    second_value = self.variable[self.tokens[self.index+4].value]
                else:
                    second_value = int(self.tokens[self.index + 4].value)
                self.variable[var_name] = int(firs_value) * int(second_value)

            elif self.tokens[self.index+2].type=="IDENTIFIER":
                var_name=self.tokens[self.index].value
                self.index+=2
                value=self.variable[self.tokens[self.index].value]
                self.variable[var_name]=value

            else:
                var_name=self.tokens[self.index].value
                self.index+=2
                value=self.tokens[self.index].value
                self.variable[var_name]=value

    def get_variable(self):
        return self.variable

class AST:
    pass

class Interpeter:
    def __init__(self,code):
        self.code=code
        self.line_number=0
        self.exceptinon=False

    def interpet(self):
        self.parse_line()

    def parse_line(self):
        lines=str(self.code).split("\n")
        for line in lines:
            self.read_line(line)
            self.line_number+=1

    def read_line(self, line):
        line = line.strip()  # Satırın başındaki ve sonundaki boşlukları temizle
        if not line:  # Eğer satır boşsa, hiçbir şey yapma
            return
        if not line.endswith(";"):
            column_index = len(line) + 1  # Hata mesajında doğru konumu belirtmek için
            print(SemicolonExpectedError("Noktalı virgül eksik ", self.line_number, column_index))
            self.exceptinon=True
class CompilerManager:
    pass


code = """& << "add";"""


interpeter=Interpeter(code)
interpeter.interpet()


lexer=Lexer(code)
parser=Parser(lexer.tokens,interpeter.exceptinon)
parser.parse()
print(parser.tokens[2].value)
