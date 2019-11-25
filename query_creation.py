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
        
        search_dictionary = {}
        
        for search_term in query:
                if search_term == "to" or search_term == "from" or search_term == "cc" or search_term == "bcc":
                        for value in range(len(query[search_term])):
                                search = search_term + '-' + query[search_term][value][1:]
                                if "emails_curs" in search_dictionary:
                                        search_dictionary["emails_curs"].append(search)
                                else:
                                        search_dictionary["emails_curs"] = [search]
                
                if search_term == "subj" or search_term == "subject" or search_term == "body":
                        for value in range(len(query[search_term])):
                                search = search_term[0] + '-' + query[search_term][value][1:]
                                if "terms_curs" in search_dictionary:
                                        search_dictionary["terms_curs"].append(search)
                                else:
                                        search_dictionary["terms_curs"] = [search]                        
                
                if search_term == "date":
                        for value in range(len(query[search_term])):
                                search = query[search_term][value]
                                if "dates_curs" in search_dictionary:
                                        search_dictionary["dates_curs"].append(search)
                                else:
                                        search_dictionary["dates_curs"] = [search]

        if len(subject_body_searches) != 0:
                if "subj_or_body" in search_dictionary:
                        for word in subject_body_searches:
                                search_dictionary["subj_or_body"].append(word)
                                        
                else:
                        search_dictionary["subj_or_body"] = []
                        for word in subject_body_searches:
                                search_dictionary["subj_or_body"].append(word)
                
        return search_dictionary


        
