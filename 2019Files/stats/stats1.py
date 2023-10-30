# -*- coding: utf-8 -*-
import pymysql
import sys
from matplotlib import pyplot as plt
from matplotlib import ticker
import fiscalYearCovnert

connection_to_Database = pymysql.connect(
    host        = "localhost"
    ,user       = "root"
    ,passwd     = "stufsno1"
    ,db         = "financials"
    ,use_unicode= True
    ,charset    = "utf8"
)
yearContextValueUnit= [] # This will hold year, context, value and unit
years               = [] # Fiscal year ending
y_Value             = []
decimalList         = []
EnglishLabelList    = []
unitDigitLabel      = '' # if 3, thousand, if 6, million
label_English       = ''
contentInConcept    = '現金及び預金'

try:
    cursor_for_SQL  = connection_to_Database.cursor()
    tempQueryText   = 'SELECT contextRef, instant, value, decimals, label_e FROM InstanceWithConcepts'\
                    + ' WHERE label_j = %s'
    valuesForTempQueryText = [contentInConcept]
    cursor_for_SQL.execute(tempQueryText, valuesForTempQueryText)
    resultFromQuery = cursor_for_SQL.fetchall()
    connection_to_Database.commit()

    for row in resultFromQuery: # Store the records that are downloaded from SQL to python list
        yearFromSQL = row[1][0:4] + row[1][5:-3]
        years.append(yearFromSQL)
        unitDigit = abs(int(row[3]))
        y_ValueFromSQL = row[2] / (10 ** unitDigit)
        decimalList.append(unitDigit)
        y_Value.append(y_ValueFromSQL)
        EnglishLabelList.append(row[4])
        context = row[0]
        if context == 'CurrentYearInstant' or context == 'Prior1YearInstant' :
            yearContextValueUnit.append({
                'Year': yearFromSQL
                ,'Context': context
                ,'Value': y_ValueFromSQL
                ,'Unit': unitDigit
            })

    deleteIndexList = []
    for i in range(0, len(yearContextValueUnit)):
        if yearContextValueUnit[i].get('Context') == 'Prior1YearInstant':
            for j in range(0, len(yearContextValueUnit)):
                if i != j:
                    if yearContextValueUnit[i].get('Year') == yearContextValueUnit[j].get('Year'):
                        if yearContextValueUnit[i].get('Context') != yearContextValueUnit[j].get('Context'):
                            if yearContextValueUnit[i].get('Value') == yearContextValueUnit[j].get('Value'):
                                deleteIndexList.append(i) # If the value is same, delte the value with Prior1YearInstant context
    for index in sorted(deleteIndexList, reverse=True):
        del yearContextValueUnit[index]

    # Check if the English labels are the same
    if (len(set(EnglishLabelList)) == 1):
        label_English += EnglishLabelList[0]
    else:
        print('English label is not consistent.')

    # Check if the decimals are the same
    if (len(set(decimalList)) == 1):
        if decimalList[0] == 3:
            unitDigitLabel += 'Thousand'
        elif decimalList[0] == 6:
            unitDigitLabel += 'Million'
    else:
        print('The unit is not consistent.')

    for row in yearContextValueUnit: print(row)
    plt.bar(years, y_Value, label = label_English)
    #plt.bar(years, y_Value)
    plt.ylabel(unitDigitLabel+' JPY')
    plt.xlabel('YearEnd')
    plt.title(label_English)
    plt.legend()
    plt.show()

except:
    connection_to_Database.rollback()
    print(sys.exc_info())
