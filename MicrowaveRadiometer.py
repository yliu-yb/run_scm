import os
import datetime
import math

import numpy


def convertRH2QV(rh, temperature, press = 101325):
    Tc = temperature - 273.15
    es = 6.112 * math.exp((17.67 * Tc) / (Tc + 243.5))
    e = rh * es
    p_mb = press / 100.
    qv = (0.622 * e) / (p_mb - (0.378 * e)) #unit (kgkg-1)
    return qv
def convertTemp2Theta(Temp, pressure):
    return Temp * math.pow(1000 / pressure, 0.286)
def convertAtl2Pressure(alt):
    return 1013.25 * (1 - (2.25577 / 10 ** 5) * alt) ** 5.25588

class MicrowaveRadiometer():
    def __init__(self, filefolder, aim_date, site_alt, tempdiff):
        self.tempdiff = tempdiff
        self.fileFolder = filefolder
        self.aim_date = datetime.datetime.strptime(aim_date, '%Y/%m/%d %H:%M:%S')
        self.site_alt = site_alt
        self.rh_files = []
        self.temp_files = []
        self.rh = []
        self.rh_alt = []
        self.temp = []
        self.temp_alt = []
        self.GetFilesFromFolder()
        self.get_RH_InFixedDate()
        self.get_TEMP_InFixedDate()
        self.qv = [convertRH2QV(rh / 100., t_k) for rh, t_k in zip(self.rh, self.temp)]
        self.theta = [convertTemp2Theta(t_k, convertAtl2Pressure(h)) for t_k, h in zip(self.temp, self.temp_alt)]

    def GetFilesFromFolder(self):
        for path, currentDirectory, files in os.walk(self.fileFolder):
            for file in files:
                if file[-7:] == 'HPC.ASC':
                    self.rh_files.append(os.path.join(path, file))
                elif file[-12:] == '.CMP.TPC.ASC':
                    self.temp_files.append(os.path.join(path, file))
        self.rh_files = sorted(self.rh_files)
        self.temp_files = sorted(self.temp_files)
    def get_RH_InFixedDate(self):
        aim_file = ''
        aim_line = -1
        for file in self.rh_files:
            f = open(file, 'r')
            lines = f.readlines()
            height_idx = 0
            rh_idx = 0
            for i in range(len(lines)):
                if height_idx == 0 and lines[i].find("Number of Altitude Levels") >= 0:
                    height_idx = i + 1
                    line = lines[height_idx].split(',')
                    line[len(line) - 1] = 10000
                    Height = list(map(int, line))
                    self.rh_alt = [self.site_alt + h for h in Height]
                if lines[i].find("# Maximum relative Humidity in File") >= 0:
                    rh_idx = i + 2
                    break
            if rh_idx == 0:
                continue
            line = lines[rh_idx].split(',')
            before_date = datetime.datetime(year=int('20' + str(line[0])), month=int(line[1]), day=int(line[2]),
                                            hour=int(line[3]), minute=int(line[4]),second=int(line[5]))
            count = 0
            for line in lines[rh_idx+1:]:
                line = line.split(',')
                after_date = datetime.datetime(year=int('20' + str(line[0])), month=int(line[1]), day=int(line[2]),
                                                hour=int(line[3]), minute=int(line[4]), second=int(line[5]))
                before_diff = (before_date - self.aim_date).total_seconds()
                after_diff = (after_date - self.aim_date).total_seconds()
                if abs(after_diff) >= abs(before_diff):
                    aim_file = file
                    aim_line = rh_idx + count
                    break
                before_date = after_date
                count += 1
            if aim_file != '' and aim_line != -1:
                print('RH Find data closet to aim date:', aim_file, aim_line, " (UTC):", before_date)
                self.rh = list(map(float, lines[aim_line].split(',')[7:]))
                break
    def get_TEMP_InFixedDate(self):
        aim_file = ''
        aim_line = -1
        for file in self.temp_files:
            f = open(file, 'r')
            lines = f.readlines()
            t_height = lines[7].split(',')
            t_height[len(t_height) - 1] = 10000
            self.temp_alt = [self.site_alt + int(h) for h in t_height]
            data_idx = 9
            line = lines[data_idx].split(',')
            before_date = datetime.datetime(year=int('20' + str(line[0])), month=int(line[1]), day=int(line[2]),
                                            hour=int(line[3]), minute=int(line[4]),second=int(line[5]))
            count = 0
            for line in lines[data_idx+1:]:
                line = line.split(',')
                after_date = datetime.datetime(year=int('20' + str(line[0])), month=int(line[1]), day=int(line[2]),
                                                hour=int(line[3]), minute=int(line[4]), second=int(line[5]))
                before_diff = (before_date - self.aim_date).total_seconds()
                after_diff = (after_date - self.aim_date).total_seconds()
                if abs(after_diff) >= abs(before_diff):
                    aim_file = file
                    aim_line = data_idx + count
                    break
                before_date = after_date
                count += 1
            if aim_file != '' and aim_line != -1:
                print('Temp Find data closet to aim date:', aim_file, aim_line, " (UTC):", before_date)
                aimtemp = list(map(float, lines[aim_line].split(',')[7:]))
                self.temp = numpy.array(aimtemp) + self.tempdiff
                break