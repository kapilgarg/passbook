"""
main module
"""
import argparse
from dateutil.parser import parse
import logging
from datetime import datetime, timedelta
from dateutil.parser import parse
import gdrive
import gsheet
import gmail
import gmail_parser
import category
import report
import send_mail


SHEET_NAME = 'passbook'

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def __enrich(data, mime_message, message_id):
    data.update({'date': parse(data['date']).strftime("%Y-%m-%d")})
    data.update({'subject': mime_message['subject']})
    data.update({'category': category.get(data['seller'])})

    data.update({'tx_type': 'debit' if 'debit' in (
        data['tx_type']).lower() else 'credit'})

    data.update({'amount': float(data['amount'])})
    data.update(
        {'amount': -1*data['amount'] if data['tx_type'] == 'credit' else data['amount']})
    data.update({'id': message_id})
    return data


def main(start_date, end_date, email_recp):
    """
    driver function
    """
    process_date_from = parse(start_date)
    process_date_to = parse(end_date)

    # Create Spreadsheet if not already done
    spreadsheet_id = gdrive.get_sheet_id(SHEET_NAME)
    if not spreadsheet_id:
        spreadsheet_id = gsheet.create_spreadsheet(SHEET_NAME)
    logger.info(f"spreadsheet_id={spreadsheet_id}")

    if not spreadsheet_id:
        logger.error('unable to create spreadsheet. Exiting!!!')
        return

    # Add a sheet for current month
    current_sheet_name = process_date_from.strftime("%Y%m")
    gsheet.add_sheet(spreadsheet_id, current_sheet_name)

    # Get the emails for the given date range
    mime_messages = gmail.get_mails(process_date_from, process_date_to)
    logger.info('total number of messgaes = %s' % len(mime_messages))

    # Parse and extract the data from emails
    records = []
    for message_id, mime_message in mime_messages.items():
        data = gmail_parser.parse(mime_message)
        if not data:
            logger.warning('couldnt parse %s' % mime_message['subject'])
            continue
        data = __enrich(data, mime_message, message_id)
        records.append(data)
        logger.debug(data)

    # Write the data to google sheet
    HEADER = ['date', 'amount', 'seller', 'tx_type', 'category', 'id']
    request = []
    for record in records:
        expense = [record[name]for name in HEADER]
        request.append(expense)

    if request:
        gsheet.write_to_sheet(spreadsheet_id, current_sheet_name, request)
        gsheet.de_duplicate(spreadsheet_id, current_sheet_name)

    # Generate Expense report and email it.
    report_date = process_date_from
    expense_report = report.generate(
        spreadsheet_id, current_sheet_name, report_date)
    logger.debug(expense_report)
    send_mail.send_message(
        'Expense report : '+report_date.strftime('%Y-%m-%d'), expense_report, email_recp)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--start_date", help="start date for the expense report")
    arg_parser.add_argument(
        "--end_date", help="end date for the expense report")
    arg_parser.add_argument(
        "--email_recp", help="email address for the recipient of expense report")
    args = arg_parser.parse_args()

    main(args.start_date, args.end_date, args.email_recp)
