def read_input(x):
    mystring = x
    mystring = (" ".join(mystring.split()))

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

    for x in queue:
        if x in operators and x is not "%":
            count = queue.index(x)
            queue[count - 1:count + 2] = ["".join(queue[count - 1:count + 2])]
        elif x is "%":
            count = queue.index(x)
            queue[count - 1:count + 1] = ["".join(queue[count - 1:count + 1])]

    print(queue)


read_input('''body:stock  confidential % shares  date<2001/04/12''')
read_input('''bcc:derryl.cleaveland@enron.com  cc:jennifer.medcalf@enron.com''')
read_input('''confidential % foo%''')
read_input('''subj:gas body:earning''')
