# passbook
Passbook is a personal money manager which tracks your expenses using bank notifications on gmail. It parses the mail , extraxts the relevent information and stores that in google sheet and sends a summary email mail for daily expense.

## Pre requisite

This application requires authentication with google hence you need to generate a credential file from google developer console. 

Go to https://console.cloud.google.com/ and create a new project. 

Select project type as desktop.

Enable following apis for the project
1. gmail
2. google sheet
3. google drive

Once project is created successfully, download the file and save it as credentials.json

Copy that credential file in working folder along with other files. When you run this application for the first time, it will ask to authenticate with your account and on successful autnentication, generates a pickle.token file in the same folder.
Any time permission are changed, this pickle file needs to be generated again. for that just delete the existing file and authenticate again.

## Run application

Run Main.py to run the application. It takes 3 parameters

1. start_date : start date for email to extract the expenses
2. end_date : end date for email to extract the expenses(excluding)
3. email_recp : email address to which summary email has to be sent

start_date and end_date should belong to same month.

By default start date is the current date and end date is tomorrow's date so that you get current day's expenses. but these can be changed and can be set from command line arguments.

    >> python main.py --email_recp <email-address>  

You receive an email like the below -
![expense summary !](/assets/images/mail.png)







