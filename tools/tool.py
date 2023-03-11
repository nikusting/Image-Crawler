def Judge():
    try:
        c = eval(input("你想爬取的图片页数："))
    except:
        print("无效输入")
        Judge()
    else:
        return c


def Judge1():
    b = eval((input("输入你想爬取的页面：")))
    if type(b)==type([1]):
        return b
    else:
        print("无效输入")
        Judge1()



if __name__=="__main__":
    Judge()