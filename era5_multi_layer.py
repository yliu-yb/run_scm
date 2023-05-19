import numpy
from netCDF4 import Dataset, num2date
from datetime import datetime
import math

def convertTemp2Theta(Temp, pressure):
    return Temp * ((1000. / pressure)**0.286)

def convertPressure2At(pressure):
    return 44330 * (1 - (pressure / 1013.25) ** (1 / 5.255))

    # return Temp * math.pow(1000. / pressure, 0.286)

class era5_multy():
    def __init__(self, file, aim_dt):
        self.file = file
        self.aim_dt = datetime.strptime(aim_dt, "%Y/%m/%d %H:%M:%S")
        self.u = []
        self.v = []
        self.w = []
        self.th = []
        self.q = []
        self.h = []
        self.getData()

    def getData(self):
        nc = Dataset(self.file)
        times = nc["time"]
        time_convert = num2date(times[:], times.units, times.calendar)
        times =[datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S') for dt in time_convert]
        t_id = times.index(self.aim_dt)
        print("find aim date time in era5 multi levels")

        lats = numpy.array(nc["latitude"])
        lons = numpy.array(nc["longitude"])
        aim_lon = 117.14
        aim_lat = 32.74
        x_id = int(numpy.where(lons == min(lons, key=lambda x: abs(x - aim_lon)))[0])
        y_id = int(numpy.where(lats == min(lats, key=lambda x: abs(x - aim_lat)))[0])

        self.u = nc["u"][t_id,:,y_id,x_id]
        self.v = nc["v"][t_id,:,y_id,x_id]
        self.w = nc["w"][t_id,:,y_id,x_id]
        self.q = nc["q"][t_id,:,y_id,x_id]
        temp = numpy.array(nc["t"][t_id,:,y_id,x_id])
        pressure = numpy.array(nc["level"])
        self.th = convertTemp2Theta(temp, pressure)
        z = numpy.array(nc["z"][t_id,:,y_id,x_id])

        self.h = z / 9.81
        self.u = self.u[::-1]
        self.v = self.v[::-1]
        self.w = self.w[::-1]
        self.q = self.q[::-1]
        self.th = self.th[::-1]
        self.h = self.h[::-1]

if __name__ == "__main__":
    era5 = era5_multy("/home/yl/GraduationProject/case_data/case_201606/data/era5/era5_20160601-30.nc", "2016/06/01 12:00:00")
    pass