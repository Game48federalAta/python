
def parser_file(filepath,contents,new_contents):
    with open(filepath,"r") as f:
        f=str(f.read()).replace(contents,new_contents)
    with open(filepath,"w") as fs:
        fs.write(str(f))

def run_file(file_path):
    with open(file_path,"r") as f:
        source=f.read()

        compile_code=compile(source,file_path,"exec")

        return exec(compile_code)

keyword={
    "IF":"if",
    "back":"return",
    "#use::":"import",
    ");":")",
    "){":"):",
    "} ":"",
    "#define":"def",
    "PRINT(":"print(",
    '");':')',
    "FOR":"for",
    "ELS{":"else:"
}
file="D:\\python\\te.txt"
for i in keyword:
    parser_file(file,i,keyword[i])
run_file(file)