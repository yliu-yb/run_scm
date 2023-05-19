import datetime
import os
import netCDF4
import numpy

class ERA5_SOIL():
    def __init__(self, filefolder, aim_date):
        self.filefolder = filefolder
        self.aim_date = datetime.datetime.strptime(aim_date, '%Y/%m/%d %H:%M:%S')
        self.files = []
        self.getfiles()
        self.soilT = []
        self.soilM = []
        self.sz = [h / 100. for h in [7, 28, 100, 289]]
        self.skinT = 0
        self.surfaceP = 0
        self.getDataInFixedDate()
        pass

    def getfiles(self):
        for path, currentDirectory, files in os.walk(self.filefolder):
            for file in files:
                self.files.append(os.path.join(path, file))
        self.files = sorted(self.files)
        self.files = [self.filefolder]

    def getDataInFixedDate(self):
        find_file = ''
        find_line = -1

        for file in self.files:
            df = netCDF4.Dataset(file)
            time = df.variables['time']
            dt = netCDF4.num2date(time[:], time.units, time.calendar)
            dt = [datetime.datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S") for x in dt]
            count = 0

            lats = numpy.array(df["latitude"])
            lons = numpy.array(df["longitude"])
            aim_lon = 117.14
            aim_lat = 32.74
            x_id = int(numpy.where(lons == min(lons, key=lambda x: abs(x - aim_lon)))[0])
            y_id = int(numpy.where(lats == min(lats, key=lambda x: abs(x - aim_lat)))[0])

            for cell in dt:
                if cell == self.aim_date:
                    find_file = file
                    find_line = count
                    break
                count += 1
            if find_file != '' and find_line != -1:
                df = netCDF4.Dataset(find_file)
                for i in range(1,5):
                    var = 'stl' + str(i)
                    self.soilT.append(df.variables[var][find_line,y_id,x_id])
                    var = 'swvl' + str(i)
                    self.soilM.append(df.variables[var][find_line,y_id,x_id])
                self.skinT = df.variables['skt'][find_line,y_id,x_id]
                self.surfaceP = df.variables['sp'][find_line,y_id,x_id]
                print('ERA5 SOIL Find data closet to aim date:' + find_file + " (UTC):"+ str(dt[find_line]))
                break
# a = ERA5_SOIL('../data/era5_soil', '2016/06/01 0:0:0')


