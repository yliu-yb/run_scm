import numpy
from numpy import ma
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
from matplotlib import colors
import matplotlib as mpl
from matplotlib import cm
from matplotlib import cm as mat_cm
import matplotlib.ticker as ticker


idxTEMP = numpy.arange(-50,50,1)
temp_bar_ticks = [-40,-30,-20,-10,0,10,20,30,40]

idxRH = numpy.arange(0,101,1)
rh_bar_ticks = [0,20,40,60,80,100]

# idxUV = numpy.arange(-30,30,1)
idxUV = [-30,-15,-10,-5,-4,-3,-2,-1,0,1,2,3,4,5,10,15,30]
UV_bar_ticks = [-30,-15,-10,-5,-4,-3,-2,-1,0,1,2,3,4,5,10,15,30]
#
v = 255 / 18.
test_color = []
for i in range(1, 18):
    test_color.append(cm.jet(int(i * v)))
colormap = test_color
cmap = (colors.ListedColormap(colormap)
        .with_extremes(over='#8B008B', under='#008B8B'))
norm = mpl.colors.BoundaryNorm(idxUV, cmap.N)

idxW = [-4 + i * 0.5 for i in range(0, 17)]
W_bar_ticks = idxW
v = 255 / 18.
w_color = []
for i in  range(1, 18):
    w_color.append(cm.jet(int(i * v)))
w_cmap = (colors.ListedColormap(w_color)
        .with_extremes(over='#8B008B', under='#008B8B'))
w_norm = mpl.colors.BoundaryNorm(idxW, w_cmap.N)

idxRef = [-35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35]
ref_bar_ticks = idxRef
v = 255 / 16.
ref_color = []
for i in  range(1, 16):
    ref_color.append(cm.jet(int(i * v)))
ref_cmap = (colors.ListedColormap(ref_color)
        .with_extremes(over='#8B008B', under='#FFFFFF'))
ref_norm = mpl.colors.BoundaryNorm(idxRef, ref_cmap.N)

y_top = 19
cm = 1 / 2.54  # centimeters in inches

# TH adv color
idx_TH_adv = [-9,-3,-1,-0.1,0.1,1,3,9]
TH_adv_bar_ticks = [-9,-3,-1,-0.1,0.1,1,3,9]

rgb_value = 255 / float(len(idx_TH_adv) + 1)
TH_adv_color = []
for i in range(1, len(idx_TH_adv) + 1):
    if i == 4:
        TH_adv_color.append('#FFFFFF')
    else:
        TH_adv_color.append(mat_cm.bwr(int(i * rgb_value)))
print("TH_adv_color", TH_adv_color)
TH_adv_cmap = (colors.ListedColormap(TH_adv_color).with_extremes(over='#8B008B', under='#006666'))
TH_adv_norm = mpl.colors.BoundaryNorm(idx_TH_adv, TH_adv_cmap.N)


# vertical velocity color
idx_w = [-1, -0.5, -0.1, 0, 0.1, 0.5, 1]
w_bar_ticks = [-1, -0.5, -0.1, 0, 0.1, 0.5, 1]
rgb_value = 255 / float(len(idx_w) + 1)
w_color = []
for i in range(1, len(idx_w) + 1):
        w_color.append(mat_cm.bwr(int(i * rgb_value)))
w_color = TH_adv_color[0:3]
w_color.extend(TH_adv_color[4:])
w_cmap = (colors.ListedColormap(w_color).with_extremes(over='#8B008B', under='#006666'))
w_norm = mpl.colors.BoundaryNorm(idx_w, w_cmap.N)

plt.rcParams['font.family'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False
SMALL_SIZE = 9
MEDIUM_SIZE = 10
BIGGER_SIZE = 10
plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


def draw_adv(x, y, w, th, qv, savefolder, variable, bkgrid_res):
    y = numpy.array(y) * 0.001
    xx, yy = numpy.meshgrid(x, y[0])
    y = list(map(list, zip(*y)))

    qv = list(map(list, zip(*qv)))
    qv = numpy.array(qv)
    
    th = list(map(list, zip(*th)))
    th = numpy.array(th)
    
    w = list(map(list, zip(*w)))
    w = numpy.array(w)

    #
    print("w:",w.max(), w.min())
    print("th:",th.max(), th.min())
    print("qv:",qv.max(), qv.min())

    # data = ma.masked_where(data == 0, data)
    nrows, ncols = 3, 1
    figsize = [16 * cm, 15 * cm]
    fig, ax = plt.subplots(nrows = nrows, ncols = ncols, figsize = figsize,
                           dpi = 300, sharex = True, sharey = True)


    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().xaxis.set_minor_locator(mdates.HourLocator(byhour=[4,8,12,16,20]))

    # plt.gca().xaxis.set_minor_locator(mdates.HourLocator(byhour=[4,8,12,16,20]))


    ax[0].set_ylabel("AGH(km)")
    ax[1].set_ylabel("AGH(km)")
    ax[2].set_ylabel("AGH(km)")

    ax[0].yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax[1].yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax[2].yaxis.set_minor_locator(ticker.MultipleLocator(1))

    ax[2].set_xlabel("Date(UTC)")
    ax[2].set_xlabel("Date(UTC)")

    ax[0].set_ylim(top=y_top)
    cs = ax[0].contourf(xx, y, w, norm=w_norm, levels=idx_w, cmap=w_cmap, extend='both')
    cb = plt.colorbar(cs, ax=ax[0], location="right", ticks=w_bar_ticks, pad = 0.01)
    ax[0].set_title("(a) " + variable + " Vertical Velocity", loc='left')
    ax[0].set_title("Units:ms$^{-1}$", loc='right')

    ax[1].set_ylim(top=y_top)
    cs = ax[1].contourf(xx, y, th, norm=TH_adv_norm, levels=idx_TH_adv, cmap=TH_adv_cmap, extend='both')
    cb = plt.colorbar(cs, ax=ax[1], location = "right",  ticks=TH_adv_bar_ticks, pad = 0.01)
    ax[1].set_title("(b) " + variable + " TH Forcing", loc = 'left')
    ax[1].set_title("Units:Kh$^{-1}$", loc = 'right')

    # cs = ax1.contour(xx, y, data, levels = levels, colors = 'k', linewidths = (1,), origin = origin)
    # ax1.clabel(cs, fontsize=9, inline=True)
    ax[2].set_ylim(top=y_top)
    cs = ax[2].contourf(xx, y, qv, norm=TH_adv_norm, levels=idx_TH_adv, cmap=TH_adv_cmap, extend='both')
    cb = plt.colorbar(cs, ax=ax[2], location = "right",  ticks=TH_adv_bar_ticks, pad = 0.01)
    ax[2].set_title("(c) " + variable + " QV Forcing", loc = 'left')
    ax[2].set_title("Units:gkg$^{-1}$h$^{-1}$", loc = 'right')

    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + " _bkgrid_res_" + str(bkgrid_res) + '.png', dpi=300, bbox_inches='tight')
    plt.clf()


def draw_vertical_velocity(x, y, data, xlabel, ylabel, title, units, variable, savefolder):
    y = numpy.array(y) * 0.001
    xx, yy = numpy.meshgrid(x, y[0])
    y = list(map(list, zip(*y)))
    data = list(map(list, zip(*data)))
    data = numpy.array(data)
    # data = ma.masked_where(data == 0, data)
    figsize = [16 * cm, 8 * cm]

    fig = plt.figure(figsize=figsize, dpi=300)
    ax1 = fig.add_subplot(111)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

    ax1.set_ylim(top=y_top)

    cs = ax1.contourf(xx, y, data, norm=w_norm, levels=idx_w, cmap=w_cmap, extend='both')
    cb = plt.colorbar(cs, ax=ax1, location = "right",  ticks=w_bar_ticks)

    ax1.set_title(units, loc='right')
    ax1.set_title(title, loc='left')

    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + '.png', dpi=300, bbox_inches='tight')
    plt.clf()
    print("max:", data.max(), ",min:", data.min())

def draw_force(x, y, data, xlabel, ylabel, title, barlabel, variable, savefolder):
    y = numpy.array(y) * 0.001
    xx, yy = numpy.meshgrid(x, y[0])
    y = list(map(list, zip(*y)))
    data = list(map(list, zip(*data)))
    data = numpy.array(data)
    # data = ma.masked_where(data == 0, data)

    fig = plt.figure(figsize=(12, 4), dpi=300)
    ax1 = fig.add_subplot(111)

    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%H:%M'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%H:%M'))
    ax1.set_ylim(top=y_top)

    cs = ax1.contourf(xx, y, data, cmap='jet')
    fig.colorbar(cs, label=barlabel)

    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + '.png', dpi=300, bbox_inches='tight')
    plt.clf()


def draw_interp_force(x, y, data, xlabel, ylabel, title, barlabel, variable, savefolder):
    y = numpy.array(y) * 0.001
    xx, yy = numpy.meshgrid(x, y[0])
    y = list(map(list, zip(*y)))
    data = list(map(list, zip(*data)))
    data = numpy.array(data)
    # data = ma.masked_where(data == 0, data)
    #
    fig = plt.figure(figsize=(12, 4), dpi=300)
    ax1 = fig.add_subplot(111)

    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.set_ylim(top=y_top)

    cs = ax1.contourf(xx, y, data, cmap='jet')
    fig.colorbar(cs, label=barlabel)
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_cloudradar_ref(type, x, y, data, xlabel, ylabel, title, barlabel, variable, savefolder):
    if type == 'wrf':
        y = numpy.array(y) * 0.001
        xx, yy = numpy.meshgrid(x, y[0])
        y = list(map(list, zip(*y)))
        data = list(map(list, zip(*data)))
        data = numpy.array(data)
        data = ma.masked_where(data <= -100, data)

        fig = plt.figure(figsize=(12, 4), dpi=300)
        ax1 = fig.add_subplot(111)

        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)

        cs = ax1.contourf(xx, y, data, norm=ref_norm, levels=idxRef, cmap=ref_cmap, extend='both')
        fig.colorbar(cs, ticks=ref_bar_ticks, label=barlabel)

        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + '.png', dpi=300, bbox_inches='tight')
        plt.clf()
        pass
    else:
        data = list(map(list, zip(*data)))
        data = numpy.array(data)
        data = ma.masked_where(data <= -100, data)

        y = numpy.array(y) * 0.001

        fig = plt.figure(figsize=(12, 4), dpi=300)
        ax1 = fig.add_subplot(111)

        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)

        cs = ax1.contourf(x, y, data, norm=ref_norm, levels=idxRef, cmap=ref_cmap, extend='both')
        fig.colorbar(cs, ticks=ref_bar_ticks, label=barlabel)

        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + '.png', dpi=300,
                    bbox_inches='tight')
        plt.clf()
        pass

def draw_wind_profiler(dt, z, souding_u, souding_v, start_date, end_date, savefolder):
    z = numpy.array(z) * 0.001

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)

    if dt[len(dt) - 1] - dt[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.set_ylim(top=y_top)

    X, Y = numpy.meshgrid(dt, z)
    # ax1.barbs(X, Y, souding_u, souding_v, length = 7)
    ax1.barbs(X, Y, souding_u, souding_v, sizes=dict(emptybarb=0))

    ax1.set_title('Wind')
    # ax1.axes.get_xaxis().set_visible(False)
    fig.set_tight_layout(True)

    plt.savefig("./" + savefolder + '/windprofiler_' + start_date + '_' + end_date + '.png', dpi = 300, bbox_inches='tight')
    plt.clf()

def draw_wind_uv(type, x, y, data, xlabel, ylabel, title, barlabel, start_date, end_date, variable, savefolder):
    if type == 'wrf':
        y = numpy.array(y) * 0.001
        xx, yy = numpy.meshgrid(x, y[0])
        y = list(map(list, zip(*y)))
        data = list(map(list, zip(*data)))


        fig = plt.figure(figsize=(6, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)
        cs = ax1.contourf(xx, y, data, norm=norm, levels=idxUV, cmap=cmap, extend='both')
        # cs = ax1.contourf(x, y, data, cmap='jet', levels=idxUV)
        fig.colorbar(cs, ticks=UV_bar_ticks, label=barlabel)

        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
        plt.clf()
    else:
        data = list(map(list, zip(*data)))
        y = numpy.array(y) * 0.001

        fig = plt.figure(figsize=(6, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)
        cs = ax1.contourf(x, y, data, norm=norm, levels=idxUV, cmap=cmap, extend='both')
        # cs = ax1.contourf(x, y, data, cmap='jet', levels=idxUV)
        fig.colorbar(cs, ticks=UV_bar_ticks, label=barlabel)

        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300,
                    bbox_inches='tight')
        plt.clf()


def draw_wind_w(type, x, y, data, xlabel, ylabel, title, barlabel, start_date, end_date, variable, savefolder):
    if type == 'wrf':
        y = numpy.array(y) * 0.001
        xx, yy = numpy.meshgrid(x, y[0])
        y = list(map(list, zip(*y)))
        data = list(map(list, zip(*data)))

        fig = plt.figure(figsize=(6, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)
        cs = ax1.contourf(xx, y, data, norm=w_norm, levels=idxW, cmap=w_cmap, extend='both')
        # cs = ax1.contourf(x, y, data, cmap='jet', levels=idxUV)
        fig.colorbar(cs, ticks=W_bar_ticks, label=barlabel)

        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
        plt.clf()
    else:
        data = list(map(list, zip(*data)))
        y = numpy.array(y) * 0.001

        fig = plt.figure(figsize=(6, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)
        cs = ax1.contourf(x, y, data, norm=w_norm, levels=idxW, cmap=w_cmap, extend='both')
        # cs = ax1.contourf(x, y, data, cmap='jet', levels=idxUV)
        fig.colorbar(cs, ticks=W_bar_ticks, label=barlabel)

        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300,
                    bbox_inches='tight')
        plt.clf()

def draw_temp(type, x, y, data, xlabel, ylabel, title, barlabel, start_date, end_date, variable, savefolder):
    if type == 'wrf':
        y = numpy.array(y) * 0.001
        xx, yy = numpy.meshgrid(x, y[0])
        y = list(map(list, zip(*y)))

        data = list(map(list, zip(*data)))
        data = numpy.array(data)
        data = data - 273.15

        fig = plt.figure(figsize=(6, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)
        cs = ax1.contourf(xx, y, data, cmap='jet', levels = idxTEMP)
        fig.colorbar(cs, ticks=temp_bar_ticks, label=barlabel)
        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + '_' + start_date + '_' + end_date + '.png', dpi = 300, bbox_inches='tight')
        plt.clf()
    else:
        data = list(map(list, zip(*data)))
        data = numpy.array(data)
        data = data - 273.15
        y = numpy.array(y) * 0.001

        fig = plt.figure(figsize=(6, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)
        cs = ax1.contourf(x, y, data, cmap='jet', levels=idxTEMP)
        fig.colorbar(cs, ticks=temp_bar_ticks, label=barlabel)
        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300,
                    bbox_inches='tight')
        plt.clf()

def draw_rh(type, x, y, data, xlabel, ylabel, title, barlabel, start_date, end_date, variable, savefolder):
    if type == 'wrf':
        y = numpy.array(y) * 0.001
        xx, yy = numpy.meshgrid(x, y[0])
        y = list(map(list, zip(*y)))
        data = list(map(list, zip(*data)))

        fig = plt.figure(figsize=(6, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)
        cs = ax1.contourf(xx, y, data, cmap='jet', levels=idxRH)
        fig.colorbar(cs, ticks=rh_bar_ticks, label=barlabel)
        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
        plt.clf()
    else:
        y = numpy.array(y) * 0.001
        data = list(map(list, zip(*data)))

        fig = plt.figure(figsize=(6, 4), dpi=300)
        ax1 = fig.add_subplot(111)
        if x[len(x) - 1] - x[0] > timedelta(days=1):
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        else:
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax1.set_ylim(top=y_top)
        cs = ax1.contourf(x, y, data, cmap='jet', levels=idxRH)
        fig.colorbar(cs, ticks=rh_bar_ticks, label=barlabel)
        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        fig.set_tight_layout(True)
        plt.savefig("./" + savefolder + '/' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300,
                    bbox_inches='tight')
        plt.clf()

def draw_temp_line(x, y, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    # y = ma.masked_where(y >= 50, y)
    y = [i - 273.15 for i in y]
    y = numpy.array(y)
    y = ma.masked_where(y <= -50, y)

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, linewidth = 2.0, color = 'black')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()
    pass

def draw_rh_line(x, y, xlabel, ylabel, title, start_date, end_date, savefolder):
    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, linewidth = 2.0, color = 'black')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/tower_rh10_' + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_uv_line(x, y, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    y = numpy.array(y)
    y = ma.masked_where(y <= -100, y)
    # y = ma.masked_where(y >= 50, y)

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, '.', c='black', markersize=1, markerfacecolor='none')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_rain(x, y, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    # y = numpy.array(y)
    # y = ma.masked_where(y <= -50, y)
    # y = ma.masked_where(y >= 50, y)

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, '.', c='black', markersize=1, markerfacecolor='none')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/wrf_' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_rain_compare(x, y, dlabel, x1, y1, d1label, xlabel, ylabel, title, start_date, end_date, variable, savefolder):

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, '.', c='red', markersize=1, markerfacecolor='none', label=dlabel)
    ax1.plot(x1, y1, '.', c='black', markersize=1, markerfacecolor='none', label=d1label)
    plt.legend(loc = 'upper right')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_uv_line_compare(x, y, dlabel, x1, y1, d1label,x2, y2, d2label, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    y = numpy.array(y)
    y1 = numpy.array(y1)
    y2 = numpy.array(y2)
    y = ma.masked_where(y <= -100, y)
    y1 = ma.masked_where(y1 <= -100, y1)
    y2 = ma.masked_where(y2 <= -100, y2)

    y = ma.masked_where(y >= 100, y)
    y1 = ma.masked_where(y1 >= 100, y1)
    y2 = ma.masked_where(y2 >= 100, y2)


    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, '.', c='black', markersize=1, markerfacecolor='none', label = dlabel)
    ax1.plot(x1, y1, '.', c='green', markersize=1, markerfacecolor='none', label = d1label)
    ax1.plot(x2, y2, '.', c='red', markersize=1, markerfacecolor='none', label = d2label)
    plt.legend(loc = 'best')

    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_temp_line_compare(x, y, dlabel, x1, y1, d1label,x2, y2, d2label, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    y = [i - 273.15 for i in y]
    y1 = [i - 273.15 for i in y1]
    y2 = [i - 273.15 for i in y2]

    y = numpy.array(y)
    y = ma.masked_where(y <= -50, y)
    y1 = numpy.array(y1)
    y1 = ma.masked_where(y1 <= -50, y1)
    y2 = numpy.array(y2)
    y2 = ma.masked_where(y2 <= -50, y2)

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, linewidth = 2.0, color = 'black', label = dlabel)
    ax1.plot(x1, y1, linewidth = 2.0, color = 'green', label = d1label)
    ax1.plot(x2, y2, linewidth = 2.0, color = 'red', label = d2label)
    plt.legend(loc = 'best')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_q_line_compare(x, y, dlabel, x1, y1, d1label,x2, y2, d2label, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, linewidth = 2.0, color = 'black', label = dlabel)
    ax1.plot(x1, y1, linewidth = 2.0, color = 'green', label = d1label)
    ax1.plot(x2, y2, linewidth = 2.0, color = 'red', label = d2label)
    plt.legend(loc = 'best')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_std(x, y, yerror, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.errorbar(x, y, yerror, fmt="o", color="blue", ecolor='grey', elinewidth=1, capsize=2, markersize=1)
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/std_' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300,
                bbox_inches='tight')
    plt.clf()

def draw_rain_std_compare(x0, y0, yerror, d0label, x, y, dlabel, x1, y1, d1label, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.errorbar(x0, y0, yerror, fmt="o", color="blue", ecolor='grey', elinewidth=1, capsize=2, markersize=1, label=d0label)
    ax1.plot(x, y, '.', c='red', markersize=1, markerfacecolor='none', label=dlabel)
    ax1.plot(x1, y1, '.', c='black', markersize=1, markerfacecolor='none', label=d1label)
    plt.legend(loc = 'upper right')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/std_' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_temp_std_compare(x0, y0, yerror, d0label, x, y, dlabel, x1, y1, d1label,x2, y2, d2label, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    y = [i - 273.15 for i in y]
    y1 = [i - 273.15 for i in y1]
    y2 = [i - 273.15 for i in y2]
    y0 = [i - 273.15 for i in y0]

    y0 = numpy.array(y0)
    y0 = ma.masked_where(y0 <= -50, y0)
    y = numpy.array(y)
    y = ma.masked_where(y <= -50, y)
    y1 = numpy.array(y1)
    y1 = ma.masked_where(y1 <= -50, y1)
    y2 = numpy.array(y2)
    y2 = ma.masked_where(y2 <= -50, y2)

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.errorbar(x0, y0, yerror, fmt="o", color="blue", ecolor='grey', elinewidth=1, capsize=2, markersize=1, label=d0label)
    ax1.plot(x, y, linewidth = 2.0, color = 'black', label = dlabel)
    ax1.plot(x1, y1, linewidth = 2.0, color = 'green', label = d1label)
    ax1.plot(x2, y2, linewidth = 2.0, color = 'red', label = d2label)
    plt.legend(loc = 'best')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/std_' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_q_std_compare(x0, y0, yerror, d0label, x, y, dlabel, x1, y1, d1label,x2, y2, d2label, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.errorbar(x0, y0, yerror, fmt="o", color="blue", ecolor='grey', elinewidth=1, capsize=2, markersize=1, label=d0label)
    ax1.plot(x, y, linewidth = 2.0, color = 'black', label = dlabel)
    ax1.plot(x1, y1, linewidth = 2.0, color = 'green', label = d1label)
    ax1.plot(x2, y2, linewidth = 2.0, color = 'red', label = d2label)
    plt.legend(loc = 'best')
    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/std_' + variable + "_" + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

def draw_uv_std_compare(x0, y0, yerror, d0label, x, y, dlabel, x1, y1, d1label,x2, y2, d2label, xlabel, ylabel, title, start_date, end_date, variable, savefolder):
    y = numpy.array(y)
    y1 = numpy.array(y1)
    y2 = numpy.array(y2)
    y = ma.masked_where(y <= -100, y)
    y1 = ma.masked_where(y1 <= -100, y1)
    y2 = ma.masked_where(y2 <= -100, y2)

    y = ma.masked_where(y >= 100, y)
    y1 = ma.masked_where(y1 >= 100, y1)
    y2 = ma.masked_where(y2 >= 100, y2)

    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax1 = fig.add_subplot(111)
    if x[len(x) - 1] - x[0] > timedelta(days=1):
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    else:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, '.', c='black', markersize=1, markerfacecolor='none', label = dlabel)
    ax1.errorbar(x0, y0, yerror, fmt="o", color="blue", ecolor='grey', elinewidth=1, capsize=2, markersize=1, label=d0label)
    ax1.plot(x1, y1, '.', c='green', markersize=1, markerfacecolor='none', label = d1label)
    ax1.plot(x2, y2, '.', c='red', markersize=1, markerfacecolor='none', label = d2label)
    plt.legend(loc = 'best')

    ax1.set_title(title)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    fig.set_tight_layout(True)
    plt.savefig("./" + savefolder + '/std_' + variable + '_' + start_date + '_' + end_date + '.png', dpi=300, bbox_inches='tight')
    plt.clf()

