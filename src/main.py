"""
main module
"""
import logging
from datetime import datetime, timedelta
from dateutil.parser import parse
import gdrive
import gsheet
import gmail
import gmail_parser
import category
import report


SHEET_NAME = 'passbook'

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    """
    driver function
    """
    process_date_from = datetime.now()+timedelta(days=-6)
    process_date_to = datetime.now()+timedelta(days=1)

    spreadsheet_id = gdrive.get_sheet_id(SHEET_NAME)
    if not spreadsheet_id:
        spreadsheet_id = gsheet.create_spreadsheet(SHEET_NAME)
    logger.info(f"spreadsheet_id={spreadsheet_id}")

    if not spreadsheet_id:
        logger.error('unable to create spreadsheet. Exiting!!!')
        return

    current_sheet_name = process_date_from.strftime("%Y%m")
    gsheet.add_sheet(spreadsheet_id, current_sheet_name)

    mime_messages = gmail.get_mails(process_date_from, process_date_to)
    logger.info('total number of messgaes = %s' % len(mime_messages))

    records = []
    for message_id,mime_message in mime_messages.items():
        data = gmail_parser.parse(mime_message)
        if not data:
            logger.warning('couldnt parse %s'% mime_message['subject'])
            continue

        data.update({'date':parse(data['date']).strftime("%Y-%m-%d")})
        data.update({'subject':mime_message['subject']})
        data.update({'category':category.get(data['seller'])})

        data.update({'tx_type':'debit' if 'debit' in (data['tx_type']).lower() else 'credit'})

        data.update({'amount':float(data['amount'])})
        data.update({'amount':-1*data['amount'] if data['tx_type'] == 'credit' else data['amount']})
        data.update({'id':message_id})

        records.append(data)
        logger.debug(data)

    HEADER = ['date', 'amount', 'seller', 'tx_type', 'category', 'id']
    request = []
    for record in records:
        expense = [record[name]for name in HEADER]
        request.append(expense)
    
    if request:
        gsheet.write_to_sheet(spreadsheet_id, current_sheet_name, request)
        gsheet.de_duplicate(spreadsheet_id, current_sheet_name)
    
    report_data = report.generate(spreadsheet_id, current_sheet_name, datetime.now()+timedelta(days=-1))
    logger.debug(report_data)

    



    
    


if __name__ == "__main__":
    main()
