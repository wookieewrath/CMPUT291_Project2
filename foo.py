def foo(x):
    print("")
    search_string = x
    decomposed_string = list(
        search_string)  # Will decompose the original search_string into a list of its individual characters.
    query = {}  # Initialize the query dictionary

    symbols = ["<", ">", ":"]
    keywords = ["row", "date", "from", "to", "subject", "subj", "cc", "bcc", "body"]

    item = 0
    while True:
        if item >= len(decomposed_string):
            break
        elif decomposed_string[item] in symbols:
            decomposed_string.insert(item, " ")
            decomposed_string.insert(item + 2, " ")
            item = item + 2

        else:
            item = item + 1

    string = "".join(decomposed_string)

    search_terms = string.split()
    subject_body_searches = []
    for i in range(len(search_terms)):
        subject_body_searches.append(search_terms[i])

    for i in range(len(search_terms)):
        if search_terms[i] in symbols:
            if search_terms[i - 1] in keywords and search_terms[i - 1] not in query:
                query[search_terms[i - 1]] = ["".join(search_terms[i] + search_terms[i + 1])]
                subject_body_searches.remove(search_terms[i - 1])
                subject_body_searches.remove(search_terms[i])
                subject_body_searches.remove(search_terms[i + 1])

            elif search_terms[i - 1] in keywords and search_terms[i - 1] in query:
                query[search_terms[i - 1]].append("".join(search_terms[i] + search_terms[i + 1]))
                subject_body_searches.remove(str(search_terms[i - 1]))
                subject_body_searches.remove(str(search_terms[i]))
                subject_body_searches.remove(str(search_terms[i + 1]))

    print(subject_body_searches)
    print(query)



foo('''body:stock  confidential % shares body:       ayy  body: body cc: foo foo body   :lamo test: foo date<2001/04/12''')
foo('''bcc:derryl.cleaveland@enron.com  cc:jennifer.medcalf@enron.com''')
foo('''confidential % foo% ''')
foo('''subj:gas body:earning''')
