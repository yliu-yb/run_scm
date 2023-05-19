from WindSonic2D import WindSonic2D
from NearSurface import NearSurface
from MicrowaveRadiometer import MicrowaveRadiometer
from WindProfilerRadar import WindProfilerRadar
from ERA5_SOIL import ERA5_SOIL
import math
from common import interpolation
from common import interpolation_3

def make(aim_date, tempdiff):

    site_alt = 86
    print('aim_date(UTC): ', aim_date)

    z = [10, 20, 35, 52, 95]
    sz = [0.1, 0.2]

    windSonic2D_filefoder = '../data/winsonic_2d/'
    windSonice2D = WindSonic2D(windSonic2D_filefoder, aim_date, z, site_alt)

    nearSurface_filefolder = '../data/turbulence/'
    nearSurface = NearSurface(nearSurface_filefolder, aim_date, z, sz, site_alt, tempdiff)

    micro_filefloder = '../data/micro/'
    micro = MicrowaveRadiometer(micro_filefloder, aim_date, site_alt, tempdiff)

    windProfilerRadar_filefolder = '../data/windprofile/'
    windRadar = WindProfilerRadar(windProfilerRadar_filefolder, aim_date, site_alt)

    ear5_soil_file = '../data/era5/era5_single_level_201606.nc'
    ear5_soil = ERA5_SOIL(ear5_soil_file, aim_date)
    # get u,v
    wind_profile_u = [wind * math.sin(math.radians(direction + 180)) for wind, direction in zip(windRadar.vel, windRadar.wind_direction)]
    wind_profile_v = [wind * math.cos(math.radians(direction + 180)) for wind, direction in zip(windRadar.vel, windRadar.wind_direction)]

    # (3) 将位温和比湿插值到风速高度
    theta_alt_h, theta_h = interpolation(micro.theta, micro.temp_alt, windRadar.alt)
    qv_alt_h, qv_h = interpolation(micro.qv, micro.rh_alt, windRadar.alt)

    # get common heigt u,v data
    u_h = wind_profile_u[:windRadar.alt.index(theta_alt_h[-1])+1]
    v_h = wind_profile_v[:windRadar.alt.index(theta_alt_h[-1])+1]
    vel_alt_h = windRadar.alt[:windRadar.alt.index(theta_alt_h[-1])+1]

    #input_sounding
    ##地面高度，10米东西、南北风，2米温度、2米比湿、地面气压
    z_terrian = site_alt

    u_10 = windSonice2D.u[0]
    v_10 = windSonice2D.v[0]
    t_2 = interpolation_3(nearSurface.alt, nearSurface.temp, 2 + site_alt)
    q_2 = interpolation_3(nearSurface.alt, nearSurface.qv, 2 + site_alt)
    psfc = (1013.25 - site_alt / 9.) * 100
    print(psfc)
    psfc = ear5_soil.surfaceP
    print(psfc)
    ##高度，东西风，南北风，位温，比湿
    h_alt_statr_index = 0
    for i in range(len(vel_alt_h)):
        if vel_alt_h[i] > nearSurface.alt[-1]:
            h_alt_statr_index = i
            break
    z = [*windSonice2D.alt, *vel_alt_h[h_alt_statr_index:]]
    u = [*windSonice2D.u, *u_h[h_alt_statr_index:]]
    v = [*windSonice2D.v, *v_h[h_alt_statr_index:]]
    theta = [*nearSurface.theta, *theta_h[h_alt_statr_index:]]
    qv = [*nearSurface.qv, *qv_h[h_alt_statr_index:]]

    print('<<sounding>>')
    print('z_terrian:', z_terrian)
    print('u_10:', u_10)
    print('v_10:', v_10)
    print('t_2:', t_2)
    print('q_2:', q_2)
    print('psfc:', psfc)
    print('z:', z)
    print('u:', u)
    print('v:', v)
    print('theta:', theta)
    print('qv:', qv)

    #input_soil
    ##
    # SURFACE SKIN TEMPERATURE (K)
    TSK = ear5_soil.skinT
    # SOIL TEMPERATURE AT LOWER BOUNDARY (K)
    TMN = ear5_soil.soilT[len(ear5_soil.soilT)-1]
    # sz = [site_alt - h for h in ear5_soil.sz]
    sz = ear5_soil.sz
    # Soil temperature (K)
    SOILT = ear5_soil.soilT
    # Soil moisture (kgm-3)
    SOILM = ear5_soil.soilM

    print('<<soil>>')
    print('0.0:', z_terrian)
    print('TSK:', TSK)
    print('TMN', TMN)
    print('sz:', sz)
    print('SOILT:', SOILT)
    print('SOILM:', SOILM)

    ####输出input_sounding
    with open("../scm_input/input_sounding","w") as f:
        f.write(format(z_terrian, '.1f') + ' ' + format(u_10, '.1f') + ' ' + format(v_10, '.1f')
                + ' ' + format(t_2, '.1f') + ' ' + format(q_2, '.4f')+ ' ' + format(psfc, '.1f'))
        f.write('\n')
        for i in range(len(z)):
            f.write(format(z[i], '.1f') + ' ' + format(u[i], '.1f') + ' ' + format(v[i], '.1f')
                    + ' ' + format(theta[i], '.1f') + ' ' + format(qv[i], '.4f'))
            f.write('\n')

    ####输出input_soil
    with open("../scm_input/input_soil","w") as f:
        f.write(format(0, '.7f') + ' ' + format(TSK, '.7f') + ' ' + format(TMN, '.7f'))
        f.write('\n')
        for i in range(len(sz)):
            f.write(format(sz[i], '.7f') + ' ' + format(SOILT[i], '.7f') + ' ' + format(SOILM[i], '.7f'))
            f.write('\n')

