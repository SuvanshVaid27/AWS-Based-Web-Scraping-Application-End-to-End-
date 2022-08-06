# AWS-Based-Web-Scraping-Application-End-to-End


This project is a complete AWS based solution with the aim of scraping news article headlines from a website, storing them in a database and analyszing the results. 

SQL, Python, AWS Cloud and shell scripting were used to create this data solution. The following steps describe the whole process in a simple manner:

1. Instal and setup a new postgres database into a T2.micro EC2 instance

  * The very first step was creating a [Free Tier t2.micro EC2 Linux instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
  While setting this up, the only change we have to make is in the security grouo where we have to allow public access for TCP over SSH connection (port 22) and TCP for PostgreSQL (port 5432). 
  
  * The next step is to access the EC2 instance through your own device. I'm using a MAC so I access it using the terminal (using the .PEM certificate file to authenticate the connection). 
  
  * Once you have access to the instance, the next step is to go ahead and [install postgresql](https://www.how2shout.com/linux/install-postgresql-13-on-aws-ec2-amazon-linux-2/) on it. 
  
  * After postgres in installed on the instance, we need to make a [tiny change in it's config file](https://betterprogramming.pub/how-to-provision-a-cheap-postgresql-database-in-aws-ec2-9984ff3ddaea) so that the Postgres server can listen on the DNS name of the EC2 instance and also allow authentication from remote connections. 

  * Once done, we can now create a user, role and password for our postgres server. To access the server and it's content from a gui based tool, I used the pgAdmin (feel free to use psql or any other tools).

  * Next, we create a 'News' database.  

2. The second part of this project is to create a small web scraping app using python and write the data to the 'News' table.   

  * A new table called 'crypto' is created first through pgAdmin, with the followig schema:

  ```
  CREATE TABLE crypto (
   newsid INT GENERATED ALWAYS AS IDENTITY,
   searchtopic VARCHAR(100) NOT NULL,
   headline VARCHAR(500) NULL,
   source VARCHAR(100) NULL,
   time TIMESTAMP NULL
   );

  ```

  *  BeautifulSoup and Requests libraries from python were used to effectively scrape news article headlines from google news. Alternatively, there is another way to do so (through the pygooglenews package) which requires less lines of code and much more information. 
  
  * In the same app, the database creadentials are read through the dot-env file and sqlalchemy is then used to create a connection with the News database in our postgres server in EC2 instance. 

  * The app finally scrapes the news headlines realted to top 10 cryptocurrencies, cleans the data, and writes the resulting dataframe to the crypto table

3.  The third and final part of this project shows how we can read data from the crypto table we created above and use efffecient aggregate queries to perform a simple exploratory analysis on the data. 
