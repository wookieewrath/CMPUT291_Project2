from bsddb3 import db

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
    iter=terms_curs.next()

result = terms_database.get(b'994')
print(result)

result = terms_curs.set(b'b-you')
print(result)