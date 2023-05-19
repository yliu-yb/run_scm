import netCDF4
import numpy
from netCDF4 import Dataset
import time
import os
from wrf_force import wrf_force
import math

def convertPressure2At(pressure):
    return  44330 * (1 - (pressure / 1013.25)**(1 / 5.255))

class ForcingNCFileMake():
    def split(self, word):
        return [char for char in word]
    def make(self, reanalyze_nc_data_file, wrffile, cdl_path, start_datetime, end_datetime, timeresolution, output_path):
        print(reanalyze_nc_data_file)
        reanalyze_data = Dataset(reanalyze_nc_data_file)
        # 再分析资料日期时间，时间戳
        reanalyze_time = reanalyze_data.variables['time']
        reanalyze_datetime = netCDF4.num2date(reanalyze_time[:], reanalyze_time.units, reanalyze_time.calendar)
        reanalyze_timestamp = [time.mktime(time.strptime(str(x), "%Y-%m-%d %H:%M:%S")) for x in reanalyze_datetime]
        reanalyze_datetime_wrf_format = [time.strftime("%Y-%m-%d_%H:%M:%S", time.strptime(str(x), "%Y-%m-%d %H:%M:%S")) for x in reanalyze_datetime]
        # 开始日期时间和结束日期时间转时间戳
        start_timestamp = time.mktime(time.strptime(start_datetime, "%Y-%m-%d_%H:%M:%S"))
        end_timestamp = time.mktime(time.strptime(end_datetime, "%Y-%m-%d_%H:%M:%S"))
        #检查 再分析资料日期时间是否满足用户设置
        iter_num = int((end_timestamp - start_timestamp) / (float(timeresolution) * 3600))
        reanalyze_missing_datatime = []
        for i in range(iter_num):
            if start_timestamp + i * 3600 not in reanalyze_timestamp:
                reanalyze_missing_datatime.append(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(start_timestamp + i * 3600)))
        if len(reanalyze_missing_datatime) > 0:
            return False, '再分析资料缺失以下日期'+str(reanalyze_missing_datatime)
        #获得再分析资料数据
        p_start_idx = 8
        p_end_idx = -5
        for var in reanalyze_data.variables:
            if var == 'level':
                pressure = reanalyze_data.variables[var][p_start_idx:]
                alt = [convertPressure2At(x) for x in pressure]
                pp = [int(x) for x in pressure]
            if var == 'u':
                u = reanalyze_data.variables[var][:,p_start_idx:,0,0]
            if var == 'v':
                v = reanalyze_data.variables[var][:,p_start_idx:,0,0]
            if var == 'w':
                w = reanalyze_data.variables[var][:,p_start_idx:,0,0]
            if var == 'q':
                qvapor = reanalyze_data.variables[var][:,p_start_idx:,0,0]
            if var == 'clwc':
                qcloud = reanalyze_data.variables[var][:,p_start_idx:,0,0]
            if var == 'crwc':
                qrain = reanalyze_data.variables[var][:,p_start_idx:,0,0]
            if var == 't':
                temperature = reanalyze_data.variables[var][:,p_start_idx:,0,0]
                xishu = (1000/numpy.array(pressure))**0.286
                theta = [(numpy.array(x) * xishu).tolist() for x in temperature]
        alt.reverse()
        # alt[0] = alt[0] - 20
        print(alt)
        # exit()
        print(pp)
        # exit()
        # get wrf force
        wrf_data = wrf_force(wrffile, "2016-06-01_00:00:00", "2016-06-05_00:00:00", alt, pp)

        print(len(reanalyze_datetime_wrf_format), len(wrf_data.dt))
        # alt = [x - alt[0] for x in alt]
        default_data = [0. for x in alt]
        tau = [1 for x in alt]
        self.datetime = reanalyze_datetime_wrf_format
        self.z = alt
        # self.z[0] = self.z[0] - 20
        print("z", self.z)
        self.u = []
        self.v = []
        self.w = []
        self.qvapor = []
        self.qcloud = []
        self.qrain = []
        self.theta = []

        # 通过cdl生成force_ideal.nc
        os.system("ncgen -o " + output_path + " " + cdl_path)
        # 将再分析资料数据写入force_ideal.nc中
        force_nc = Dataset(output_path, 'r+')

        for itime in range(len(wrf_data.dt)):
            self.u.append(u[itime][::-1])
            self.v.append(v[itime][::-1])
            self.w.append(w[itime][::-1])
            self.qvapor.append(qvapor[itime][::-1])
            self.qrain.append(qrain[itime][::-1])
            self.qcloud.append(qcloud[itime][::-1])
            self.theta.append(theta[itime][::-1])

            force_nc.variables['Times'][itime] = self.split(reanalyze_datetime_wrf_format[itime])

            force_nc.variables['Z_FORCE'][itime] = self.z
            # force_nc.variables['U'][itime] = self.u[itime]
            # force_nc.variables['V'][itime] = self.v[itime]
            # force_nc.variables['W'][itime] = self.w[itime]
            # force_nc.variables['QVAPOR'][itime] = self.qvapor[itime]
            # force_nc.variables['QCLOUD'][itime] = self.qcloud[itime]
            # force_nc.variables['QRAIN'][itime] = self.qrain[itime]
            # force_nc.variables['T'][itime] = self.theta[itime]
            # print(wrf_data.TH_UPSTREAM_X[itime])
            force_nc.variables['U_G'][itime] = wrf_data.U_g[itime]
            force_nc.variables['V_G'][itime] = wrf_data.V_g[itime]
            force_nc.variables['W_SUBS'][itime] = default_data
            force_nc.variables['TH_UPSTREAM_X'][itime] = wrf_data.TH_UPSTREAM_X[itime]
            force_nc.variables['TH_UPSTREAM_Y'][itime] = wrf_data.TH_UPSTREAM_Y[itime]
            force_nc.variables['QV_UPSTREAM_X'][itime] = wrf_data.QV_UPSTREAM_X[itime]
            force_nc.variables['QV_UPSTREAM_Y'][itime] = wrf_data.QV_UPSTREAM_Y[itime]
            force_nc.variables['U_UPSTREAM_X'][itime] = wrf_data.U_UPSTREAM_X[itime]
            force_nc.variables['U_UPSTREAM_Y'][itime] = wrf_data.U_UPSTREAM_Y[itime]
            force_nc.variables['V_UPSTREAM_X'][itime] = wrf_data.V_UPSTREAM_X[itime]
            force_nc.variables['V_UPSTREAM_Y'][itime] = wrf_data.V_UPSTREAM_Y[itime]
            force_nc.variables['Z_FORCE_TEND'][itime] = default_data
            force_nc.variables['U_G_TEND'][itime] = default_data
            force_nc.variables['V_G_TEND'][itime] = default_data
            force_nc.variables['W_SUBS_TEND'][itime] = default_data
            force_nc.variables['TH_UPSTREAM_X_TEND'][itime] = default_data
            force_nc.variables['TH_UPSTREAM_Y_TEND'][itime] = default_data
            force_nc.variables['QV_UPSTREAM_X_TEND'][itime] = default_data
            force_nc.variables['QV_UPSTREAM_Y_TEND'][itime] = default_data
            force_nc.variables['U_UPSTREAM_X_TEND'][itime] = default_data
            force_nc.variables['U_UPSTREAM_Y_TEND'][itime] = default_data
            force_nc.variables['V_UPSTREAM_X_TEND'][itime] = default_data
            force_nc.variables['V_UPSTREAM_Y_TEND'][itime] = default_data
            force_nc.variables['TAU_X'][itime] = tau
            force_nc.variables['TAU_X_TEND'][itime] = default_data
            force_nc.variables['TAU_Y'][itime] = tau
            force_nc.variables['TAU_Y_TEND'][itime] = default_data
        force_nc.close()
        return True,'强迫场文件生成完成'+ output_path

            # force_nc.variables['Z_FORCE'][itime] = self.z[0:z_top_idx]
            # force_nc.variables['U'][itime] = self.u[itime][0:z_top_idx]
            # force_nc.variables['V'][itime] = self.v[itime][0:z_top_idx]
            # force_nc.variables['W'][itime] = self.w[itime][0:z_top_idx]
            # force_nc.variables['QVAPOR'][itime] = self.qvapor[itime][0:z_top_idx]
            # force_nc.variables['QCLOUD'][itime] =self.qcloud[itime][0:z_top_idx]
            # force_nc.variables['QRAIN'][itime] = self.qrain[itime][0:z_top_idx]
            # force_nc.variables['T'][itime] = self.theta[itime][0:z_top_idx]
            #
            # force_nc.variables['U_G'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['V_G'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['W_SUBS'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['TH_UPSTREAM_X'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['TH_UPSTREAM_Y'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['QV_UPSTREAM_X'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['QV_UPSTREAM_Y'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['U_UPSTREAM_X'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['U_UPSTREAM_Y'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['V_UPSTREAM_X'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['V_UPSTREAM_Y'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['Z_FORCE_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['U_G_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['V_G_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['W_SUBS_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['TH_UPSTREAM_X_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['TH_UPSTREAM_Y_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['QV_UPSTREAM_X_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['QV_UPSTREAM_Y_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['U_UPSTREAM_X_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['U_UPSTREAM_Y_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['V_UPSTREAM_X_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['V_UPSTREAM_Y_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['TAU_X'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['TAU_X_TEND'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['TAU_Y'][itime] = default_data[0:z_top_idx]
            # force_nc.variables['TAU_Y_TEND'][itime] = default_data[0:z_top_idx]