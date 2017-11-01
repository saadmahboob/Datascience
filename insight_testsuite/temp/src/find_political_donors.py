import sys
import time
import statistics
import datetime

def isValid(item, category):
    # OTHER_ID should be empty for "individual contributions"
    if category == 'OTHER_ID':
        return item == ''
    
    # invalid CMTE_ID: not alphanumeric, lenth is not 9
    if category == 'CMTE_ID':
        if not item.isalnum() or len(item) != 9:
            return False
    
    # invalid TRANSACTION_AMT: empty, not a number, <0
    if category == 'TRANSACTION_AMT':
        if not item:
            return False
        try:
            float(item)
        except(ValueError, TypeError):
            return False
        if float(item) < 0:
            return False
        
    # invalid ZIP_CODE: not digit, lenth not in 5~9     
    if category == 'ZIP_CODE':
        if not item.isdigit() or len(item) < 5 or len(item) > 9:
            return False
        
    # invalid TRANSACTION_DT: empty, not digit, malformed, not in 2015~2017    
    if category == 'TRANSACTION_DT':
        if not item.isdigit() or len(item) != 8:
            return False
        year, month, day = int(item[4:]), int(item[:2]), int(item[2:4])
        try:
            newDate = datetime.datetime(year, month, day)
        except ValueError:
            return False
        if year > 2017 or year < 2015:
            return False
            
    return True



def main():
    print("Loading...")
    
    input_path = './input/itcont.txt'
    output_zip = './output/medianvals_by_zip.txt'
    output_date = './output/medianvals_by_date.txt'
    
    if len(sys.argv) == 4:
        input_path = sys.argv[1]
        output_zip = sys.argv[2]
        output_date = sys.argv[3]
    else:
        print(" Path Error" )
        return
        
    zipcode_dic = {}
    date_dic = {}
    with open(input_path, "r") as inputfile:
        with open(output_zip, "w") as outputfile:
            for current_line in inputfile:
                if current_line == '\n':
                    continue
                # split the line to get the information each filed which is divided by '|'
                line_list = current_line.split('|')
                               
                # line_list[0]: "CMTE_ID", line_list[10][:5]: "ZIP_CODE" (first 5 digits), line_list[13]: "TRANSACTION_DT", line_list[14]: "TRANSACTION_AMT"
                # The key of zipcode_dic is "id_zip", which is combined by id+zipcode, because if one id had 2 contributions with different zipcode, they should be different in this file. 
                #print(line_list)
                CMTE_ID = line_list[0]
                ZIP_CODE = line_list[10]
                TRANSACTION_DT = line_list[13]
                TRANSACTION_AMT = line_list[14]
                OTHER_ID = line_list[15]
                
                if not isValid(OTHER_ID, 'OTHER_ID') or not isValid(CMTE_ID, 'CMTE_ID') or not isValid(TRANSACTION_AMT, 'TRANSACTION_AMT'):
                    continue
                
                if isValid(ZIP_CODE, 'ZIP_CODE'):
                    ZIP_CODE = line_list[10][:5]                
                    id_zip = CMTE_ID + ZIP_CODE
                    
                    
                    # zipcode_dic[id_zip] records the contributions history until now of this id and this zipcode
                    if not id_zip in zipcode_dic:
                        zipcode_dic[id_zip] = [int(TRANSACTION_AMT)]
                    else:
                        zipcode_dic[id_zip].append(int(TRANSACTION_AMT))
                        
                    # calculate the current median
                    median = statistics.median(zipcode_dic[id_zip])
                    median = round(median)
                    
                    # write to file
                    outputfile.write(CMTE_ID + '|' + ZIP_CODE + '|' + str(median) + '|' + str(len(zipcode_dic[id_zip])) + '|' + str(sum(zipcode_dic[id_zip])))
                    outputfile.write('\n')
                
                # similar as previous zipcode_dic, build the date_dic
                if isValid(TRANSACTION_DT, 'TRANSACTION_DT'):

                    id_date = CMTE_ID + TRANSACTION_DT
                    if not id_date in date_dic:
                        date_dic[id_date] = [int(TRANSACTION_AMT)]
                    else:
                        date_dic[id_date].append(int(TRANSACTION_AMT))
                                
    print("Medianvals_by_zip complete")
    
    # After all the input read and date_dic built, calculate median and write to file
    with open(output_date, "w") as outputfile:
        # sort the id_date by alphabetical and chronologically in date_list
        date_list = []
        for i in date_dic:
            date_list.append(i)
        date_list.sort()
        for i in date_list:
            CMTE_ID = i[:9]
            TRANSACTION_DT = i[9:]
            median = round(statistics.median(date_dic[i]))
            outputfile.write(CMTE_ID + '|' + TRANSACTION_DT + '|' + str(median) + '|' + str(len(date_dic[i])) + '|' + str(sum(date_dic[i])))
            outputfile.write('\n')

    print("Medianvals_by_date complete...")                    

    
start_time = time.time()
main()
print("Total time: {} seconds".format(round(time.time() - start_time)))    
                
            

