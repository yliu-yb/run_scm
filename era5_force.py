import numpy
from netCDF4 import Dataset, num2date
import datetime
import math
import draw

def convertTemp2Theta(Temp, pressure):
    return Temp * ((1000. / pressure)**0.286)

def convertPressure2At(pressure):
    return 44330 * (1 - (pressure / 1013.25) ** (1 / 5.255))

    # return Temp * math.pow(1000. / pressure, 0.286)

class era5_multy():
    def __init__(self, file, start_date, end_date):
        self.TH_adv = []
        self.QV_adv = []
        self.aim_start_date = start_date
        self.aim_end_date = end_date
        self.file = file
        self.start_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d_%H:%M:%S')
        self.end_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d_%H:%M:%S')
        self.GetData()
        self.draw()

    def GetData(self):
        nc = Dataset(self.file)
        times = nc["time"]
        time_convert = num2date(times[:], times.units, times.calendar)
        dt = [datetime.datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S') for dt in time_convert]
        startidx = dt.index(self.start_dt)
        endidx = dt.index(self.end_dt)

        lats = numpy.array(nc["latitude"])
        lons = numpy.array(nc["longitude"])
        aim_lon = 117.14
        aim_lat = 32.74
        center_node_x = int(numpy.where(lons == min(lons, key=lambda x: abs(x - aim_lon)))[0])
        center_node_y = int(numpy.where(lats == min(lats, key=lambda x: abs(x - aim_lat)))[0])
        print("aim_lon_lat:", aim_lon, aim_lat)
        print("nearest_lon_lat in era5:", min(lons, key=lambda x: abs(x - aim_lon)), min(lats, key=lambda x: abs(x - aim_lat)))

        north_node_x = center_node_x
        north_node_y = center_node_y - 1
        south_node_x = center_node_x
        south_node_y = center_node_y + 1

        east_node_x = center_node_x + 1
        east_node_y = center_node_y
        west_node_x = center_node_x - 1
        west_node_y = center_node_y
        distance = 25000.
        up_stream_mk = True
        def GetAdvectionTendency_x(var, vel, t_startidx, t_endidx, h_level):
            result = []
            for t in range(t_startidx, t_endidx):
                profile = []
                for z in range(0, h_level):
                    vel_center = vel[t, z, center_node_y, center_node_x]
                    var_center = var[t, z, center_node_y, center_node_x]
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
            return numpy.array(result)

        def GetAdvectionTendency_y(var, vel, t_startidx, t_endidx, h_level):
            result = []
            for t in range(t_startidx, t_endidx):
                profile = []
                for z in range(0, h_level):
                    vel_center = vel[t, z, center_node_y, center_node_x]
                    var_center = var[t, z, center_node_y, center_node_x]
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
            return numpy.array(result)

        omiga = 0.000072921
        f = 2 * omiga * math.sin(32.74 * 3.14 / 180.)
        coe_gf = 9.81 / f
        def GetGeoWind_U(var, t_startidx, t_endidx, h_level):
            result = []
            for t in range(t_startidx, t_endidx):
                profile = []
                for z in range(0, h_level):
                    var_south = var[t, z, south_node_y, south_node_x]
                    var_north = var[t, z, north_node_y, north_node_x]
                    ug = -coe_gf * (var_north - var_south) / (2 * distance)
                    profile.append(ug)
                result.append(profile)
            return numpy.array(result)

        def GetGeoWind_V(var, t_startidx, t_endidx, h_level):
            result = []
            for t in range(t_startidx, t_endidx):
                profile = []
                for z in range(0, h_level):
                    var_west = var[t, z, west_node_y, west_node_x]
                    var_east = var[t, z, east_node_y, east_node_x]
                    vg = coe_gf * (var_east - var_west) / (2 * distance)
                    profile.append(vg)
                result.append(profile)
            return numpy.array(result)

        U = numpy.array(nc["u"])
        V = numpy.array(nc["v"])
        W = numpy.array(nc["w"])

        QV = numpy.array(nc["q"])
        Temp = numpy.array(nc["t"])
        Z = numpy.array(nc["z"]) / 9.81
        P = numpy.array(nc["level"])

        TH = numpy.zeros((len(Temp), len(Temp[0]), len(Temp[0,0]), len(Temp[0,0,0])))
        for t in range(0, len(Temp)):
            for y in range(0, len(Temp[0,0])):
                for x in range(0, len(Temp[0,0,0])):
                    TH[t,:,y,x] = convertTemp2Theta(Temp[t,:,y,x], P)

        levels = len(Z[0,:,center_node_y,center_node_x])

        self.U_UPSTREAM_X = GetAdvectionTendency_x(U, U, startidx, endidx, levels)
        self.U_UPSTREAM_Y = GetAdvectionTendency_y(U, V, startidx, endidx, levels)

        self.V_UPSTREAM_X = GetAdvectionTendency_x(V, U, startidx, endidx, levels)
        self.V_UPSTREAM_Y = GetAdvectionTendency_y(V, V, startidx, endidx, levels)

        self.QV_UPSTREAM_X = GetAdvectionTendency_x(QV, U, startidx, endidx, levels)
        self.QV_UPSTREAM_Y = GetAdvectionTendency_y(QV, V, startidx, endidx, levels)

        self.TH_UPSTREAM_X = GetAdvectionTendency_x(TH, U, startidx, endidx, levels)
        self.TH_UPSTREAM_Y = GetAdvectionTendency_y(TH, V, startidx, endidx, levels)

        # get geowind from geopotential
        self.U_g = GetGeoWind_U(Z, startidx, endidx, levels)
        self.V_g = GetGeoWind_V(Z, startidx, endidx, levels)

        # print("levels", levels)

        self.height = Z[startidx:endidx,:,center_node_y,center_node_x]

        self.U_UPSTREAM_X_tend = self.U_UPSTREAM_X[:,::-1]
        self.U_UPSTREAM_Y_tend = self.U_UPSTREAM_Y[:,::-1]

        self.V_UPSTREAM_X_tend = self.V_UPSTREAM_X[:, ::-1]
        self.V_UPSTREAM_Y_tend = self.V_UPSTREAM_Y[:, ::-1]

        self.QV_UPSTREAM_X_tend = self.QV_UPSTREAM_X[:, ::-1]
        self.QV_UPSTREAM_Y_tend = self.QV_UPSTREAM_Y[:, ::-1]

        self.TH_UPSTREAM_X_tend = self.TH_UPSTREAM_X[:, ::-1]
        self.TH_UPSTREAM_Y_tend = self.TH_UPSTREAM_Y[:, ::-1]

        self.U_UPSTREAM_X = U[startidx:endidx, :, center_node_y, center_node_x]
        self.U_UPSTREAM_Y = U[startidx:endidx, :, center_node_y, center_node_x]

        self.V_UPSTREAM_X = V[startidx:endidx, :, center_node_y, center_node_x]
        self.V_UPSTREAM_Y = V[startidx:endidx, :, center_node_y, center_node_x]

        self.QV_UPSTREAM_X = QV[startidx:endidx, :, center_node_y, center_node_x]
        self.QV_UPSTREAM_Y = QV[startidx:endidx, :, center_node_y, center_node_x]

        self.TH_UPSTREAM_X = TH[startidx:endidx, :, center_node_y, center_node_x]
        self.TH_UPSTREAM_Y = TH[startidx:endidx, :, center_node_y, center_node_x]

        self.W_SUBS = W[startidx:endidx, :, center_node_y, center_node_x]

        self.U_UPSTREAM_X = self.U_UPSTREAM_X[:, ::-1]
        self.U_UPSTREAM_Y = self.U_UPSTREAM_Y[:, ::-1]

        self.V_UPSTREAM_X = self.V_UPSTREAM_X[:, ::-1]
        self.V_UPSTREAM_Y = self.V_UPSTREAM_Y[:, ::-1]

        self.QV_UPSTREAM_X = self.QV_UPSTREAM_X[:, ::-1]
        self.QV_UPSTREAM_Y = self.QV_UPSTREAM_Y[:, ::-1]

        self.TH_UPSTREAM_X = self.TH_UPSTREAM_X[:, ::-1]
        self.TH_UPSTREAM_Y = self.TH_UPSTREAM_Y[:, ::-1]

        # calculate advection
        # u*dT/dx + v*dT/dy
        self.TH_adv = self.CalculateAdv(startidx, endidx, levels, distance,
                                        U[:, :, y, x], V[:, :, y, x],
                                        TH[:, :, west_node_y, west_node_x],
                                        TH[:, :, east_node_y, east_node_x],
                                        TH[:, :, north_node_y, north_node_x],
                                        TH[:, :, south_node_y, south_node_x],
                                        )
        self.QV_adv = self.CalculateAdv(startidx, endidx, levels, distance,
                                        U[:, :, y, x], V[:, :, y, x],
                                        QV[:, :, west_node_y, west_node_x],
                                        QV[:, :, east_node_y, east_node_x],
                                        QV[:, :, north_node_y, north_node_x],
                                        QV[:, :, south_node_y, south_node_x],
                                        )
        print("self.TH_adv[0,:]")
        # print(self.TH_adv[0,:])
        # end calculate advection

        self.W_SUBS = self.W_SUBS[:, ::-1]

        self.U_g = self.U_g[:, ::-1]
        self.V_g = self.V_g[:, ::-1]

        self.TH_adv = self.TH_adv[:, ::-1]
        self.QV_adv = self.QV_adv[:, ::-1]

        self.height = self.height[:,::-1]

        h_end_id = 0
        top_height = 20000
        for i in range(0, len(self.height[0])):
            if self.height[0, i] > top_height:
                h_end_id = i + 1
                break

        self.U_UPSTREAM_X = self.U_UPSTREAM_X[:, 0:h_end_id]
        self.U_UPSTREAM_Y = self.U_UPSTREAM_Y[:, 0:h_end_id]

        self.V_UPSTREAM_X = self.V_UPSTREAM_X[:, 0:h_end_id]
        self.V_UPSTREAM_Y = self.V_UPSTREAM_Y[:, 0:h_end_id]

        self.QV_UPSTREAM_X = self.QV_UPSTREAM_X[:, 0:h_end_id]
        self.QV_UPSTREAM_Y = self.QV_UPSTREAM_Y[:, 0:h_end_id]

        self.TH_UPSTREAM_X = self.TH_UPSTREAM_X[:, 0:h_end_id]
        self.TH_UPSTREAM_Y = self.TH_UPSTREAM_Y[:, 0:h_end_id]

        self.U_UPSTREAM_X_tend = self.U_UPSTREAM_X_tend[:, 0:h_end_id]
        self.U_UPSTREAM_Y_tend = self.U_UPSTREAM_Y_tend[:, 0:h_end_id]

        self.V_UPSTREAM_X_tend = self.V_UPSTREAM_X_tend[:, 0:h_end_id]
        self.V_UPSTREAM_Y_tend = self.V_UPSTREAM_Y_tend[:, 0:h_end_id]

        self.QV_UPSTREAM_X_tend = self.QV_UPSTREAM_X_tend[:, 0:h_end_id]
        self.QV_UPSTREAM_Y_tend = self.QV_UPSTREAM_Y_tend[:, 0:h_end_id]

        self.TH_UPSTREAM_X_tend = self.TH_UPSTREAM_X_tend[:, 0:h_end_id]
        self.TH_UPSTREAM_Y_tend = self.TH_UPSTREAM_Y_tend[:, 0:h_end_id]

        self.W_SUBS = self.W_SUBS[:, 0:h_end_id]

        self.U_g = self.U_g[:, 0:h_end_id]
        self.V_g = self.V_g[:, 0:h_end_id]

        self.height = self.height[:, 0:h_end_id]

        self.TH_adv = self.TH_adv[:, 0:h_end_id]
        self.QV_adv = self.QV_adv[:, 0:h_end_id]

        print(self.height[0,-1])
        self.dt = dt[startidx:endidx]

    def draw(self):
        yp = self.height
        # for i in self.dt:
        #     yp.append(self.interpH)
        date = self.aim_start_date + "-" + self.aim_end_date
        save_path = "./advection/"

        # draw.draw_vertical_velocity(self.dt, yp, self.W_SUBS, "Date(UTC)", "AGH(km)", "(a) Vertical Velocity",
        #                             'Units:m/s', 'w_era5', save_path)
        #
        # draw.draw_adv(self.dt, yp, self.TH_adv * 3600, "Date(UTC)", "AGH(km)", "(b) TH Foring",
        #               'Units:K/h', 'TH_adv_ear5', save_path)
        #
        # draw.draw_adv(self.dt, yp, self.QV_adv * 3600 * 1000, "Date(UTC)", "AGH(km)", "(c) QV Foring",
        #               'Units:g/kg/h', 'QV_adv_era5', save_path)

        draw.draw_adv(self.dt, yp, self.W_SUBS, -self.TH_adv * 3600, -self.QV_adv * 3600 * 1000, save_path, 'ERA5')


        # draw.draw_force(self.dt, yp, self.U_UPSTREAM_X_tend, date, 'height(km)', 'upstream u x-advection',
        #                 'm s-2', 'era5_U_UPSTREAM_X', save_path)
        # draw.draw_force(self.dt, yp, self.U_UPSTREAM_Y_tend, date, 'height(km)', 'upstream u y-advection',
        #                 'm s-2', 'era5_U_UPSTREAM_Y', save_path)
        #
        # draw.draw_force(self.dt, yp, self.V_UPSTREAM_X_tend, date, 'height(km)', 'upstream v x-advection',
        #                 'm s-2', 'era5_V_UPSTREAM_X', save_path)
        # draw.draw_force(self.dt, yp, self.V_UPSTREAM_Y_tend, date, 'height(km)', 'upstream v y-advection',
        #                 'm s-2', 'era5_V_UPSTREAM_Y', save_path)
        #
        # draw.draw_force(self.dt, yp, self.QV_UPSTREAM_X_tend, date, 'height(km)', 'upstream qv x-advection',
        #                 'kg kg-1 s-1', 'era5_QV_UPSTREAM_X', save_path)
        # draw.draw_force(self.dt, yp, self.QV_UPSTREAM_Y_tend, date, 'height(km)', 'upstream qv y-advection',
        #                 'kg kg-1 s-1', 'era5_QV_UPSTREAM_Y', save_path)
        #
        # draw.draw_force(self.dt, yp, self.TH_UPSTREAM_X_tend, date, 'height(km)',
        #                 'upstream theta x-advection', 'K s-1', 'era5_TH_UPSTREAM_X', save_path)
        # draw.draw_force(self.dt, yp, self.TH_UPSTREAM_Y_tend, date, 'height(km)',
        #                 'upstream theta y-advection', 'K s-1', 'era5_TH_UPSTREAM_Y', save_path)
        # U_g = self.U_g
        # V_g = self.V_g
        #
        # draw.draw_force(self.dt, yp, U_g, date, 'height(km)',
        #                 'x-component geostrophic wind', 'm s-1', 'era5_U_g', save_path)
        # draw.draw_force(self.dt, yp, V_g, date, 'height(km)',
        #                 'y-component geostrophic wind', 'm s-1', 'era5_V_g', save_path)
        print("draw era5_advection succeed")
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
    start_date = "20160531 000000"
    end_date = "20160604 000000"
    era5 = era5_multy("../data/era5/era5_levels_20160530-0604.nc", start_date, end_date)
