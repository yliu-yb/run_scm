import datetime
import os
from numpy import ma

class WindProfilerRadar():
    def __init__(self, filefolder, aim_date, site_alt):
        self.filefolder = filefolder
        self.aim_date = datetime.datetime.strptime(aim_date, '%Y/%m/%d %H:%M:%S')
        self.site_alt = site_alt
        self.alt = []
        self.vel = []
        self.z = []
        self.vertical_vel =[]
        self.wind_direction = []
        self.dt = []
        self.files = []
        self.getfiles()
        self.findfileInFixedDate()
        # self.getData()
        self.z = [x * 0.001 for x in self.z]

    def getfiles(self):
        for path, currentDirectory, files in os.walk(self.filefolder):
            for file in files:
                self.files.append(os.path.join(path, file))
        self.files = sorted(self.files)

    def getData(self):
        for file in self.files:
            self.dt.append(datetime.datetime.strptime(file[-34:-20], '%Y%m%d%H%M%S'))
            f = open(file)
            lines = f.readlines()
            i = -1
            vel = []
            z = []
            vertical_vel = []
            wind_direction = []
            for line in lines:
                i += 1
                if i < 3:
                    continue
                line = line.split()
                if line[0].find('NNNN') >= 0 :
                    break
                z.append(float(line[0]))
                if line[1].find('/////') >= 0 or line[2].find('/////') >= 0 or line[3].find('/////') >= 0:
                    wind_direction.append(ma.masked)
                    vel.append(ma.masked)
                    vertical_vel.append(ma.masked)
                    pass
                else:
                    wind_direction.append(float(line[1]))
                    vel.append(float(line[2]))
                    vertical_vel.append(line[3])
            self.vel.append(vel)
            self.wind_direction.append(wind_direction)
            self.vertical_vel.append(vertical_vel)
            self.z = z
    def findfileInFixedDate(self):
        # Z_RADR_I_IAP02_20160601001250_P_WPRD_MST_ROBS.TXT
        find_file = ''
        aim_line = -1
        before_date = datetime.datetime.strptime(self.files[0][-34:-20], '%Y%m%d%H%M%S')
        count = 0
        for file in self.files[1:]:
            after_date = datetime.datetime.strptime(file[-34:-20], '%Y%m%d%H%M%S')
            before_diff = (before_date - self.aim_date).total_seconds()
            after_diff = (after_date - self.aim_date).total_seconds()
            if abs(after_diff) >= abs(before_diff):
                aim_line = count
                find_file = self.files[count]
                print('WindProfilerRadar find file:', find_file, " (UTC):", before_date)
                break
            before_date = after_date
            count += 1
        if find_file == '':
            print('WindProfilerRadar fail to find the data date close to aim date')
            return
        f = open(find_file)
        lines = f.readlines()
        i = -1
        z = []
        wind_direction = []
        vel = []
        for line in lines:
            i += 1
            if i < 3:
                continue
            line = line.split()
            if line[0].find('NNNN') >= 0 or line[1].find('/////') >= 0 or line[2].find('/////') >= 0:
                continue
            else:
                z.append(float(line[0]))
                wind_direction.append(float(line[1]))
                vel.append(float(line[2]))
        self.wind_direction = wind_direction
        self.vel = vel
        self.alt = [h + self.site_alt for h in z]