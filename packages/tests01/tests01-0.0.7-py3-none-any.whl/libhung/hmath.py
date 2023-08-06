#phuong trinh
def pt_1(a,b):
    """giải phương trình bậc nhất"""
    if a == 0 and b != 0 :
        print('pt vo nghiem')                   
    elif a == 0 and b == 0 :
        print('pt vo so nghiem')   
    elif a != 0 :
        print(f'x = {- b / a}')
        return - b / a   


def pt_2(a, b, c):
    """giải phương trình bậc hai"""
    if b * b - 4 * a * c < 0:
        print('pt vo nghiem')
                            
    elif b * b - 4 * a * c == 0:
        print(f'x = {- b / (2 * a)}')
        return - b / (2 * a)

    else:
        x1 = (- b + ((b * b - 4 * a * c) ** (1 / 2))) / (2 * a)
        x2 = (- b - ((b * b - 4 * a * c) ** (1 / 2))) / (2 * a)
        print(f'x1 = {x1}\nx2 = {x2}')
        return x1, x2



def hpt_1_2(a1, b1, c1, a2, b2, c2):
    """giải hệ phương trình bậc nhất hai ẩn"""
    D = a1 * b2 - a2 * b1
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1

    if D != 0 :
        print(f'x = {Dx / D}\ny = {Dy / D}')
        return Dx / D,Dy / (D)  
    elif (D) == 0 and ((Dx) != 0 or Dy != 0):
        print('hpt vo  nghiem')

    elif ((D) - (Dx) == 0) and ((D) -Dy == 0) and ((Dx) -Dy==0):
        print('hpt vo so nghiem')       