# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:51:56 2016

@author: changfan
"""

import os
from bs4 import BeautifulSoup
# you need modify the path of your trioptics test file on line #11
MHT_path = 'C:\\Users\\changfan\\Documents\\Lens_test_data\\final\\20140929\\'
for fn in os.listdir(MHT_path):  
    html_file_loc=MHT_path+fn
    print html_file_loc
    html_file = open(html_file_loc, 'r')
    html = html_file.read()    
    title = os.path.splitext(html_file_loc)[0]    
    soup = BeautifulSoup(html)    
    tables = soup.find_all("table", id="ITableDataItems")    
    table_num = 1    
    for table in tables:
        if table.tbody is not None:
            table_item = table.tbody
        else:
            table_item = table
        csv = open(title+'-'+str(table_num)+'.csv', 'w')
        for row in table_item.children:
            if row.name == "tr":
                if row['id'] != 'ITRLegend':
                    first = True
                    for col in row.children:
                        if col.string is not None:
                            if first:
                                first = False
                            else:
                                csv.write(',')
                                csv.write(col.string)
                    csv.write('\n')
        csv.close()
        table_num += 1    
    html_file.close()
print("Done")