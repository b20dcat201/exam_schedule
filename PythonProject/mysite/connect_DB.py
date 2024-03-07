# module nay dung de ket noi voi sql server 
import pyodbc

def connectSQL():
    cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-HR1EMAC;'
                      'Database=test;'
                      'Trusted_Connection=yes;')
    return cnxn