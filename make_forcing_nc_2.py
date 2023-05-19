import netCDF4
import numpy
from netCDF4 import Dataset
import time
import os
from wrf_force import wrf_force
import math

def convertPressure2At(pressure):
    coe1 = math.log10(pressure / 1013.25)
    coe2 = (10 ** coe1) / 5.2558797
    # return 0.3048 * (coe2 - 1) / (-6.8755856 * 0.000001)
    return  44330 * (1 - (pressure / 1013.25)**(1 / 5.255))

class ForcingNCFileMake():
    def split(self, word):
        return [char for char in word]
    def make(self, wrffile, cdl_path, start_datetime, end_datetime, output_path, tau_res, bkgrid_res):

        interp_height = []
        for i in range(0, 1050, 50):
            interp_height.append(i)
        for i in range(1100, 2000, 100):
            interp_height.append(i)
        for i in range(2150, 4000, 150):
            interp_height.append(i)
        for i in range(4250, 6000, 250):
            interp_height.append(i)
        for i in range(6300, 9000, 300):
            interp_height.append(i)
        for i in range(9500, 12000, 500):
            interp_height.append(i)
        for i in range(12000, 19100, 1000):
            interp_height.append(i)

        # interp_height = [15.749827595790762, 238.4417219179528, 464.8328171424742, 697.1426338107755, 934.6313317423841, 1177.298910937294, 1425.885211575987, 1681.1300738389289, 1943.0334977261202, 2212.3353234180363, 2489.775391095147, 3069.0702524049534, 3683.137602196961, 4336.416481553997, 5038.524812822206, 5798.340678167252, 6622.522639213389, 7523.647979028643, 8520.952542305298, 9635.891694277047, 10909.89648505034, 11623.842259206105, 12405.113489784848, 13264.067939313183, 14228.07969446858, 15336.36028481608, 16656.235166778657, 18731.486873003443, 19000.0]

        # alt = [i + 120 for i in interp_height]
        alt = [i + 180 for i in interp_height]

        # for i in range(100, 19100, 100):
        #     alt.append(i + 20)
        print(alt)
        print(len(alt))

        wrf_data = wrf_force(wrffile, start_datetime, end_datetime, alt, int(bkgrid_res))
        default_data = [0. for x in alt]

        tau = [int(tau_res) * 3600 for x in alt]
        self.z = [x - 160 for x in alt]
        self.dt = [time.strftime("%Y-%m-%d_%H:%M:%S", time.strptime(str(dt), "%Y-%m-%d %H:%M:%S")) for dt in wrf_data.dt]
        # print(self.dt)
        # exit()
        # 通过cdl生成force_ideal.nc
        os.system("ncgen -o " + output_path + " " + cdl_path)
        # 将再分析资料数据写入force_ideal.nc中
        force_nc = Dataset(output_path, 'r+')

        # check
        print("check")
        print(wrf_data.U_UPSTREAM_X.max(), wrf_data.U_UPSTREAM_X.min())
        print(wrf_data.U_UPSTREAM_Y.max(), wrf_data.U_UPSTREAM_Y.min())
        print(wrf_data.V_UPSTREAM_X.max(), wrf_data.V_UPSTREAM_X.min())
        print(wrf_data.V_UPSTREAM_Y.max(), wrf_data.V_UPSTREAM_Y.min())
        print(wrf_data.QV_UPSTREAM_X.max(), wrf_data.QV_UPSTREAM_X.min())
        print(wrf_data.QV_UPSTREAM_Y.max(), wrf_data.QV_UPSTREAM_Y.min())
        print(wrf_data.TH_UPSTREAM_X.max(), wrf_data.TH_UPSTREAM_X.min())
        print(wrf_data.TH_UPSTREAM_Y.max(), wrf_data.TH_UPSTREAM_Y.min())

        print(wrf_data.U_UPSTREAM_X_tend.max(), wrf_data.U_UPSTREAM_X_tend.min())
        print(wrf_data.U_UPSTREAM_Y_tend.max(), wrf_data.U_UPSTREAM_Y_tend.min())
        print(wrf_data.V_UPSTREAM_X_tend.max(), wrf_data.V_UPSTREAM_X_tend.min())
        print(wrf_data.V_UPSTREAM_Y_tend.max(), wrf_data.V_UPSTREAM_Y_tend.min())
        print(wrf_data.QV_UPSTREAM_X_tend.max(), wrf_data.QV_UPSTREAM_X_tend.min())
        print(wrf_data.QV_UPSTREAM_Y_tend.max(), wrf_data.QV_UPSTREAM_Y_tend.min())
        print(wrf_data.TH_UPSTREAM_X_tend.max(), wrf_data.TH_UPSTREAM_X_tend.min())
        print(wrf_data.TH_UPSTREAM_Y_tend.max(), wrf_data.TH_UPSTREAM_Y_tend.min())

        print(wrf_data.W_SUBS.max(), wrf_data.W_SUBS.min())
        print("end check")

        for itime in range(len(wrf_data.dt)):
            force_nc.variables['Times'][itime] = self.split(self.dt[itime])
            force_nc.variables['Z_FORCE'][itime] = self.z

            force_nc.variables['U_G'][itime] = default_data
            force_nc.variables['V_G'][itime] = default_data

            # force_nc.variables['U_G'][itime] = wrf_data.U_g[itime]
            # force_nc.variables['V_G'][itime] = wrf_data.V_g[itime]

            # force_nc.variables['U_G'][itime] = wrf_data.U[itime]
            # force_nc.variables['V_G'][itime] = wrf_data.V[itime]

            force_nc.variables['W_SUBS'][itime] = wrf_data.W_SUBS[itime]
            # force_nc.variables['W_SUBS'][itime] = default_data

            force_nc.variables['TH_UPSTREAM_X'][itime] = wrf_data.TH_UPSTREAM_X[itime]
            force_nc.variables['TH_UPSTREAM_Y'][itime] = wrf_data.TH_UPSTREAM_Y[itime]
            force_nc.variables['QV_UPSTREAM_X'][itime] = wrf_data.QV_UPSTREAM_X[itime]
            force_nc.variables['QV_UPSTREAM_Y'][itime] = wrf_data.QV_UPSTREAM_Y[itime]
            force_nc.variables['U_UPSTREAM_X'][itime] =  wrf_data.U_UPSTREAM_X[itime]
            force_nc.variables['U_UPSTREAM_Y'][itime] =  wrf_data.U_UPSTREAM_Y[itime]
            force_nc.variables['V_UPSTREAM_X'][itime] =  wrf_data.V_UPSTREAM_X[itime]
            force_nc.variables['V_UPSTREAM_Y'][itime] =  wrf_data.V_UPSTREAM_Y[itime]
            force_nc.variables['Z_FORCE_TEND'][itime] = default_data
            force_nc.variables['U_G_TEND'][itime] = default_data
            force_nc.variables['V_G_TEND'][itime] = default_data
            force_nc.variables['W_SUBS_TEND'][itime] = default_data
            force_nc.variables['TH_UPSTREAM_X_TEND'][itime] = wrf_data.TH_UPSTREAM_X_tend[itime]
            force_nc.variables['TH_UPSTREAM_Y_TEND'][itime] = wrf_data.TH_UPSTREAM_Y_tend[itime]
            force_nc.variables['QV_UPSTREAM_X_TEND'][itime] = wrf_data.QV_UPSTREAM_X_tend[itime]
            force_nc.variables['QV_UPSTREAM_Y_TEND'][itime] = wrf_data.QV_UPSTREAM_Y_tend[itime]
            force_nc.variables['U_UPSTREAM_X_TEND'][itime] =  wrf_data.U_UPSTREAM_X_tend[itime]
            force_nc.variables['U_UPSTREAM_Y_TEND'][itime] =  wrf_data.U_UPSTREAM_Y_tend[itime]
            force_nc.variables['V_UPSTREAM_X_TEND'][itime] =  wrf_data.V_UPSTREAM_X_tend[itime]
            force_nc.variables['V_UPSTREAM_Y_TEND'][itime] =  wrf_data.V_UPSTREAM_Y_tend[itime]
            # force_nc.variables['TH_UPSTREAM_X_TEND'][itime] = default_data
            # force_nc.variables['TH_UPSTREAM_Y_TEND'][itime] = default_data
            # force_nc.variables['QV_UPSTREAM_X_TEND'][itime] = default_data
            # force_nc.variables['QV_UPSTREAM_Y_TEND'][itime] = default_data
            # force_nc.variables['U_UPSTREAM_X_TEND'][itime] = default_data
            # force_nc.variables['U_UPSTREAM_Y_TEND'][itime] = default_data
            # force_nc.variables['V_UPSTREAM_X_TEND'][itime] = default_data
            # force_nc.variables['V_UPSTREAM_Y_TEND'][itime] = default_data

            force_nc.variables['TAU_X'][itime] = tau
            force_nc.variables['TAU_X_TEND'][itime] = default_data
            force_nc.variables['TAU_Y'][itime] = tau
            force_nc.variables['TAU_Y_TEND'][itime] = default_data
        force_nc.close()
        return True,'强迫场文件生成完成'+ output_path