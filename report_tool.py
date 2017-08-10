#!/usr/bin/env python
import psycopg2

DBNAME = "news"

"""What are the most popular three articles of all time?
Present this information as a sorted list with the most
popular article at the top."""
def popular_articles():
    """Which articles have been accessed the most?"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select articles.title, top3_articles.hits
                 from articles join top3_articles
                 on articles.slug = top3_articles.replace
                 order by hits desc;""")
    articles = c.fetchall()
    for article in articles:
        print article[0], "|", article[1], "views"
    db.close()

"""Who are the most popular article authors of all time?
   When you sum up all of the articles each author has written,
   which authors get the most page views?"""
def popular_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select authors.name, author_viewstats.total_hits
                 from authors join author_viewstats
                 on authors.id = author_viewstats.author;""")
    authors = c.fetchall()
    for author in authors:
        print author[0], "|", author[1], "views"
    db.close()

"""On which days did more than 1% of requests lead to errors?
   The log table includes a column status that indicates the HTTP
   status code that the news site sent to the user's browser."""
def error_days():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from daily_error_percent where error_percent > 1;")
    days = c.fetchall()
    for day in days:
        print str('{:%B %d, %Y}'.format(day[0])) + " | " +str('{:0.2f}'.format(day[1])) + "%"
    db.close()


print("The top three articles on the website are:")
popular_articles()

print(" ")

print("The Top Authors are:")
popular_authors()

print(" ")

print("Days with more than 1 percent error are:")
error_days()
