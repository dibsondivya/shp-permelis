# PERMELIS
Permelis is a searchable image-based medication database that facilitates the printing of personalised medication lists for patients.

## Key Features
* Real-time search results based on purpose, name and side effects of medications
* Side-by-side view of search results and cart
* Easy access to medication information through modal dialog
* Add, Edit and Delete options for administrator

## Installation
Local version of Permelis currently requires a MySQL client for database management and Python 3.7's Flask for the server-side. MySQL 8.0 is recommended.

## Contents
Specific packages needed are found in requirements.txt while all relevant icons, medication images, css files and js files are found in the static folder. The sql script for database creation and population is found in sqldump.sql, to be run within your MySQL client. Database is made up of three tables; DrugInfo for medication-related information, AdminInfo for administrator login-related information and AuthenticationInfo for primary app access.

## Database Setup
* MySQL Community Server
    1. Download MySQL Community Server, ensuring you have no other MySQL products previously installed and initialize with defaults.
    2. Create root user account with password, where both are to be remembered.
    3. Once setup, go to your MySQL client.
* MySQL Client
    1. Suggested MySQL clients are DBeaver or MySQL Workbench.
    2. Once downloaded, select 'Connect to a Database' to create a database connection and choose MySQL as the driver. 
    3. For server information, keep server host as localhost and port as 3306. Leave the database name blank. For authentication information, setup the username (dbuser), typically found as root and the password (dbpass).
    4. Click 'Finish' to complete setup.
    5. Once created, click the created database connection to view the dropdown for Databases.
    6. Create a new database, with the name to represent dbname.
    7. Click 'Open SQL Script' and select sqldump.sql.
    8. Run the script and watch the tables be created and populated.
* Python file changes
    1. Open secretact.py file and rename dbname, dbuser and dbpass as per your database setup above.

## To note in Windows 
1. Download wkhtmltopdf from https://wkhtmltopdf.org/downloads.html and unzip the exe instead of running the installer
2. Identify path of wkhtmltopdf.exe in Program Files aka ////PATH/////
3. In app.py, under the @app.route('/printing'), replace 
~~~
pdf = pdfkit.from_string(printout, False, options=options) 
~~~
with the two lines below where ////PATH///// is replaced
~~~
    config = pdfkit.configuration(wkhtmltopdf=r'////PATH/////')
    pdf = pdfkit.from_string(printout, False, options=options, configuration=config)
~~~

## Before Execution
Once MySQL client has been setup, edit secretact.py to state your database information. Refer to Database Setup for more information. Once requirements.txt has also been run, run app.py.

## Decisions to Make
* If adding images directly to the static/images folder instead of through the app itself, replace all spaces in image name with an underscore and adjust the name in the Img column of DrugInfo table in the database accordingly to prevent image duplicates.
* If adding additional columns to the admin table, 
    1. Run an sql script adding columns to the database in a MySQL client and populate them. Once done, generate an sqldump.sql and update the .sql file in this folder. Editing the sql database will automatically update the table found in Admin View.
    2. Edit Admin.html and Edit.html found in the 'templates' folder to include the new columns in the forms.
    3. Edit Modal.html to reflect the new information in a modal upon a search.
    4. Edit App.py to account for the new columns so as to ensure updates to the database.
    5. Edit Admin.js within static/js to allow for export of additional columns. 

## Project Status
App has been deployed using AWS.

## For Future Editions
Consider adding section on how to remember to take medications, to be featured in the printout, as well as including more information on medication storage, dosages and contraindications for improved understanding and literacy.

## Contact
If in need of assistance, contact me at divya_shridar@mymail.sutd.edu.sg.