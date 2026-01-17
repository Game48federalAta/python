
def ebob(a,b):
    num=1
    for i in range(a+1):
        if i>0:
            if a%i==0 and b%i==0:num =i

    return num
def ekok(a,b):
    return int(a/ebob(a,b) * b/ebob(a,b) *ebob(a,b))
def isAralarindaAsal(a,b):
    if ebob(a,b) ==1:return True
    else:return False

print(isAralarindaAsal(2356,6667))