from datetime import datetime
import os

#class to store the required information of a particular ip address
class node:
    def __init__(self,ip,first,last,cik,accession,extension):
        #output to log file
        self.ip = ip
        self.first = first
        self.last = last
        doc_id = cik+accession+extension
        self.document = set([doc_id])

#write to output log file
#params: noder: type node
def write_to_logfile(noder):
    output_filename = "./output/sessionization.txt"
    file = open(output_filename,'a')
    file.write(noder.ip+","+noder.first.strftime('%Y-%m-%d %H:%M:%S') +","+noder.last.strftime('%Y-%m-%d %H:%M:%S') + ","+str(int((noder.last - noder.first).total_seconds())+1) +","+str(len(noder.document)) +"\n")
    file.close()


def main():
    #filenames
    log_filename = "./input/log.csv"
    inactivity_filename = "./input/inactivity_period.txt"
	
    #read the inactivity file and store the timeout duration in a variable
    inactivity = open(inactivity_filename,'r')
    timeout = float(inactivity.read())
    inactivity.close()

    #read the log filename and process the information
    log = open(log_filename,'r')

    #store the first line in a dictionary
    #this creates a mapping between the column name and the column number
    columns = log.readline().split(',')
    column_mapping = {}
    for i in range(len(columns)):
        column_mapping[columns[i]] = i

    #process the rest of the lines in log file one by one
    main_dict = {} #stores the mapping between ipadress: node associated with it
    list = [] #stores the list of ipaddress in the oreder of their visit
    while True:
        line = log.readline()
        if not line:
            break

        #split the input line into all columns and store the required ones in variable
        values = line.split(',')
        ip = values[column_mapping['ip']]
        date_time_value = values[column_mapping['date']] + ":" + values[column_mapping['time']]
        time = datetime.strptime(date_time_value, '%Y-%m-%d:%H:%M:%S')
        cik = values[column_mapping['cik']]
        accession = values[column_mapping['accession']]
        extention = values[column_mapping['extention']]

        #on every new entry check the list nodes whether any of them have timedout
        #if timedout, write entry to output logfile
        #delete from dict and list
        for ipn in list:
            if (time - main_dict[ipn].last).total_seconds() > timeout:
                write_to_logfile(main_dict[ipn])
                list.remove(ipn)
                main_dict.pop(ipn)
        #create a new entry in main_dict and list if the ip is not seen before
        #or has been deleted previously
        if ip not in main_dict:
            list.append(ip)
            new_node = node(ip,time,time,cik,accession,extention)
            main_dict[ip] = new_node
        #if present update the node with current node items
        else:
            main_dict[ip].last = time
            main_dict[ip].document.add(cik+accession+extention)
            main_dict[ip].cik = cik
            main_dict[ip].accession = accession
            main_dict[ip].extention = extention
    #at the end of the file as their are no lines to process
    #write all the ips present in the list to logfile
    for ip in list:
        write_to_logfile(main_dict[ip])


if __name__ == '__main__':
    main()