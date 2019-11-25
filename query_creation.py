def query_creation(user_input):
        search_string = user_input
        decomposed_string = list(search_string) #Will decompose the original search_string into a list of its individual characters.
        query = {} #Initialize the query dictionary
        
        symbols = ["<",">",":", ">=", "<="]
        keywords = ["row", "date", "from", "to", "subject", "subj", "cc", "bcc", "body"]
        
        item = 0
        while True:
                if item >= len(decomposed_string):
                        break
                elif decomposed_string[item] in symbols:
                        decomposed_string.insert(item, " ")
                        decomposed_string.insert(item+2, " ")
                        item = item+2
                
                else:
                        item = item+1
        
        string = "".join(decomposed_string)
        
        search_terms = string.split()
        subject_body_searches= []
        for i in range(len(search_terms)):
                subject_body_searches.append(search_terms[i])
        
        for i in range(len(search_terms)):
                if search_terms[i] in symbols:
                        if search_terms[i-1] in keywords and search_terms[i-1] not in query:
                                query[search_terms[i-1]] = ["".join(search_terms[i] + search_terms[i+1])]
                                subject_body_searches.remove(search_terms[i-1])
                                subject_body_searches.remove(search_terms[i])
                                subject_body_searches.remove(search_terms[i+1])
                                
                        elif search_terms[i-1] in keywords and search_terms[i-1] in query:
                                query[search_terms[i-1]].append("".join(search_terms[i] + search_terms[i+1]))
                                subject_body_searches.remove(str(search_terms[i-1]))
                                subject_body_searches.remove(str(search_terms[i]))
                                subject_body_searches.remove(str(search_terms[i+1]))     
        
        print("SEARCH TERMS IN EITHER THE SUBJECT OR BODY:", subject_body_searches) 
        print("QUERY DICTIONARY", query)
        
        search_dictionary = {}
        
        for search_term in query:
                if search_term == "to" or search_term == "from" or search_term == "cc" or search_term == "bcc":
                        for value in range(len(query[search_term])):
                                search = search_term + '-' + query[search_term][value][1:]
                                if "EMAIL_SEARCHES" in search_dictionary:
                                        search_dictionary["EMAIL_SEARCHES"].append(search)
                                else:
                                        search_dictionary["EMAIL_SEARCHES"] = [search]
                
                if search_term == "subj" or search_term == "subject" or search_term == "body":
                        for value in range(len(query[search_term])):
                                search = search_term[0] + '-' + query[search_term][value][1:]
                                if "TERMS_SEARCHES" in search_dictionary:
                                        search_dictionary["TERMS_SEARCHES"].append(search)
                                else:
                                        search_dictionary["TERMS_SEARCHES"] = [search]                        
                
                if search_term == "date":
                        for value in range(len(query[search_term])):
                                search = query[search_term][value]
                                if "DATES_SEARCHES" in search_dictionary:
                                        search_dictionary["DATES_SEARCHES"].append(search)
                                else:
                                        search_dictionary["DATES_SEARCHES"] = [search]

        if len(subject_body_searches) != 0:
                if "SUBJ_OR_BODY" in search_dictionary:
                        for word in subject_body_searches:
                                search_dictionary["SUBJ_OR_BODY"].append(word)
                                        
                else:
                        search_dictionary["SUBJ_OR_BODY"] = []
                        for word in subject_body_searches:
                                search_dictionary["SUBJ_OR_BODY"].append(word)
                
        print(search_dictionary)

query_creation("date:1999/01/01 date>=1999/02/02 date<=1999/03/03")
        
