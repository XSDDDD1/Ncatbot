def a ():
    text1 = input()
    text2 = text1.encode("UTF-8").decode("gbk", errors='ignore')
    print(text2)

if __name__ == "__main__":
    a()