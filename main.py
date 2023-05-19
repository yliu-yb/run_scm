import sys
import scm_input_make_2
import make_forcing_nc_2
import make_forcing_nc_3

import make_namelist
import os
import process_wrfout

para1 = sys.argv[1]
para2 = sys.argv[2]
para3 = sys.argv[3]
para4 = sys.argv[4]
para5 = sys.argv[5]
para6 = sys.argv[6]

start_year = para1[:4]
start_month = para1[4:6]
start_day = para1[6:8]
start_hour = para1[8:10]

end_year = para2[:4]
end_month = para2[4:6]
end_day = para2[6:8]
end_hour = para2[8:10]

run_days = para3
run_hours = para3
physicID = para4
temp_diff = str(para5)

# era5_multi_level_file = "../data/era5/era5_20160601-30.nc"
# ear5_single_level_file = "../data/era5/era5_single_level_201606.nc"
# wrf_3d_file = "/home/yl/wrf/wrfv4.4/WRF/test/data_save/case_force_make/wrfout_d03_2016-06-01_00:00:00"
# wrf_3d_file = "../../Draw/data/wrfout_d03_2016-05-31_00:00:00"
# wrf_3d_file = "../data/wrf/wrfout_d03_2016-06-01_00:00:00"

wrf_3d_file = "../../Draw/data/wrfout_20160531-0604_force_change.nc"
era5_multi_level_file = "../data/era5/era5_levels_20160530-0604.nc"
era5_single_level_file = "../data/era5/era5_single_20160530-0604.nc"

# set namelist config items
aim_date = str(start_year) + "/" + str(start_month) + "/" + str(start_day).zfill(2) + " " + str(start_hour) +":0:0"
start_date = str(start_year) + "-" + str(start_month) + "-" + str(start_day).zfill(2) + "_" + str(start_hour).zfill(2) +":00:00"
end_date = str(end_year) + "-" + str(end_month) + "-" + str(end_day).zfill(2) + "_" + str(end_hour).zfill(2) +":00:00"

# set scm exe folder
# scm_root = "/home/yl/wrf/wrf_scm/WRF/test/"
scm_root = "/home/yl/wrf/wrf_scm/WRF/"

# case folder
scm_folder = "case_physicID-" + str(physicID) + "_tempdiff_" + temp_diff + "_"+str(start_year)+str(start_month)+str(start_day).zfill(2) + "_" + str(start_hour) + "0000-"+str(end_year)+str(end_month)+str(end_day).zfill(2) + "_" + str(end_hour)

# make scm input data
scm_input_make_2.make(aim_date, float(temp_diff), era5_single_level_file, era5_multi_level_file)

# force_source_type = 'ERA5'
force_source_type = 'WRF'

if force_source_type == "ERA5":
    # make scm force data
    force = make_forcing_nc_3.ForcingNCFileMake()
    force.make(era5_multi_level_file,
               "forcing_file_2.cdl",
               start_date,
               end_date,
               "../scm_input/force_ideal.nc")
else:
    force = make_forcing_nc_2.ForcingNCFileMake()
    force.make(wrf_3d_file,
               "forcing_file_2.cdl",
               start_date,
               end_date,
               "../scm_input/force_ideal.nc")
# make scm namelist
make_namelist.make(run_hours, start_year, start_month, start_day, start_hour, end_year, end_month, end_day, end_hour, physicID)
print("namelist make succeed")
# exit()
# prepare for scm run
case_path = scm_root + scm_folder
# os.system("rm -rf " + case_path)
os.system("rm -rf " + case_path)
os.system("cp -a " + scm_root + "run " + case_path)
os.system("rm -rf " + case_path +"/wrfout*")
os.system("rm -rf " + case_path + "/wrfout*")
os.system("rm -rf " + case_path + "/force_ideal.nc")
os.system("rm -rf " + case_path + "/input_soil")
os.system("rm -rf " + case_path + "/input_sounding")
os.system("rm -rf " + case_path + "/namelist.input")
os.system("cp -a ../scm_input/* " + case_path)

# make scm run bash
file = open("scm_run.sh", "w")
content = """
cd %s
ulimit -s unlimited
./run_me_first.csh
./ideal.exe
gdb ./wrf.exe
"""
content = content % case_path
file.writelines(content)
file.close()

# run scm
os.system("chmod +x scm_run.sh")
os.system("./scm_run.sh")
os.system("rm -rf scm_run.sh")

# make folder to save wrf result
wrf_out = "../physicID-" + str(physicID)+ "_tempdiff_" + temp_diff + "_wrf_out"
os.system("mkdir " + wrf_out)

# move wrf result to aim folder and rename
filename = "wrfout_" + str(start_year) + str(start_month) + str(start_day).zfill(2) + "_" + str(start_hour).zfill(2) + "0000" + "-" + str(end_year) + str(end_month) + str(end_day).zfill(2)+ "_" + str(end_hour).zfill(2) + "0000" + ".nc"
os.system("cp -a " + case_path + "/wrfout_d* " + wrf_out + "/" + filename)

# # draw wrf out after processing
# process_wrfout = process_wrfout.process_wrfout(filepath=wrf_out + "/" + filename,date=str(start_year) + str(start_month) + str(start_day).zfill(2) + "_" + str(start_hour).zfill(2) + "0000"
#           + "-" + str(end_year) + str(end_month) + str(end_day).zfill(2)+ "_" + str(end_hour).zfill(2) + "0000", physicID=physicID)
# process_wrfout.single_file()


print("end")
