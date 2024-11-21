def i(j):
    x = j.pop()
    print(x)
    x = j.pop()
    print(x)
    x = j.pop()
    print(x)

mylist = [x for x in range(0,10)]
i(mylist)
x = mylist.pop()
print(x)
x = mylist.pop()
print(x)
i(mylist)
x = mylist.pop()
print(x)