import numpy
from numpy import ma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from matplotlib import ticker
from datetime import timedelta
import netCDF4 as nc
import wrf
from wrf import getvar
import os

class process_wrfout:
    def __init__(self, filepath, date, physicID, folder = ""):
        self.filepath = filepath
        self.date = date
        self.filefolder = folder
        self.physicID = physicID
        self.saveFolder = "../physicID-" + str(physicID) + "_fig"
        # os.system("rm -rf " + self.saveFolder)
        os.system("mkdir "+ self.saveFolder)

    def single_file(self):
        self.df = nc.Dataset(self.filepath)
        z = getvar(self.df, 'z')
        self.vars = ['CLDFRA', 'QCLOUD', 'QGRAUP', 'QHAIL', 'QICE', 'QRAIN', 'QSNOW', 'QVAPOR']

        PH = self.df.variables['PH']
        PHB = self.df.variables['PHB']
        times = self.df.variables['Times']
        self.datetime = []
        for time in times:
            strDatatime = ''
            for b in time:
                strDatatime += bytes.decode(b)
            self.datetime.append(datetime.datetime.strptime(strDatatime, '%Y-%m-%d_%H:%M:%S'))
        self.height = [h * 0.001 for h in z[:,0,0]]
        # pos_ew = 0
        # pos_ns = 0
        # for i in range(len(PHB[0][:]) - 1):
        #     self.height.append((PHB[0][i][pos_ns][pos_ew] + PH[0][i][pos_ns][pos_ew]) / 9.81 / 1000.)

        for var in self.vars:
            xlabel = 'Time(UTC)'
            ylabel = 'Height(km)'
            title = getattr(self.df.variables[var], 'description')
            barlabel = getattr(self.df.variables[var], 'units')
            self.draw_wrfout(var, self.datetime, self.height,
                        self.df.variables[var][:, :, 0, 0], xlabel, ylabel, title, barlabel)

    def multi_files(self):
        self.files = []
        for root, dirs, files in os.walk(self.filefolder):
            for file in files:
                self.files.append(os.path.join(root, file))
        print(self.files)
        self.files = sorted(self.files)
        for file in self.files:
            self.datetime = []
            print(file)
            df = nc.Dataset(file)
            times = df.variables['Times']
            for time in times:
                strDatatime = ''
                for b in time:
                    strDatatime += bytes.decode(b)
                self.datetime.append(datetime.datetime.strptime(strDatatime, '%Y-%m-%d_%H:%M:%S'))
            print(len(self.datetime))
            print(self.datetime)
            exit()
            # print(self.datetime[60 * 12])
    def draw_wrfout(self, variable, x, y, data, xlabel, ylabel, title, barlabel):
        data = list(map(list, zip(*data)))
        fig = plt.figure(figsize=(12, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=12)

        cs = ax1.contourf(x, y, data, cmap='jet')
        cbar = fig.colorbar(cs, ax=ax1, pad=0.01, label=barlabel)
        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        # fig.autofmt_xdate()
        fig.set_tight_layout(True)

        plt.savefig(self.saveFolder + '/' + variable + "_" + str(self.date) + '.png', dpi=300, bbox_inches='tight')
if __name__ == "__main__":
    # wrf = process_wrfout("../wrf_out/wrfout_20161010-20161011.nc", "20161010-20161011")
    # wrf.single_file()
    # wrf = process_wrfout("", "test", 0, "../wrf_out")
    # wrf.multi_files()
    pass
