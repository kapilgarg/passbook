from dateutil.parser import parse
import itertools
import logging
import gsheet

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def generate(spreadsheet_id, sheet_name, date):
    records = gsheet.get_from_sheet(spreadsheet_id, sheet_name)
    current_day_record = [record for record in records if record[0] == date.strftime("%Y-%m-%d")]
    current_day_record  = sorted(current_day_record,key=lambda x:x[4])
    group_by_category_daily = itertools.groupby(current_day_record, lambda x:x[4])

    expanse_by_category_daily = {}
    for category,group in group_by_category_daily:
        expanse_by_category_daily[category] = sum([float(rec[1]) for rec in group])
    
    expanse_by_category_monthly = {}
    monthly_records = sorted(records,key=lambda x:x[4])
    group_by_category_month = itertools.groupby(monthly_records, lambda x:x[4])
    for category,group in group_by_category_month:
        expanse_by_category_monthly[category] = sum([float(rec[1]) for rec in group])

    return {
        'current_day_record':current_day_record,
        'expanse_by_category_daily': expanse_by_category_daily,
        'expanse_by_category_monthly':expanse_by_category_monthly
    }