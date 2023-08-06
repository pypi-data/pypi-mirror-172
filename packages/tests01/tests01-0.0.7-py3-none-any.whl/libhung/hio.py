def hinput(key = ' ', content = '', type = "str"):
    """đưa vào một string, kết quả trả ra là một list được tách bởi key"""
    l = input(f'{content}').split(key)
    if type == 'str':
        return l
    elif type == 'int':
        for i in range(len(l)):
            l[i] = int(l[i])
        return l
    elif type == 'float':
        for i in range(len(l)):
            l[i] = float(l[i])
        return l

a = hinput(content = "nhap vao string: ", key = "." )
print(a)