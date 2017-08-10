# Logs Analysis Project
This .zip file contains a Python file that prints out reports based on the information from a mock database for a fictional news website, created by Udacity. Also included is a plain text file that demonstrates what should be printed out after running the program.

## Prerequisites
* [Python2](https://www.python.org/)
* [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)

## Getting Started
Download the .zip file, which has:
* report_tool.py
* EXAMPLE_OUTPUT.text
* README.md

Open each file to examine its contents and comments in the code.

In addition you MUST download the actual database in order for these files to work properly. Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip this file.

The file inside is called __newsdata.sql__. Put this file into the vagrant directory, which is shared with your virtual machine.


## Running The Script
Firing up the VM:
* Run ``` vagrant up ```
* Run ``` vagrant ssh ```

To load the data, use the command:
```
psql -d news -f newsdata.sql
```

Here's what this command does (as per the description provided by Udacity):
* ```psql``` — the PostgreSQL command line program
* ```-d news``` — connect to the database named news which has been set up for you
* ```-f newsdata.sql``` — run the SQL statements in the file newsdata.sql

After this step, you may access the database by using ```psql -d news```. 


### report_tool.py
This python file contains three functions:
* popular_articles()
* popular_authors()
* error_days()

All three functions will fetch data from the __news__ database which will print out specific queries.

In addition, these functions use specific queries that have been created with multiple views.

__The user MUST manually add these views to the news database.__

#### popular_articles
The popular_articles function presents the three most popular articles as a sorted list with the most one at the top.

Views used:
* __top3_articles__ - This view has the columns "replace" and "hits". The replace column contains the individual "paths" from the log table. It was created so that top3_articles could be joined with the articles table with ease.
```
create view top3_articles as select replace(path,'/article/',''), count(*) as hits from log where status = '200 OK' group by path order by hits desc offset 1 limit 3;
```

#### popular_authors
The popular_authors function presents the most popular authors of all time, aggregating view counts for each author.

Views used:
* __article_hit_totals__ - This shows the view totals for all articles published.
```
create view article_hit_totals as select replace(path,'/article/',''), count(*) as hits from log where status = '200 OK' group by path order by hits desc offset 1;
```
* __authorid_hits_per_article__ - This shows each articles' view totals with its author's numeric ID.
```
create view authorid_hits_per_article as select articles.author, article_hit_totals.hits from articles join article_hit_totals on articles.slug = article_hit_totals.replace order by author;
```

* __author_viewstats__ - This shows the aggregated view totals for each author's numeric ID. This view can finally be joined with authors table so we can finally obtain the expected query.
```
create view author_viewstats as select author, sum(hits) as total_hits from authorid_hits_per_article group by author;
```

#### error_days
 The error_days function presents on which days did more than 1% of requests led to errors.

 Views used:
 * __daily_errors__ - This shows the number of requests that led to errors on a specific day.
 ```
create view daily_errors as select time::date, count(*) as errors from log where status != '200 OK' group by time::date order by time::date;
```
 * __daily_success__ - This shows the number of requests that were successful on a specific day.
 ```
 create view daily_success as select time::date, count(*) as success from log where status = '200 OK' group by time::date order by time::date;
 ```

 * __daily_error_percent__ - This shows the percentage of requests that led to errors on a specific day.
 ```
 create view daily_error_percent as select daily_success.time,(daily_errors.errors/(daily_success.success + daily_errors.errors)::float)*100 as error_percent from daily_errors join daily_success on daily_errors.time = daily_success.time;
 ```
 ## Running the program
 In order to test and view the proper results of the three queries, make sure to have Vagrant and a virtual machine installed.

 Also make sure to have downloaded the newsdata.sql file in your Vagrant directory, which can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

 The line of code that will run on Terminal is:

 ```
 python report_tool.py
 ```

## Built With
* [Atom](https://atom.io) - Text editor used to create report_tool.py and README.md
* [Vagrant](https://www.vagrantup.com/) - A tool for building and managing virtual machine environments in a single workflow.
* [VirtualBox](https://www.virtualbox.org/)- VirtualBox is a general-purpose full virtualizer for x86 hardware, targeted at server, desktop and embedded use.

## Contributing
Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors
* **Chris Jeon**

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
