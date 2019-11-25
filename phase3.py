from bsddb3 import db
from query_creation import query_creation


def terms_search(curs, term):
    pass

def dates_search(curs, term):
    pass

def emails_search(curs, term):
    pass


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
    
    while True:
        foo = input("Please enter a search query: ")
        
        search_dict = query_creation(foo)
        
        
        
        for database in search_dict:
            if database == "terms_curs":
                for term in search_dict[database]:
                    terms_search(terms_curs, term)
                    
            if database == "dates_curs":
                for term in search_dict[database]:
                    dates_search(dates_curs, term)
                    
            if database == "emails_curs":
                for term in search_dict[database]:
                    emails_search(emails_curs, term)
                    
            if database == "subj_or_body":
                pass               


if __name__ == "__main__":
    main()
