from bsddb3 import db
from query_creation import query_creation


def terms_search(curs, term):
    result = curs.set(bytes(term,'utf-8'))
    query_set = set()
    
    while True:
        if result is not None:
            query_set.add(result[1])
            result = curs.next_dup()
        else:
            break
    
    return query_set    
    
def dates_search(curs, term):
    symbol = ''
    length = len(term)
    query_set = set()
    i = 0
    for i in range(3):
        if term[i].isdigit() == False:
            symbol += term[i]
        
        else:
            j=i
            break
    term = term[j:]
    print(term)
    print(symbol)

    result = curs.set(bytes(term,'utf-8'))
    
    if symbol == ':':
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.next_dup()
            else:
                break
    
    elif symbol == '>':
        result = curs.next_nodup()
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.next()
            else:
                break        
        
    
    elif symbol == '<':
        result = curs.prev()
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.prev()
            
            else:
                break
                
    elif symbol == '>=':
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.next()
            else:
                break         
        
    
    elif symbol == '<=':
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.next_dup()
            else:
                break
            
        result = curs.prev_nodup()
        while True:
            if result is not None:
                query_set.add(result[1])
                result = curs.prev()
            else:
                break    
    
    return query_set

def emails_search(curs, term):
    
    result = curs.set(bytes(term,'utf-8'))
    query_set = set()
    
    while True:
        if result is not None:
            query_set.add(result[1])
            result = curs.next_dup()
        else:
            break
    
    return query_set

def body_search(curs, term):
    
    term_1 = 'b-' + term
    term_2 = 's-' + term
    
    result = curs.set(bytes(term_1,'utf-8'))
    query_set = set()
    
    while True:
        if result is not None:
            query_set.add(result[1])
            result = curs.next_dup()
        else:
            break    
    
    result = curs.set(bytes(term_2,'utf-8'))
    
    while True:
        if result is not None:
            query_set.add(result[1])
            result = curs.next_dup()
        else:
            break       
                      
    return query_set

def main():

    terms_file = "te.idx"
    dates_file = "da.idx"
    emails_file = "em.idx"
    recs_file = "re.idx"

    terms_database = db.DB()
    dates_database = db.DB()
    emails_database = db.DB()
    recs_database = db.DB()

    terms_database.open(terms_file)
    dates_database.open(dates_file)
    emails_database.open(emails_file)
    recs_database.open(recs_file)

    terms_curs = terms_database.cursor()
    dates_curs = dates_database.cursor()
    emails_curs = emails_database.cursor()
    recs_curs = recs_database.cursor()
    
    print("Welcome to the database!")
    print("Typing 'output=full' will output full records")
    print("Typing 'output=brief' will output Row ID and Subject")
    
    mode = "brief"
    
    while True:
        foo = input("Please enter a search query: ")
        
        if foo == 'stop':
            break
        
        if foo == "output=full":
            mode = "full"
            print("Now in full output mode.")
            continue
    
        if foo == "output=brief":
            mode = "brief"
            print("Now in brief output mode.")
            continue        
        
        search_dict = query_creation(foo)
        print("This is the search dictionary")
        print(search_dict)
        
        sets = []
        
        for database in search_dict:
            
            if database == "terms_curs":
                i = 0
                for term in search_dict[database]:
                    if i == 0:
                        term_set = terms_search(terms_curs, term)
                        i += 1
                    else:
                        term_set = term_set.intersection(terms_search(terms_curs,term))
                
                sets.append(term_set)
                        
                        
                    
            if database == "dates_curs":
                i = 0
                for term in search_dict[database]:
                    if i == 0:
                        dates_set = dates_search(dates_curs, term)
                        i += 1
                    else:
                        dates_set = dates_set.intersection(dates_search(dates_curs,term))
                
                sets.append(dates_set)  
                                  
                    
                    
            if database == "emails_curs":
                i = 0
                for term in search_dict[database]:
                    if i == 0:
                        emails_set = emails_search(emails_curs, term)
                        i += 1
                    else:
                        emails_set = emails_set.intersection(emails_search(emails_curs,term))
                
                sets.append(emails_set) 
                    
            if database == "subj_or_body":
                i = 0
                for term in search_dict[database]:
                    if i == 0:
                        body_set = body_search(terms_curs, term)
                        i += 1
                    else:
                        body_set = body_set.intersection(body_search(terms_curs,term))
                
                sets.append(body_set)              

            j = 0
            for i in sets:
                if j == 0:
                    final_set = i
                    j+=1
                    
                else: 
                    final_set = final_set.intersection(i)
            print(final_set)
            
            some_list = list(final_set)
            print(some_list)
            
            if mode=="full":
                for row in some_list:
                    result = recs_curs.set(row)
                    print(result[1].decode("utf-8"))
                    
            elif mode=="brief":
                # to do :(
                pass
                    
                    

if __name__ == "__main__":
    main()
