def read_input():
    mystring = "body :    stock  confidential%  shares  date  <2001/04/12"
    mystring = (" ".join(mystring.split()))

    print("\nOld string:\n" + mystring + "\n")

    replacements = [
        [" : ", ":"],
        [" :", ":"],
        [": ", ":"],
        [" < ", "<"],
        ["< ", "<"],
        [" <", "<"],
        [" > ", ">"],
        ["> ", ">"],
        [" >", ">"],
        [" %", "%"],
        [" % ", "%"],
        ["% ", "%"],
    ]

    for foo in replacements:
        mystring = mystring.replace(foo[0], foo[1])

    print("New string:\n" + mystring + "\n")
    operators = set(":<>%' '")
    the_array = [[]]

    count = 0
    for character in mystring:
        if character in operators:
            count += 1
            the_array.append([character])
            count += 1
            the_array.append([])
        else:
            the_array[count].append(character)

    queue = []
    for foo in the_array:
        queue.append("".join(foo))

    queue = list(filter(lambda a: a != ' ', queue))

    print(queue)

    queue_count = 0
    new_array_count = 0
    new_array = [[]]
    while queue_count < len(queue):

        if queue[count] in operators:
            new_array[count].append(queue[count])
            new_array[count].append(queue[count + 1])
            new_array.append([])
            queue_count += 1
        else:
            new_array[count].append(queue[count])
            new_array.append([])
            queue_count += 1

    print(new_array)
    new_array[0].append("foo")
    print(new_array)


read_input()
