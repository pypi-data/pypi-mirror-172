import csv
import datetime
import pandas as pd
import os
# import asyncio
# import aiofiles
# from aiocsv import AsyncWriter


class DataWriter:
    """Create a csv to log data with a list after defining a header
    
    First create logger object and defining its modes.
    Second, create a header for the csv or .txt file.
    Finally write the rows to the csv."""

    def __init__(self, filename="dataLog", output_direct="Data", replace_file=False, timestamp=True, silent=False, txtmode=False):
        
        # intialize silent/timestamp mode bool
        self._silent = silent
        self._timestamp = timestamp
        self._txtmode = txtmode

        # Define .csv name
        csv_ts = datetime.datetime.now()
        if self._txtmode == False:
            csv_filename = "{}_{}.csv".format(filename, csv_ts.strftime("%m-%d"))
        else:
            csv_filename = "{}_{}.txt".format(filename, csv_ts.strftime("%m-%d"))
            

        # create path to access data .csv file
        current_direct = os.getcwd()
        self.csv_folder = os.path.join(current_direct, output_direct)
        self._csv_path = os.path.sep.join((self.csv_folder, csv_filename))

        # Create data folder
        if not os.path.exists(self.csv_folder):
            os.mkdir(self.csv_folder)
        # self._csv_path = os.path.join(current_direct, csv_filename)

        # Create empty .csv if it has not been initialized or delete old file instance
        if replace_file == True and os.path.exists(self._csv_path) or not os.path.exists(self._csv_path):
            open(self._csv_path, 'w').close()

            
    # Define setter/getter properties to toggle Silent mode
    @property
    def silent(self):
        return self._silent
    
    @silent.setter
    def silent(self, mode):
        if isinstance(mode, bool):
            self._silent = mode
        else:
            print("Please input a bool.")


    def write_header(self, *args, ignore_old_header=False):
        # take either a list type or unspecified args
        header = self.args_to_list(*args)
        
        # save header length after initializing it
        if self._timestamp == True:
            header.append("Timestamp")
        self.col_count = len(header)
        
        if self._txtmode == False:
            # Create fresh header   or  rewrite old header  or  break from script
            try:
                # load pandas data frame to see if file exists already
                df = pd.read_csv(self._csv_path, on_bad_lines='skip') # or pd.read_excel(filename) for xls file
                # avoid user input for function guidance
                if ignore_old_header == True:
                    return
                
                # act upon header depending on user feedback
                user_feedback = input("Header detected! Press \n\t[enter] to keep old header or \n\t[anykey+enter] to overwrite current header or\n\t[b+enter] to break from script\n")
                if user_feedback == "":
                    pass
                elif user_feedback == "b":
                    raise AttributeError("csv already has header row.")
                else:
                    df.columns = header
                    df.to_csv(self._csv_path, index=False)
                
            # .csv is empty. Thus, create a new header for file.
            except pd.errors.EmptyDataError:
                # no header made, so create a new one
                with open(self._csv_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    # write the header
                    writer.writerow(header)
            
        # txt mode
        else:
            header_str = ""
            for i, data in enumerate(header):
                if i == len(header)-1:
                    header_str += str(data) + "\n"
                else:
                    header_str += str(data) + ","
                    
            with open(self._csv_path, "w") as f:
                f.write(header_str)
                
                
    def write_row(self, *args):
        # take either a list type or unspecified args
        list_ = self.args_to_list(*args)
        
        # create timestamp data
        if self._timestamp == True:
            ts = datetime.datetime.now()
            timestamp = "{}".format(ts.strftime("%m/%d/%Y %H:%M:%S"))
            
        try:
            # check if .col_count variable has been initialized.
            x = self.col_count
        except AttributeError:
            try:
                # check how many columns if self.col_count not initialized
                with open(self._csv_path) as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    self.col_count = len(header)
                    
            # Error raised if there is no header in the .csv yet
            except StopIteration:
                # break from script and request a new header
                raise AttributeError("CSV needs a header before rows can be written")
        
        # find ending index of data for list conditioning 
        if self._timestamp == True:
            data_end_index = self.col_count - 1
        else:
            data_end_index = self.col_count
        # conditioning the data list_ to maintain timestamp row and throw warnings if not on silent.
        if len(list_) < (data_end_index):
            if self._silent == False:
                print("[CSV LOGGER] Less variables than there are columns. Columns {} through {} will be NaN.".format(len(list_)+1, data_end_index))
            for _ in range(0, (data_end_index-len(list_))):
                list_.append(None)
            if self._timestamp == True:
                list_.append(timestamp)
        elif len(list_) > (data_end_index):
            if self._timestamp == True:
                list_.insert(data_end_index, timestamp)
            if self._silent == False:
                print("[CSV LOGGER] Warning, more variables are being passed in than columns. All data indexed beyond {} will be included in columns wihthout headers.".format(self.col_count-2))
        else:
            if self._timestamp == True:
                list_.append(timestamp)

        # write row after conditioning list 
        with open(self._csv_path, 'a', newline='') as f:
            if self._txtmode == False:
                writer = csv.writer(f)
                # write the row
                writer.writerow(list_)
            else:
                row_str = ""
                for i, data in enumerate(list_):
                    if i == len(list_)-1:
                        row_str += str(data) + "\n"
                    else:
                        row_str += str(data) + ","
                f.write(row_str)
                
                    
    # async def consume(self, que: asyncio.Queue) -> None:
    #     while True:
    #         args = que.get()                
    #         await self.write_row(*args)
    #         que.task_done()
                
        
    # async def main(self, que: asyncio.Queue, ncon: int):
    #     consumers = [asyncio.create_task(self.consume(que)) for _ in range(ncon)]
    #     await que.join()  # Implicitly awaits consumers, too
    #     for c in consumers:
    #         c.cancel()

                
    def args_to_list(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            list_ = args[0]
        else:
            list_ = list(args)
        return list_      
            
def test():
    datalogger = DataWriter("test1", timestamp=True, silent=False, output_direct="deleteMe")
    data = ["55", "yes", None]
    # map(lambda x: [x], data)
    datalogger.write_header(["header1", True, 10], ignore_old_header=True)
    datalogger.write_row(data)
    datalogger.write_row(["poop", 666, "yup"])
    datalogger.write_row([33, 25, 12, None])
    datalogger.write_row(["I am here!"])
    datalog2 = DataWriter("test2", timestamp=False, silent = True, output_direct="deleteMe", replace_file=True)
    datalog2.write_header(["header1", 2, [33, 44], (15,1)])
    datalog2.write_row([])
    datalog2.silent = False
    datalog2.timestamp = True
    datalog2.write_row([True, None, 333, "hello"])
    datalog2.write_row([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    datalog2.write_header([33333333, "blep:"], ignore_old_header=True)
    datalog2.write_row([1])
    datalog2.write_row(3, 4, 'bleh', True, (1, 2), [5, '6'])
    datalog2.write_row([12345.6789123456789, "1.23456789E8"])
    
    log3 = DataWriter("test3", timestamp=True, silent=True, txtmode=True, output_direct="deleteMe", replace_file=True)
    log3.write_header(["col1", "col2", 3, 4.0])
    log3.write_row(["1", "2", 3, 4])
    log3.write_row([True, False, None, 1])
    log3.write_row(["yes"])
    log3.write_row(["go", 2, 3, 4, 5, 6, 7])
    
    serial = 38
    setpoint = 45
    avg_freq = "3.777777E8"
    std_freq = "1.23456789E7"
    log4 = DataWriter("SN0{}".format(serial), timestamp=True, silent=True, txtmode=True, output_direct="deleteMe")
    log4.write_header(["Serial Number", 'Set Point [C]', 'Frequency [Hz]', 'STDEV'])
    log4.write_row([serial, setpoint, repr(float(avg_freq)), repr(float(std_freq))])
    
    import time
    # s = time.perf_counter()
    # q = asyncio.Queue()
    # log5 = dataLogger("test5", timestamp=True, silent=True, txtmode=False, output_direct="deleteMe", replace_file=True)
    # log5.write_header(["Clo 1", 'Col2', 'Col3', 'Col4', 'Col5'])
    # for i in range(1000):
    #     q.put(i, i+1, i+2, i+3, i+4, i+5)
    # log5.main(q, 2)
    # elapsed = time.perf_counter() - s
    # print(f"async executed in {elapsed:0.4f} seconds.")
    
    s =  time.perf_counter()
    log6 = DataWriter("test6", timestamp=True, silent=True, txtmode=False, output_direct="deleteMe", replace_file=True)
    log6.write_header(["Clo 1", 'Col2', 'Col3', 'Col4', 'Col5'])
    s = time.perf_counter()
    for i in range(10000):
        log6.write_row(i, i+1, i+2, i+3, i+4, i+5)
    elapsed = time.perf_counter() - s
    print(f"sync executed in {elapsed:0.4f} seconds.")




if __name__ == "__main__":
    test()

