from django.test import TestCase, SimpleTestCase
import pandas as pd
import random
from datetime import datetime, timedelta
# from . import models
# Create your tests here.
# class SimpleTests(SimpleTestCase):
#     def test_home_page_status(self):
#         response = self.client.get("/")
#         self.assertEqual(response.status_code, 200)   


# from datetime import datetime, timedelta


# def tinhNgay(input_date, n):
#     day, month, year = map(int, input_date.split('/'))
#     date_obj = datetime(year, month, day)
#     new_date = date_obj + timedelta(days=n)
#     output_date = new_date.strftime("%d/%m/%Y")
#     return output_date

def Ngay(input_date):
    year, month, day = map(int, input_date.split('-'))
    date_obj = datetime(year, month, day)
    output_date = date_obj.strftime("%d/%m/%Y") 
    return output_date

# print(tinhNgay('05/04/2023', 5))

def ngay_sql(input_date):
    day, month, year = map(int, input_date.split('/'))
    date_obj = datetime(year, month, day)
    output_date = date_obj.strptime("%Y/%m/%d")
    return output_date

print(Ngay("2002-05-11"))
print(ngay_sql("05/11/2002"))