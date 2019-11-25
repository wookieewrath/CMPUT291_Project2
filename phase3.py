from bsddb3 import db

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

    iter = terms_curs.first()

    result = dates_curs.set(b'2000/01/12')
   # query_set = set()
    query_list = []
    
    #for dates cases
    symbol = '<='
    #greater than case
    if symbol == '=':
        while True:
            if result is not None:
                query_list.append(result[1])
                result = dates_curs.next_dup()
            else:
                break
    
    elif symbol == '>':
        result = dates_curs.next_nodup()
        while True:
            if result is not None:
                query_list.append(result[1])
                result = dates_curs.next()
            else:
                break        
        
    
    elif symbol == '<':
        result = dates_curs.prev()
        while True:
            if result is not None:
                query_list.append(result[1])
                result = dates_curs.prev()
            
            else:
                break
                
    elif symbol == '>=':
        while True:
            if result is not None:
                query_list.append(result[1])
                result = dates_curs.next()
            else:
                break         
        
    
    elif symbol == '<=':
        while True:
            if result is not None:
                query_list.append(result[1])
                result = dates_curs.next_dup()
            else:
                break
            
        result = dates_curs.prev_nodup()
        while True:
            if result is not None:
                query_list.append(result[1])
                result = dates_curs.prev()
            else:
                break
    
    
    print(query_list)
    
    
main()
