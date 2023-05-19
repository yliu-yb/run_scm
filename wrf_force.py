import numpy
from netCDF4 import Dataset
from wrf import getvar, ll_to_xy, disable_xarray, ALL_TIMES, interplevel
import datetime
import numpy as np
import math
import draw
from numpy import ma
from datetime import timedelta


class wrf_force():
    def __init__(self, file, aim_start_date, aim_end_date, interp_height, bkgrid_res):

        self.dt = []
        self.z = []
        self.file = file
        self.aim_start_date = aim_start_date
        self.aim_end_date = aim_end_date
        self.interpH = interp_height
        self.interpP = []

        self.bkgrid_res = bkgrid_res

        self.U_UPSTREAM_X = []  # upstream u x-advection "m s-2"
        self.U_UPSTREAM_Y = []  # upstream u x-advection "m s-2"

        self.V_UPSTREAM_X = []  # upstream v y-advection "m s-2"
        self.V_UPSTREAM_Y = []  # upstream v y-advection "m s-2"

        self.QV_UPSTREAM_X = []
        self.QV_UPSTREAM_Y = []

        self.TH_UPSTREAM_X = []
        self.TH_UPSTREAM_Y = []

        self.U_g = []
        self.V_g = []

        self.TH_adv = []
        self.QV_adv = []

        self.get_force_data()
        self.draw()

    def get_force_data(self):
        ncfile = Dataset(self.file)

        # disable_xarray()

        # Get the geopotential height (m) and pressure (hPa).
        z = getvar(ncfile, "z", timeidx=ALL_TIMES)
        p = getvar(ncfile, "pressure", timeidx=ALL_TIMES)
        lats = getvar(ncfile, "lat", timeidx=ALL_TIMES)
        lons = getvar(ncfile, "lon", timeidx=ALL_TIMES)

        U = getvar(ncfile, 'U', timeidx=ALL_TIMES)
        V = getvar(ncfile, 'V', timeidx=ALL_TIMES)
        W = getvar(ncfile, 'W', timeidx=ALL_TIMES)

        T = getvar(ncfile, 'th', timeidx=ALL_TIMES)
        QVAPOR = getvar(ncfile, 'QVAPOR', timeidx=ALL_TIMES)
        Temp = getvar(ncfile, 'temp', timeidx=ALL_TIMES)
        Tv = getvar(ncfile, 'tv', timeidx=ALL_TIMES)

        PH = getvar(ncfile, 'PH', timeidx=ALL_TIMES)
        PHB = getvar(ncfile, 'PHB', timeidx=ALL_TIMES)

        GeoH = (PH + PHB) / 9.81

        times = ncfile.variables["Times"]
        dt = []
        for time in times:
            strDatatime = ''
            for b in time:
                strDatatime += bytes.decode(b)
            dt.append(datetime.datetime.strptime(strDatatime, '%Y-%m-%d_%H:%M:%S').replace(minute=0, second=0))

        x, y = ll_to_xy(ncfile, 32.74, 117.14)

        self.z = z[0, :, y, x]

        west_node_x = x - 1
        west_node_y = y
        east_node_x = x + 1
        east_node_y = y

        south_node_x = x
        south_node_y = y - 1
        north_node_x = x
        north_node_y = y + 1

        print("center:", lons[0, y, x], lats[0, y, x])
        print("west:", lons[0, west_node_y, west_node_x], lats[0, west_node_y, west_node_x])
        print("east:", lons[0, east_node_y, east_node_x], lats[0, east_node_y, east_node_x])
        print("south:", lons[0, south_node_y, south_node_x], lats[0, south_node_y, south_node_x])
        print("north:", lons[0, north_node_y, north_node_x], lats[0, north_node_y, north_node_x])

        # get advection data

        # interp to specified pressure level

        # time set
        aim_start_dt = datetime.datetime.strptime(self.aim_start_date, '%Y-%m-%d_%H:%M:%S')
        aim_end_dt = datetime.datetime.strptime(self.aim_end_date, '%Y-%m-%d_%H:%M:%S')
        endidx = dt.index(aim_end_dt)
        startidx = dt.index(aim_start_dt)

        for i in range(startidx + 1, endidx):
            sec_diff = (dt[i] - dt[startidx]).total_seconds()
            if sec_diff % (int(self.bkgrid_res) * 6) != 0:
                multi = sec_diff / (int(self.bkgrid_res) * 6)
                multi = int(multi) + 1
                dt[i] = dt[startidx] + timedelta(seconds= multi * (int(self.bkgrid_res) * 6) )
        # print(dt[startidx:])
        # exit()
        print("start_idx", startidx)
        # calculate advection tendency
        # h_level = len(z[0, :, 0, 0])
        h_level = np.array(self.interpH)

        levels = len(h_level)
        # distance = 3000.  # grid distance 3000m
        distance = self.bkgrid_res * 1000  # grid distance 3000m

        up_stream_mk = True

        def GetAdvectionTendency_x(var, vel, t_startidx, t_endidx, h_level):
            result = []
            for t in range(t_startidx, t_endidx):
                profile = []
                for z in range(0, h_level):
                    vel_center = vel[t, z, y, x]
                    var_center = var[t, z, y, x]
                    var_west = var[t, z, west_node_y, west_node_x]
                    var_east = var[t, z, east_node_y, east_node_x]
                    if vel_center >= 0 or up_stream_mk == False:
                        up_bound = (var_east + var_center) / 2.
                        down_bound = (var_center + var_west) / 2.
                    else:
                        up_bound = (var_west + var_center) / 2.
                        down_bound = (var_center + var_east) / 2.
                    gradient = (up_bound - down_bound) / distance
                    profile.append(gradient * vel_center)
                result.append(profile)
            return result

        def GetAdvectionTendency_y(var, vel, t_startidx, t_endidx, h_level):
            result = []
            for t in range(t_startidx, t_endidx):
                profile = []
                for z in range(0, h_level):
                    vel_center = vel[t, z, y, x]
                    var_center = var[t, z, y, x]
                    var_north = var[t, z, north_node_y, north_node_x]
                    var_south = var[t, z, south_node_y, south_node_x]
                    if vel_center >= 0 or up_stream_mk == False:
                        up_bound = (var_north + var_center) / 2.
                        down_bound = (var_center + var_south) / 2.
                    else:
                        up_bound = (var_south + var_center) / 2.
                        down_bound = (var_center + var_north) / 2.
                    gradient = (up_bound - down_bound) / distance
                    profile.append(gradient * vel_center)
                result.append(profile)
            return result

        # omiga = 7.2921 * 0.00001
        omiga = 0.000072921

        f = 2 * omiga * math.sin(32.74 * 3.14 / 180.)
        coe_gf = 9.81 / f
        f_recip = 1 / f
        # def GetGeoWind_U(var, t_startidx, t_endidx, h_level):
        #     result = []
        #     for t in range(t_startidx, t_endidx):
        #         profile = []
        #         for z in range(0, h_level):
        #             var_south = var[t, z, south_node_y, south_node_x]
        #             var_north = var[t, z, north_node_y, north_node_x]
        #             ug = -coe_gf * (var_north - var_south) / (2 * distance)
        #             profile.append(ug)
        #         result.append(profile)
        #     return result
        #
        # def GetGeoWind_V(var, t_startidx, t_endidx, h_level):
        #     result = []
        #     for t in range(t_startidx, t_endidx):
        #         profile = []
        #         for z in range(0, h_level):
        #             var_west = var[t, z, west_node_y, west_node_x]
        #             var_east = var[t, z, east_node_y, east_node_x]
        #             vg = coe_gf * (var_east - var_west) / (2 * distance)
        #             profile.append(vg)
        #         result.append(profile)
        #     return result

        Rd = 287

        def GetGeoWind_V(Tv, Pressure, t_startidx, t_endidx, h_level):
            result = []
            for t in range(t_startidx, t_endidx):
                profile = []
                for z in range(0, h_level):
                    var_west = Pressure[t, z, west_node_y, west_node_x] * 100
                    var_east = Pressure[t, z, east_node_y, east_node_x] * 100
                    vg = f_recip * (0.01 * Rd * Tv[t, z, y, x] / Pressure[t, z, y, x]) * (
                                (var_east - var_west) / (2 * distance))
                    profile.append(vg)

                result.append(profile)
            return result

        def GetGeoWind_U(Tv, Pressure, t_startidx, t_endidx, h_level):
            result = []
            for t in range(t_startidx, t_endidx):
                profile = []
                for z in range(0, h_level):
                    var_south = Pressure[t, z, south_node_y, south_node_x] * 100
                    var_north = Pressure[t, z, north_node_y, north_node_x] * 100
                    ug = -f_recip * (0.01 * Rd * Tv[t, z, y, x] / Pressure[t, z, y, x]) * (
                                (var_north - var_south) / (2 * distance))
                    profile.append(ug)
                result.append(profile)
            return result

        # interpolate to set presure levels
        p_level = np.array(interplevel(p, z, h_level))
        p_level = p_level[0, :, y, x]
        print(p_level)
        p_level[0] = 990

        geo_zero_height = 1500
        geo_zero_height_id = 0
        for i in range(0, len(h_level)):
            if h_level[i] > geo_zero_height:
                geo_zero_height_id = i - 1
                break

        U_interp = np.array(interplevel(U[:, :, :, 1:], z, h_level))
        V_interp = np.array(interplevel(V[:, :, 1:, :], z, h_level))
        W_interp = np.array(interplevel(W[:, 1:, :, :], z, h_level))

        TH_interp = np.array(interplevel(T[:, :, :, :], z, h_level))
        QV_interp = np.array(interplevel(QVAPOR[:, :, :, :], z, h_level))
        GeoH_interp = np.array(interplevel(GeoH[:, 1:, :, :], p, p_level))
        Pressure_interp = np.array(interplevel(p[:, :, :, :], z, h_level))
        Temp_interp = np.array(interplevel(Temp[:, :, :, :], z, h_level))
        Tv_interp = np.array(interplevel(Tv[:, :, :, :], z, h_level))

        # print(T)
        # print(QVAPOR)
        # calculate advection
        # u*dT/dx + v*dT/dy
        self.TH_adv = self.CalculateAdv(startidx, endidx, levels, distance,
                                        U_interp[:, :, y, x], V_interp[:, :, y, x],
                                        TH_interp[:, :, west_node_y, west_node_x],
                                        TH_interp[:, :, east_node_y, east_node_x],
                                        TH_interp[:, :, north_node_y, north_node_x],
                                        TH_interp[:, :, south_node_y, south_node_x],
                                        )
        self.QV_adv = self.CalculateAdv(startidx, endidx, levels, distance,
                                        U_interp[:, :, y, x], V_interp[:, :, y, x],
                                        QV_interp[:, :, west_node_y, west_node_x],
                                        QV_interp[:, :, east_node_y, east_node_x],
                                        QV_interp[:, :, north_node_y, north_node_x],
                                        QV_interp[:, :, south_node_y, south_node_x],
                                        )
        print("self.TH_adv[0,:]")
        # print(self.TH_adv[0,:])
        # end calculate advection

        self.W_SUBS = W_interp[startidx:endidx, :, y, x]
        # print(self.W_SUBS[0,:])
        # exit()
        self.U_UPSTREAM_X_tend = GetAdvectionTendency_x(U_interp, U_interp, startidx, endidx, levels)
        self.U_UPSTREAM_Y_tend = GetAdvectionTendency_y(U_interp, V_interp, startidx, endidx, levels)
        self.V_UPSTREAM_X_tend = GetAdvectionTendency_x(V_interp, U_interp, startidx, endidx, levels)
        self.V_UPSTREAM_Y_tend = GetAdvectionTendency_y(V_interp, V_interp, startidx, endidx, levels)
        self.QV_UPSTREAM_X_tend = GetAdvectionTendency_x(QV_interp, U_interp, startidx, endidx, levels)
        self.QV_UPSTREAM_Y_tend = GetAdvectionTendency_y(QV_interp, V_interp, startidx, endidx, levels)
        self.TH_UPSTREAM_X_tend = GetAdvectionTendency_x(TH_interp, U_interp, startidx, endidx, levels)
        self.TH_UPSTREAM_Y_tend = GetAdvectionTendency_y(TH_interp, V_interp, startidx, endidx, levels)

        self.U_UPSTREAM_X = U_interp[startidx:endidx, :, y, x]
        self.U_UPSTREAM_Y = U_interp[startidx:endidx, :, y, x]
        self.V_UPSTREAM_X = V_interp[startidx:endidx, :, y, x]
        self.V_UPSTREAM_Y = V_interp[startidx:endidx, :, y, x]
        self.QV_UPSTREAM_X = QV_interp[startidx:endidx, :, y, x]
        self.QV_UPSTREAM_Y = QV_interp[startidx:endidx, :, y, x]
        self.TH_UPSTREAM_X = TH_interp[startidx:endidx, :, y, x]
        self.TH_UPSTREAM_Y = TH_interp[startidx:endidx, :, y, x]

        self.U_UPSTREAM_X = numpy.array(self.U_UPSTREAM_X)
        self.U_UPSTREAM_Y = numpy.array(self.U_UPSTREAM_Y)
        self.V_UPSTREAM_X = numpy.array(self.V_UPSTREAM_X)
        self.V_UPSTREAM_Y = numpy.array(self.V_UPSTREAM_Y)
        self.QV_UPSTREAM_X = numpy.array(self.QV_UPSTREAM_X)
        self.QV_UPSTREAM_Y = numpy.array(self.QV_UPSTREAM_Y)
        self.TH_UPSTREAM_X = numpy.array(self.TH_UPSTREAM_X)
        self.TH_UPSTREAM_Y = numpy.array(self.TH_UPSTREAM_Y)

        self.U_UPSTREAM_X_tend = numpy.array(self.U_UPSTREAM_X_tend)
        self.U_UPSTREAM_Y_tend = numpy.array(self.U_UPSTREAM_Y_tend)
        self.V_UPSTREAM_X_tend = numpy.array(self.V_UPSTREAM_X_tend)
        self.V_UPSTREAM_Y_tend = numpy.array(self.V_UPSTREAM_Y_tend)
        self.QV_UPSTREAM_X_tend = numpy.array(self.QV_UPSTREAM_X_tend)
        self.QV_UPSTREAM_Y_tend = numpy.array(self.QV_UPSTREAM_Y_tend)
        self.TH_UPSTREAM_X_tend = numpy.array(self.TH_UPSTREAM_X_tend)
        self.TH_UPSTREAM_Y_tend = numpy.array(self.TH_UPSTREAM_Y_tend)
        self.W_SUBS = numpy.array(self.W_SUBS)

        # print("check")
        # print(self.U_UPSTREAM_X.max(), self.U_UPSTREAM_X.min())
        # print(self.U_UPSTREAM_Y.max(), self.U_UPSTREAM_Y.min())
        # print(self.V_UPSTREAM_X.max(), self.V_UPSTREAM_X.min())
        # print(self.V_UPSTREAM_Y.max(), self.V_UPSTREAM_Y.min())
        # print(self.QV_UPSTREAM_X.max(), self.QV_UPSTREAM_X.min())
        # print(self.QV_UPSTREAM_Y.max(), self.QV_UPSTREAM_Y.min())
        # print(self.TH_UPSTREAM_X.max(), self.TH_UPSTREAM_X.min())
        # print(self.TH_UPSTREAM_Y.max(), self.TH_UPSTREAM_Y.min())
        #
        # print(self.U_UPSTREAM_X_tend.max(), self.U_UPSTREAM_X_tend.min())
        # print(self.U_UPSTREAM_Y_tend.max(), self.U_UPSTREAM_Y_tend.min())
        # print(self.V_UPSTREAM_X_tend.max(), self.V_UPSTREAM_X_tend.min())
        # print(self.V_UPSTREAM_Y_tend.max(), self.V_UPSTREAM_Y_tend.min())
        # print(self.QV_UPSTREAM_X_tend.max(), self.QV_UPSTREAM_X_tend.min())
        # print(self.QV_UPSTREAM_Y_tend.max(), self.QV_UPSTREAM_Y_tend.min())
        # print(self.TH_UPSTREAM_X_tend.max(), self.TH_UPSTREAM_X_tend.min())
        # print(self.TH_UPSTREAM_Y_tend.max(), self.TH_UPSTREAM_Y_tend.min())
        #
        # print(self.W_SUBS.max(), self.W_SUBS.min)
        # print("end check")
        # print(GeoH_interp)
        # print('---')
        # get geowind from geopotential
        # self.U_g = GetGeoWind_U(GeoH_interp, startidx, endidx, levels)
        # self.V_g = GetGeoWind_V(GeoH_interp, startidx, endidx, levels)
        # get geowind from pressure gradient force

        self.U_g = GetGeoWind_U(Tv_interp, Pressure_interp, startidx, endidx, levels)
        self.V_g = GetGeoWind_V(Tv_interp, Pressure_interp, startidx, endidx, levels)
        self.U = U_interp[startidx:endidx, :, y, x]
        self.V = U_interp[startidx:endidx, :, y, x]

        # print(self.U_g)
        # for data in self.U_g:
        #     data[0:geo_zero_height_id] = [0] * geo_zero_height_id
        # for data in self.V_g:
        #     data[0:geo_zero_height_id] = [0] * geo_zero_height_id
        self.dt = dt[startidx:endidx]

        print("dt")
        print(self.dt)
        # exit()

    def draw(self):
        yp = []
        for i in self.dt:
            yp.append(self.interpH)
        date = self.aim_start_date + "-" + self.aim_end_date
        save_path = "./advection/"

        # draw.draw_vertical_velocity(self.dt, yp, self.W_SUBS, "Date(UTC)", "AGH(km)", "(a) Vertical Velocity",
        #               'Units:m/s', 'w', save_path)
        #
        # draw.draw_adv(self.dt, yp, self.TH_adv * 3600, "Date(UTC)", "AGH(km)", "(b) TH Foring",
        #               'Units:K/h', 'TH_adv', save_path)
        #
        # draw.draw_adv(self.dt, yp, self.QV_adv * 3600 * 1000, "Date(UTC)", "AGH(km)", "(c) QV Foring",
        #               'Units:g/kg/h', 'QV_adv', save_path)

        draw.draw_adv(self.dt, yp, self.W_SUBS, -self.TH_adv * 3600, -self.QV_adv * 3600 * 1000, save_path, 'WRF-3D',
                      self.bkgrid_res)

        # draw.draw_force(self.dt, yp, self.U_UPSTREAM_X_tend, date, 'height(km)', 'upstream u x-advection',
        #                 'm s-2', 'U_UPSTREAM_X', save_path)
        # draw.draw_force(self.dt, yp, self.U_UPSTREAM_Y_tend, date, 'height(km)', 'upstream u y-advection',
        #                 'm s-2', 'U_UPSTREAM_Y', save_path)
        #
        # draw.draw_force(self.dt, yp, self.V_UPSTREAM_X_tend, date, 'height(km)', 'upstream v x-advection',
        #                 'm s-2', 'V_UPSTREAM_X', save_path)
        # draw.draw_force(self.dt, yp, self.V_UPSTREAM_Y_tend, date, 'height(km)', 'upstream v y-advection',
        #                 'm s-2', 'V_UPSTREAM_Y', save_path)
        #
        # draw.draw_force(self.dt, yp, self.QV_UPSTREAM_X_tend, date, 'height(km)', 'upstream qv x-advection',
        #                 'kg kg-1 s-1', 'QV_UPSTREAM_X', save_path)
        # draw.draw_force(self.dt, yp, self.QV_UPSTREAM_Y_tend, date, 'height(km)', 'upstream qv y-advection',
        #                 'kg kg-1 s-1', 'QV_UPSTREAM_Y', save_path)
        #
        # draw.draw_force(self.dt, yp, self.TH_UPSTREAM_X_tend, date, 'height(km)',
        #                 'upstream theta x-advection', 'K s-1', 'TH_UPSTREAM_X', save_path)
        # draw.draw_force(self.dt, yp, self.TH_UPSTREAM_Y_tend, date, 'height(km)',
        #                 'upstream theta y-advection', 'K s-1', 'TH_UPSTREAM_Y', save_path)
        # U_g = np.array(self.U_g)
        # V_g = np.array(self.V_g)
        # # U_g = ma.masked_where(U_g == 0, U_g)
        # # V_g = ma.masked_where(V_g == 0, V_g)
        #
        # draw.draw_force(self.dt, yp, U_g, date, 'height(km)',
        #                 'x-component geostrophic wind', 'm s-1', 'U_g', save_path)
        # draw.draw_force(self.dt, yp, V_g, date, 'height(km)',
        #                 'y-component geostrophic wind', 'm s-1', 'V_g', save_path)
        print("draw advction succeed")
        # exit()

    def CalculateAdv(self, t_start, t_end, h_level, distance, u, v, val_west, val_east, val_north, val_south):
        result = []
        for i in range(t_start, t_end):
            profile = []
            for j in range(0, h_level):
                v1 = v2 = 0
                e_w_diff = (val_east[i, j] - val_west[i, j]) / float(distance)
                n_s_diff = (val_north[i, j] - val_south[i, j]) / float(distance)
                if u[i, j] > 0:
                    v1 = e_w_diff * u[i, j]
                else:
                    v1 = -e_w_diff * u[i, j]
                if v[i, j] > 0:
                    v2 = n_s_diff * v[i, j]
                else:
                    v2 = -n_s_diff * v[i, j]
                profile.append(-v1 - v2)
            result.append(profile)
        return numpy.array(result)


if __name__ == "__main__":
    print("hello")

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

    alt = [i + 120 for i in interp_height]

    wrf_3d_file = ""
    force_from_wrf = wrf_force(wrf_3d_file, "2016-05-31_02:00:00", "2016-06-04_00:00:00", alt)
