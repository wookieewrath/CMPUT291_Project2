



def foo(mystring):

    for x in range(len(mystring)-1, -1, -1):
        if mystring[x] == "z":
            mystring = mystring[:-1]
            return foo(mystring)
        else:
            last = mystring[-1]
            mystring = mystring[:-1] + chr(ord(last)+1)
            return mystring


x = foo("b-z")
print(x)