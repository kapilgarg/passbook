"""
report module
"""
from string import Template
import itertools
import logging
import gsheet

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

mail_template = Template("""
Hello,
Here is your expense report.

Total expense : $total_expense
---------------------------------------------------
$current_day_records

Categorized Expense
---------------------------------------------------
$expense_by_category_daily

Total expense in this month (till now)
---------------------------------------------------
$expense_by_category_monthly
""")
line_record_seller = Template("INR $amount - $seller \n")
line_record_category = Template("INR $amount - $category \n")

def __generate_data(spreadsheet_id, sheet_name, date):
    records = gsheet.get_from_sheet(spreadsheet_id, sheet_name)
    current_day_record = [record for record in records if record[0] == date.strftime("%Y-%m-%d")]
    current_day_record  = sorted(current_day_record,key=lambda x:x[4])
    group_by_category_daily = itertools.groupby(current_day_record, lambda x:x[4])

    expense_by_category_daily = {}
    for category,group in group_by_category_daily:
        expense_by_category_daily[category] = sum([float(rec[1]) for rec in group])
    
    expense_by_category_monthly = {}
    monthly_records = sorted(records,key=lambda x:x[4])
    group_by_category_month = itertools.groupby(monthly_records, lambda x:x[4])
    for category,group in group_by_category_month:
        expense_by_category_monthly[category] = sum([float(rec[1]) for rec in group])
    
    return {        
        'current_day_records':current_day_record,
        'expense_by_category_daily': expense_by_category_daily,
        'expense_by_category_monthly':expense_by_category_monthly
    }

def generate(spreadsheet_id, sheet_name, date):
    """
    returns the data to generate email notification
    """
    data = __generate_data(spreadsheet_id, sheet_name, date)

    current_day_records = data['current_day_records']
    expense_by_category_daily = data['expense_by_category_daily']
    expense_by_category_monthly = data['expense_by_category_monthly']

    #total expense contains only debit
    total_expense = sum([float(record[1]) for record in current_day_records if float(record[1]) > 0])
    for record in current_day_records:
        expense_for_current_day = expense_for_current_day + line_record_seller.substitute(amount=record[1], seller=record[2])
    logger.debug(expense_for_current_day)

    expense_by_category_daily_str = ''
    for category, expense_amount in expense_by_category_daily.items():
        expense_by_category_daily_str = line_record_category.substitute(amount=expense_amount, category=category)
    logger.debug(expense_by_category_daily_str)

    expense_by_category_monthly_str = ''
    for category, expense_amount in expense_by_category_monthly.items():
        expense_by_category_monthly_str = line_record_category.substitute(amount=expense_amount, category=category)
    logger.debug(expense_by_category_monthly_str)

    return mail_template.substitute({
        'total_expense':total_expense,
        'date':date.strftime("%Y-%m-%d"),
        'current_day_records':expense_for_current_day,
        'expense_by_category_daily':expense_by_category_daily_str,
        'expense_by_category_monthly':expense_by_category_monthly_str
    })
