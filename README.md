# Net-Positional-Value-Between-2-Months

Files Needed:
- Stocks NAV Tables for 1st and 2nd month
- Cleaned Data Table for 1st and 2ns month
- List of LQ45 stocks

Coding Process:
1. Used merge functions to merge each "stocks nav table" and "cleaned data table" by month
2. Filled up each blank space with "null" value
3. Set the 'Percentage' and 'AUM' into float64 types so you can multiply them together
4. Create a new column 'Percentage * AUM'
5. Double for loop, if 'Portfolio Code' in 'Stocks Nav Tables' == 'Portfolio Code' in LQ45, add 'Percentage * AUM' by specific stock
6. Format Nicely and Print to CSV File
   

