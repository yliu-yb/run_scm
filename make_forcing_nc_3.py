import netCDF4
import numpy
from netCDF4 import Dataset
import time
import os
from wrf_force import wrf_force
import math
from era5_force import era5_multy

def convertPressure2At(pressure):
    coe1 = math.log10(pressure / 1013.25)
    coe2 = (10 ** coe1) / 5.2558797
    # return 0.3048 * (coe2 - 1) / (-6.8755856 * 0.000001)
    return  44330 * (1 - (pressure / 1013.25)**(1 / 5.255))

class ForcingNCFileMake():
    def split(self, word):
        return [char for char in word]
    def make(self, era5_file, cdl_path, start_datetime, end_datetime, output_path):

        # interp_height = []
        # for i in range(0, 1050, 50):
        #     interp_height.append(i)
        # for i in range(1100, 2000, 100):
        #     interp_height.append(i)
        # for i in range(2150, 4000, 150):
        #     interp_height.append(i)
        # for i in range(4250, 6000, 250):
        #     interp_height.append(i)
        # for i in range(6300, 9000, 300):
        #     interp_height.append(i)
        # for i in range(9500, 12000, 500):
        #     interp_height.append(i)
        # for i in range(12000, 19100, 1000):
        #     interp_height.append(i)
        #
        # alt = [i + 120 for i in interp_height]
        # # for i in range(100, 19100, 100):
        # #     alt.append(i + 20)
        # print(alt)
        # print(len(alt))

        era5_data = era5_multy(era5_file, start_datetime, end_datetime)
        levels = len(era5_data.height[0])
        print(levels)
        default_data = [0.] * levels
        tau = [3600*3] * levels
        self.z = [x - 30 for x in era5_data.height[0]]
        print(self.z)
        self.dt = [time.strftime("%Y-%m-%d_%H:%M:%S", time.strptime(str(dt), "%Y-%m-%d %H:%M:%S")) for dt in era5_data.dt]
        # print(self.dt)
        # exit()
        # 通过cdl生成force_ideal.nc
        os.system("ncgen -o " + output_path + " " + cdl_path)
        # 将再分析资料数据写入force_ideal.nc中
        force_nc = Dataset(output_path, 'r+')

        for itime in range(len(era5_data.dt)):
            force_nc.variables['Times'][itime] = self.split(self.dt[itime])
            force_nc.variables['Z_FORCE'][itime] = self.z

            force_nc.variables['U_G'][itime] = default_data
            force_nc.variables['V_G'][itime] = default_data

            # force_nc.variables['U_G'][itime] = era5_data.U_g[itime]
            # force_nc.variables['V_G'][itime] = era5_data.V_g[itime]

            # force_nc.variables['U_G'][itime] = era5_data.U[itime]
            # force_nc.variables['V_G'][itime] = era5_data.V[itime]

            # force_nc.variables['W_SUBS'][itime] = default_data
            force_nc.variables['W_SUBS'][itime] = era5_data.W_SUBS[itime]

            force_nc.variables['TH_UPSTREAM_X'][itime] = era5_data.TH_UPSTREAM_X[itime]
            force_nc.variables['TH_UPSTREAM_Y'][itime] = era5_data.TH_UPSTREAM_Y[itime]
            force_nc.variables['QV_UPSTREAM_X'][itime] = era5_data.QV_UPSTREAM_X[itime]
            force_nc.variables['QV_UPSTREAM_Y'][itime] = era5_data.QV_UPSTREAM_Y[itime]
            force_nc.variables['U_UPSTREAM_X'][itime] = era5_data.U_UPSTREAM_X[itime]
            force_nc.variables['U_UPSTREAM_Y'][itime] = era5_data.U_UPSTREAM_Y[itime]
            force_nc.variables['V_UPSTREAM_X'][itime] = era5_data.V_UPSTREAM_X[itime]
            force_nc.variables['V_UPSTREAM_Y'][itime] = era5_data.V_UPSTREAM_Y[itime]

            force_nc.variables['Z_FORCE_TEND'][itime] = default_data
            force_nc.variables['U_G_TEND'][itime] = default_data
            force_nc.variables['V_G_TEND'][itime] = default_data
            force_nc.variables['W_SUBS_TEND'][itime] = default_data

            force_nc.variables['TH_UPSTREAM_X_TEND'][itime] = era5_data.TH_UPSTREAM_X_tend[itime]
            force_nc.variables['TH_UPSTREAM_Y_TEND'][itime] = era5_data.TH_UPSTREAM_Y_tend[itime]
            force_nc.variables['QV_UPSTREAM_X_TEND'][itime] = era5_data.QV_UPSTREAM_X_tend[itime]
            force_nc.variables['QV_UPSTREAM_Y_TEND'][itime] = era5_data.QV_UPSTREAM_Y_tend[itime]
            force_nc.variables['U_UPSTREAM_X_TEND'][itime] = era5_data.U_UPSTREAM_X_tend[itime]
            force_nc.variables['U_UPSTREAM_Y_TEND'][itime] = era5_data.U_UPSTREAM_Y_tend[itime]
            force_nc.variables['V_UPSTREAM_X_TEND'][itime] = era5_data.V_UPSTREAM_X_tend[itime]
            force_nc.variables['V_UPSTREAM_Y_TEND'][itime] = era5_data.V_UPSTREAM_Y_tend[itime]

            force_nc.variables['TAU_X'][itime] = tau
            force_nc.variables['TAU_X_TEND'][itime] = default_data
            force_nc.variables['TAU_Y'][itime] = tau
            force_nc.variables['TAU_Y_TEND'][itime] = default_data
        force_nc.close()
        return True,'强迫场文件生成完成'+ output_path