"""
categories the expanse
"""
categories = {}
all_category_list = []

with open('category.txt', 'r') as f:
    all_category_list = f.readlines()

categories = {k:v.replace("\n",'') for k,v in (category.split("=")for category in all_category_list)}

def get(seller):
    """
    return category corrosponding to seller
    """
    for key in categories.keys():
        if key in seller:
            return categories[key]
    return 'other'
