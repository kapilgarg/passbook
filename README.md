# passbook
Passbook is a personal money manager which tracks your expenses using bank notifications on gmail. It parses the mail , extraxts the relevent information and stores that in google sheet and sends a summary email mail for daily expense.

## Pre requisite
This application requires authentication with google hence you need to generate a credential file from google develop console with following apis enabled-
1. gmail
2. google sheet
3. google drive
copy that credential file in working folder along with other files. When you run this application for the first time, it will ask to authenticate with your account and on successful autnentication, generates a pickle.token file in the same folder.
Any time permission are changed, this pickle file needs to be generated again. for that just delete the existing file and authenticate again.