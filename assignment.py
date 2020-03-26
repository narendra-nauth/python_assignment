import matplotlib.pyplot as plt
import numpy as np
import tabulate as tt
import csv
import statistics


countryNames = []
hivData      = []

filename     = 'hiv.csv'
mainlabel    = 'HIV Cases 2010 - 2018'
yearCount    = 9
title        = 'HIV Cases'
labels       = 0

def importedData():
    with open(filename, 'r') as hivFile:
        reader = csv.reader(hivFile)
        for col in reader:
            countryNames.append(col[0])
            
            coldata = []
            for i in range(1, 10):
                if(col[i]):
                    coldata.append(int(col[i]))
                else:
                   coldata.append(0)
                
            hivData.append(coldata)

def calculateYearTotals():
    totals = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for country in countryNames:
        if countryNames.index(country) != 0:
            totals[0] += hivData[countryNames.index(country)][0]
            totals[1] += hivData[countryNames.index(country)][1]
            totals[2] += hivData[countryNames.index(country)][2]
            totals[3] += hivData[countryNames.index(country)][3]
            totals[4] += hivData[countryNames.index(country)][4]
            totals[5] += hivData[countryNames.index(country)][5]
            totals[6] += hivData[countryNames.index(country)][6]
            totals[7] += hivData[countryNames.index(country)][7]
            totals[8] += hivData[countryNames.index(country)][8]
    return totals

def promptUser():
    print('Select From Menu Below:')
    print('1 - Total Number of HIV Cases Per Year')
    print('2 - Total Number of HIV Cases Per Country')
    print('3 - Average Number of HIV Cases Per Year')
    print('4 - Average Number of HIV Cases Per Country')
    print('5 - Highest & Lowest Average Cases By Country')
    print('6 - Highest & Lowest Total Cases By Year')
    print('7 - Relational Increase/Decrease Based On Years & Totals')
    print('8 - Predicted Total By Year')
    print('9 - LineGraph: Total HIV Cases Per Year')
    print('10 - LineGraph: Country HIV Cases Per Year')
    print('11 - Histogram: Total HIV Cases Per Year')
    print('12 - Histogram: Country HIV Cases Per Year')
    print('q - Quit')

def totalCasesByYear():
    totals = calculateYearTotals()
    print('\nTotal HIV Cases Per Year')
    tableData = []
    for i in range(0, yearCount):
        record = [hivData[labels][i], totals[i]]
        tableData.append(record)

    print(tt.tabulate(tableData, ["Year", "Total"]))
    print('\n')

def totalCasesByCountry():
    print('\nTotal HIV Cases By Country')
    tableData = []
    for country in countryNames:
        index = countryNames.index(country)
        if  index != 0:
            total = 0
            for i in hivData[index]:
                total += i
            record = [country, total]
            tableData.append(record)
    print(tt.tabulate(tableData, ["Country", "Total"]))
    print('\n')

def avgCasesByYear():
    totals = calculateYearTotals()
    count  = 0
    for country in countryNames:
        index = countryNames.index(country)
        if  index != 0:
            count += 1
    print('\nAverage HIV Cases Per Year')
    tableData = []
    for i in range(0, yearCount):
        totals[i] = round(totals[i] / count, 2)
        record = [hivData[labels][i], totals[i]]
        tableData.append(record)
    print(tt.tabulate(tableData, ["Year", "Average"]))
    print('\n')

def avgCasesByCountry():
    print('\nAverage HIV Cases Per Year')
    tableData = []
    for country in countryNames:
        index = countryNames.index(country)
        if  index != 0:
            average  = round(statistics.mean(hivData[index]), 2)
            record = [country, average]
            tableData.append(record)
    print(tt.tabulate(tableData, ["Country", "Average"]))
    print('\n')

def highLowAverageCountry():
    countries = []
    averages  = []
    for country in countryNames:
        index = countryNames.index(country)
        if  index != 0:
            average  = round(statistics.mean(hivData[index]), 2)
            countries.append(country)
            averages.append(average)
    min_val = min(averages)
    min_ind = averages.index(min_val)
    max_val = max(averages)
    max_ind = averages.index(max_val)
    print('\nHighest & Lowest Average Cases By Country')
    tableData = []
    tableData.append([countries[min_ind], "Minimum Average", min_val])
    tableData.append([countries[max_ind], "Maximum Average", max_val])
    print(tt.tabulate(tableData, ["Country", "Category", "Average"]))
    print('\n')

def highLowTotalYear():
    totals = calculateYearTotals()
    min_val = min(totals)
    min_ind = totals.index(min_val)
    max_val = max(totals)
    max_ind = totals.index(max_val)
    print('\nHighest & Lowest Total Cases By Year')
    tableData = []
    tableData.append([hivData[labels][min_ind], "Minimum Total", min_val])
    tableData.append([hivData[labels][max_ind], "Maximum Total", max_val])
    print(tt.tabulate(tableData, ["Year", "Category", "Total"]))
    print('\n')

def relationIncreaseDecrease():
    years   = hivData[labels]
    totals  = calculateYearTotals()
    corr    = np.corrcoef(years, totals)
    coef    = round(corr[0][1], 2)
    print('\nCorrelation Coefficient For Years & Totals:',coef)
    if 0.1 <= coef <= 0.2:
        print('Relation Shows A Weak Increase In Totals')
    elif 0.21 <= coef <= 0.79:
        print('Relation Shows A Moderate Increase In Totals')
    elif 0.8 <= coef <= 1:
        print('Relation Shows A Strong Increase In Totals')
    elif -0.1 >= coef >= -0.2:
        print('Relation Shows A Weak Decrease In Totals')
    elif -0.21 >= coef >= -0.79:
        print('Relation Shows A Moderate Decrease In Totals')
    elif -0.8 >= coef >= -1:
        print('Relation Shows A Strong Decrease In Totals')
    elif coef == 0:
        print('Relation Shows No Change In Totals')
    print('\n')

def predictedTotalByYear():
    year = input('\nEnter Year For Predicted Total: ')
    x_values = np.array(hivData[labels], dtype=np.float64)
    y_values = np.array(calculateYearTotals(), dtype=np.float64)
    m, b = best_fit_line(x_values, y_values)
    total_prediction = (m * int(year)) + b
    print('Predicted Total:', round(total_prediction,2))
    print('\n')

def best_fit_line(x_values, y_values):
    m = (((statistics.mean(x_values) * statistics.mean(y_values)) - statistics.mean(x_values * y_values)) /
         ((statistics.mean(x_values) * statistics.mean(x_values)) - statistics.mean(x_values * x_values)))

    b = statistics.mean(y_values) - m * statistics.mean(x_values)
    return m, b

def graphlabels(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()

def totalLinegraph():
    totals = calculateYearTotals()
    plt.plot(hivData[labels], totals, label='Total '+title)
    graphlabels('Year', 'Total '+title, 'Total '+mainlabel)
    plt.show()
    print('\n')

def countryLinegraph():
    country = input('Enter Country Name: ')
    if country in countryNames:
        index = countryNames.index(country)
        plt.plot(hivData[labels], hivData[index], label=country+' '+title)
        graphlabels('Year', title, country+' '+mainlabel)
        plt.show()
        print('\n')
    else:
        print('Country Entered Is Invalid')
        print('\n')

def totalHistogram():
    totals = calculateYearTotals()
    plt.bar(hivData[labels], totals, label='Total '+title, width=1.0)
    graphlabels('Year', title, 'Total '+mainlabel)
    plt.show()
    print('\n')

def countryHistogram():
    country = input('Enter Country Name: ')
    if country in countryNames:
        index = countryNames.index(country)
        plt.bar(hivData[labels], hivData[index], label=country+' '+title, width=1.0)
        graphlabels('Year', title, country+' '+mainlabel)
        plt.show()
        print('\n')
    else:
        print('Country Entered Is Invalid')
        print('\n')
       
def Main():
    importedData()

    while True:
        promptUser()
        opt = input()

        if(opt == '1'):
            totalCasesByYear()
        if(opt == '2'):
            totalCasesByCountry()
        if(opt == '3'):
            avgCasesByYear()
        if(opt == '4'):
            avgCasesByCountry()
        if(opt == '5'):
            highLowAverageCountry()
        if(opt == '6'):
            highLowTotalYear()
        if(opt == '7'):
            relationIncreaseDecrease()
        if(opt == '8'):
            predictedTotalByYear()
        if(opt == '9'):
            totalLinegraph()
        if(opt == '10'):
            countryLinegraph()
        if(opt == '11'):
            totalHistogram()
        if(opt == '12'):
            countryHistogram()
        if(opt == 'q'):
            break
    
Main()
    
