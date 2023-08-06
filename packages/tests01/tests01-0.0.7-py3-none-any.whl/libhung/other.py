def snt(a):
    """kiểm tra số nguyên tố"""
    kt = True
    if a == 0 or a == 1:
            kt = False
    elif a == 2:
        kt = True
    else:
        for i in range(2,a):
            if a%i == 0:
                kt = False
    if kt == True:
        print(f'{a} la so nguyen to')
    else:
        print(f'{a} khong phai so nguyen to')