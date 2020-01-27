# employee_rec

This directory contains code developed for an assignment. Kindly read below before cloning and using the same.

### List of pre-requisites:
1) Libraries and packages required are mentioned in "requirements.txt" available at root directory of this project.

### Understanding tech stack used:
1) This project contains both back end and front end code.
2) This is built in python, using django framework, mysql database and utilizes vanilla javascript, jQuery for DOM manipulation.
3) Table display is made using jQuery datatable plugin with django api calls as source.
4) DRF is used in django for APIs.

###What it does?
Helps "Add" a new employee to database.
"Search" employees in database based on parameters.
"Edit" few fields of a record.
"Delete" a record from database.

###How to run?
1) Clone the project on your local system.
2) Install dependencies from requirements.txt file (it is suggested to create a virtual environment first).
3) DB connection (Change in settings.py file -> the DATABASE variable as per your local setup)
4) Run makemigrations and migrate commands.
5) Runserver. This will render the website on localhost, you can then view/use it on localhost:<port>/employee/
Please note : the project is developed for assignment purpose, please use only recommended url as other urls are 
not configured and/or handled.

###Time to develop this project?
Started on Sunday 26th Jan 11 am (working hours 8-9 hours)
Completed on Monday 27th Jan around 4 pm (working hours 1-2 hours)

