# Introduction
This is my solution for the Coding challenge of Insight Data Engineering. The challenge can be found at: https://github.com/InsightDataScience/find-political-donors

# Approach

The input file `itcont.txt` lists campaign contributions by individual donors. We’re primarily interested in the zip code associated with the donor, amount contributed, date of the transaction and ID of the recipient. Results were wrote to 2 output files: `medianvals_by_zip.txt` and `medianvals_by_date.txt`.

1. Input file was read line by line
2. Two dictionaries stored the data aggregated by id combines zip code and id combines date
3. Write to medianvals_by_zip.txt dynamically for every valid input line
4. After the entire input file is processed, the results data were sorted and wrote to medianvals_by_date.txt

## Details of input and output files

The Federal Election Commission provides data files stretching back years and is [regularly updated](http://classic.fec.gov/finance/disclosure/ftpdet.shtml)

We are considering the following fields:  

* `CMTE_ID`: identifies the flier, which for our purposes is the recipient of this contribution
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity 

Each line of the first output file `medianvals_by_zip.txt`:
* recipient of the contribution  
* 5-digit zip code of the contributor  
* running median of contributions received by recipient from the contributor's zip code streamed in so far.  
* counts of the contributions from same contributions with the same zip code
* total amount of contributions received by recipient from the contributor's zip code streamed in so far

For example: `C00177436|30004|384|1|384`
 

Each line of the second output file `medianvals_by_date.txt`: 
* recipeint of the contribution 
* date of the contribution  
* median of contributions received by recipient on that date.  to the next dollar) 
* total number of transactions received by recipient on that date
* total amount of contributions received by recipient on that date

For example: `C00177436|01312017|384|4|13823`

Unlike the first output file, this second output file should have lines sorted alphabetical by recipient and then chronologically by date.

# Packages required
* datetime
* time
* sys
* statistics

# Run Instructions
To run this program, simply execute the `./run.sh` in the root directory.
To run the tests, `insight_testsuite~$ ./run_tests.sh`


# Details of the tests
* Test_1: Test case provided by Insight Data Engineering.
* Test_2: Based on test_1, adding some repeat lines
* Test_3: Based on test_1, testing invalid zip code cases, invalid date cases, invalid other non-important fileds cases
* Test_4: It contains the first 50000 lines from the Federal Election Commission 2017-2018 individual contribution file downloaded from [Federal Election Commission](http://classic.fec.gov/finance/disclosure/ftpdet.shtml#a2017_2018), 
