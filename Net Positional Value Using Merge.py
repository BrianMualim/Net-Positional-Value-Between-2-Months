import csv
import pandas as pd
import numpy as np

# firstMonth should be the earlier month
# Must be in Month[:3]-Year Format
firstMonth = "Apr-2023"
secondMonth = "May-2023"

stocksFirstMonthNAVcsv = pd.read_csv("C:\\Users\\brian\\Downloads\\Stocks NAV Tables\\Stocks NAV Tables " + firstMonth + ".csv")
cleanDataFirstMonthNAVcsv = pd.read_csv(
    "C:\\Users\\brian\\Downloads\\Clean Data for Stocks\\CleanData " + firstMonth + ".csv")
stocksSecondMonthNAVcsv = pd.read_csv("C:\\Users\\brian\\Downloads\\Stocks NAV Tables\\Stocks NAV Tables " + secondMonth + ".csv")
cleanDataSecondMonthNAVcsv = pd.read_csv(
    "C:\\Users\\brian\\Downloads\\Clean Data for Stocks\\CleanData " + secondMonth + ".csv")

lq45ListofStocksNAVcsv = pd.read_csv("C:\\Users\\brian\\Downloads\\HPAM\\LQ45.csv")

# Merge clean data and stocks data together, separated by month obviously
firstMonthMergeData = pd.merge(cleanDataFirstMonthNAVcsv, stocksFirstMonthNAVcsv, on='Nama Produk', how='outer')
firstMonthMergeData = firstMonthMergeData.fillna('null')

secondMonthMergeData = pd.merge(cleanDataSecondMonthNAVcsv, stocksSecondMonthNAVcsv, on='Nama Produk', how='outer')
secondMonthMergeData = secondMonthMergeData.fillna('null')

# Turn percentage and AUM into float64s
firstMonthMergeData['Percentage'] = pd.to_numeric(firstMonthMergeData['Percentage'], errors='coerce') \
    .astype(pd.Float64Dtype())
firstMonthMergeData['AUM'] = pd.to_numeric(firstMonthMergeData['AUM'], errors='coerce') \
    .astype(pd.Float64Dtype())
secondMonthMergeData['Percentage'] = pd.to_numeric(secondMonthMergeData['Percentage'], errors='coerce') \
    .astype(pd.Float64Dtype())
secondMonthMergeData['AUM'] = pd.to_numeric(secondMonthMergeData['AUM'], errors='coerce') \
    .astype(pd.Float64Dtype())

firstMonthMergeData['Percent * AUM'] = np.where(firstMonthMergeData['Percentage'].isnull()
                                                | firstMonthMergeData['AUM'].isnull(),
                                                -1, firstMonthMergeData['Percentage'] *
                                                firstMonthMergeData['AUM'] / 100)
secondMonthMergeData['Percent * AUM'] = np.where(secondMonthMergeData['Percentage'].isnull()
                                                 | secondMonthMergeData['AUM'].isnull(),
                                                 -1, secondMonthMergeData['Percentage'] *
                                                 secondMonthMergeData['AUM'] / 100)


firstMonthMergeData['Percent * AUM'] = pd.to_numeric(firstMonthMergeData['Percent * AUM'], errors='coerce') \
    .astype(pd.Float64Dtype())

secondMonthMergeData['Percent * AUM'] = pd.to_numeric(secondMonthMergeData['Percent * AUM'], errors='coerce') \
    .astype(pd.Float64Dtype())

portfolioCodeLQ45 = lq45ListofStocksNAVcsv['Portfolio Code']

portfolioCodeFirstMonthCleanHeader = firstMonthMergeData['Portfolio Code']
aumPerStockFirstMonthColumn = firstMonthMergeData['Percent * AUM']

portfolioCodeSecondMonthCleanHeader = secondMonthMergeData['Portfolio Code']
aumPerStockSecondMonthColumn = secondMonthMergeData['Percent * AUM']

dataFirstMonth = []
dataSecondMonth = []

for i in range(len(portfolioCodeLQ45)):
    counter = 0
    stockAUM = 0
    for j in range(len(portfolioCodeFirstMonthCleanHeader)):
        if portfolioCodeLQ45[i] == portfolioCodeFirstMonthCleanHeader[j].upper():
            counter += 1
            if aumPerStockFirstMonthColumn[j] != -1:
                stockAUM += aumPerStockFirstMonthColumn[j]

    dictionary = {
        "Portfolio Code": portfolioCodeLQ45[i],
        "Counter of MIs": counter,
        "Stock AUM " + firstMonth: stockAUM
    }
    dataFirstMonth.append(dictionary)


stockAUM = 0
for i in range(len(portfolioCodeLQ45)):
    counter = 0

    for j in range(len(portfolioCodeSecondMonthCleanHeader)):
        if portfolioCodeLQ45[i] == portfolioCodeSecondMonthCleanHeader[j].upper():
            counter += 1
            if aumPerStockSecondMonthColumn[j] != -1:
                stockAUM += aumPerStockSecondMonthColumn[j]

    dictionary = {
        "Portfolio Code": portfolioCodeLQ45[i],
        "Counter of MIs": counter,
        "Stock AUM " + secondMonth: stockAUM
    }
    dataSecondMonth.append(dictionary)
    stockAUM = 0

firstMonthDF = pd.DataFrame(dataFirstMonth)
secondMonthDF = pd.DataFrame(dataSecondMonth)

combined_df = pd.concat([secondMonthDF[['Portfolio Code', 'Stock AUM ' + secondMonth]], firstMonthDF[['Stock AUM ' + firstMonth]]], axis=1)
combined_df['Stock AUM Difference'] = combined_df['Stock AUM ' + secondMonth] - combined_df['Stock AUM ' + firstMonth]
combined_df.to_csv("C:\\Users\\brian\\Downloads\\Net Positional Using Merge " + firstMonth + " to " + secondMonth + ".csv")


