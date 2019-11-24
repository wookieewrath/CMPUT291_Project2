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
    while iter:
        print(iter)
        iter = terms_curs.next()

    result = dates_curs.set(b'2001/05/14')
    while True:
        result = dates_curs.next_dup()
        if result is not None:
            print(result)
        else:
            break

if __name__ == "__main__":
    main()