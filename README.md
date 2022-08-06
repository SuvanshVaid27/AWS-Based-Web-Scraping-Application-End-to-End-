# AWS-Based-Web-Scraping-Application-End-to-End


This project is a complete AWS based solution with the aim of scraping news article headlines from a website, storing them in a database and analyszing the results. 

SQL, Python, AWS Cloud and shell scripting were used to create this data solution. The following steps describe the whole process in a simple manner:

  1. The very first step was creating a [Free Tier t2.micro EC2 Linux instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
  While setting this up, the only change we have to make is in the security grouo where we have to allow public access for TCP over SSH connection (port 22) and TCP for PostgreSQL (port 5432). 
  
  2. The next step is to access the EC2 instance through your own device. I'm using a MAC so I access it using the terminal (using the .PEM certificate file to authenticate the connection). 
  
  3. Once you have access to the instance, the next step is to go ahead and [install postgresql](https://www.how2shout.com/linux/install-postgresql-13-on-aws-ec2-amazon-linux-2/) on it. 
  
2. Design and code a small scraping python app in vs code or similar
3. Use the app to scrape 200+ news articles and inspect the data. More data fields
(meta data, sentiment, etc) is better and more impressive.
4. Design the database table schema
5. Create the new database table and insert the news data
6. Analyse the news data in a jupyter notebook
7. Summarise and send details back to us so we can read your code, sql & db schema.

