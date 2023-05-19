import datetime
import glob
import pandas as pd
import math
from datetime import timedelta
import os

def convertPressure2At(pressure):
    return  44330 * [1 - (pressure / 1013.25)**(1 / 5.255)]
def convertAtl2Pressure(alt):
    return 1013.25 * (1 - (2.25577 / 10 ** 5) * alt) ** 5.25588
def convertTemp2Theta(Temp, pressure):
    return Temp * math.pow(1000 / pressure, 0.286)
def convertRH2QV(rh, temperature, press = 101325):
    Tc = temperature - 273.15
    es = 6.112 * math.exp((17.67 * Tc) / (Tc + 243.5))
    e = rh * es
    p_mb = press / 100.
    qv = (0.622 * e) / (p_mb - (0.378 * e))
    return qv
class NearSurface():
    def __init__(self, filefolder, aim_date, z, soil_z, site_alt, tempdiff):
        self.tempdiff = tempdiff
        self.filefolder = filefolder
        self.aim_date = datetime.datetime.strptime(aim_date, '%Y/%m/%d %H:%M:%S') + timedelta(hours=8)
        self.z = z
        self.soil_z = soil_z
        self.site_alt = site_alt
        self.theta = []
        self.temp = []
        self.qv = []
        self.soilT = []
        self.files = []
        self.getfiles()
        self.getDataInFixedDate()
        self.alt = [self.site_alt + h for h in self.z]

    def getfiles(self):
        for root, dirs, files in os.walk(self.filefolder):
            for file in files:
                self.files.append(os.path.join(root, file))
        # self.files = glob.glob(self.filefolder + '*')
        self.files = sorted(self.files)


    def getDataInFixedDate(self):
        aim_file = ''
        aim_line = -1
        for file in self.files:
            df = pd.read_csv(file)
            before_date = datetime.datetime(year=int(df['Year'][0]), month=int(df['Month'][0]), day=int(df['Day'][0]),
                                            hour=int(df['Hour'][0]), minute=int(df['Minute'][0]),
                                            second=int(df['Second'][0]))
            count = 0
            for year, month, day, hour, min, sec in zip(df['Year'][1:], df['Month'][1:], df['Day'][1:], df['Hour'][1:],
                                                        df['Minute'][1:], df['Second'][1:]):
                after_date = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour),
                                               minute=int(min), second=int(sec))
                before_diff = (before_date - self.aim_date).total_seconds()
                after_diff = (after_date - self.aim_date).total_seconds()
                if abs(after_diff) >= abs(before_diff):
                    aim_file = file
                    aim_line = count
                    break
                before_date = after_date
                count += 1
            if aim_file != '' and aim_line != -1:
                print('NearSurface Find data closet to aim date:', aim_file, aim_line, " (BJT):",before_date)
                df = pd.read_csv(aim_file)
                for i in self.z:
                    name = 'Ta_' + str(i) + 'M_Avg'
                    ta = df[name][aim_line] + self.tempdiff
                    pa = convertAtl2Pressure(self.site_alt + i)
                    self.temp.append(ta + 273.15)
                    self.theta.append(convertTemp2Theta(ta + 273.15, pa))
                    ####相对湿度计算比湿
                    name = 'RH_' + str(i) + 'M_Avg'
                    rha = df[name][aim_line] * 0.01
                    self.qv.append(convertRH2QV(rha, ta + 273.15))
                for i in self.soil_z:
                    name = 'T_Soil_' + format(i * 100, '.0f') + 'CM_Avg'
                    self.soilT.append(df[name][aim_line] + 273.15)
                break
        pass
