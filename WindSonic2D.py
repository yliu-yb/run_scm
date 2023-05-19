import glob
import pandas as pd
import time
import datetime
from datetime import timedelta
import os
from numpy import ma

class WindSonic2D():
    def __init__(self, filefolder, aim_date, z, site_alt):
        self.filefolder = filefolder
        self.aim_date = datetime.datetime.strptime(aim_date, '%Y/%m/%d %H:%M:%S') + timedelta(hours=8)
        self.site_alt = site_alt
        self.z = z
        self.u = []
        self.v = []
        self.files = []
        self.getfiles()
        self.getDataInFixedDate()
        self.alt = [self.site_alt + h for h in self.z]

    def getfiles(self):
        for root, dirs, files in os.walk(self.filefolder):
            for file in files:
                self.files.append(os.path.join(root, file))
        self.files = sorted(self.files)
        # self.files = glob.glob(self.filefolder+'*')


    def getDataInFixedDate(self):
        aim_file = ''
        aim_line = -1
        for file in self.files:
            df = pd.read_csv(file)
            before_date = datetime.datetime(year=int(df['Year'][0]), month=int(df['Month'][0]), day=int(df['Day'][0]),
                                            hour=int(df['Hour'][0]),minute=int(df['Minute'][0]),second=int(df['Second'][0]))
            count = 0
            for year, month, day, hour, min, sec in zip(df['Year'][1:], df['Month'][1:], df['Day'][1:], df['Hour'][1:], df['Minute'][1:], df['Second'][1:]):
                after_date = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(min),second=int(sec))
                before_diff = (before_date - self.aim_date).total_seconds()
                after_diff = (after_date - self.aim_date).total_seconds()
                if abs(after_diff) >= abs(before_diff):
                    aim_file = file
                    aim_line = count
                    break
                before_date = after_date
                count += 1
            if aim_file != '' and aim_line != -1:
                print('WindSonic2D Find data closet to aim date:', aim_file, aim_line, " (BJT):",before_date)
                df = pd.read_csv(aim_file)
                for i in self.z:
                    name = 'U_' + str(i) + 'M'
                    if i == 35:
                        name += '_1'
                    self.u.append(df[name][aim_line])
                    name = 'V_' + str(i) + 'M'
                    if i == 35:
                        name += '_1'
                    self.v.append(df[name][aim_line])
                print(self.z)
                print(self.u, self.v)
                # if max(abs(self.u)) > 1000 or max(abs(self.v)):
                #     exit()
                break


