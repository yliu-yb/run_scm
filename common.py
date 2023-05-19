from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

def interpolation(A_value:list, A_hieght:list, B_height:list):
    result = []
    result_height = []
    for b_h in B_height:
        for i in range(len(A_hieght)-1):
            if A_hieght[i] < b_h and b_h < A_hieght[i+1]:
                result_height.append(b_h)
                result.append(A_value[i] * ((A_hieght[i+1] - b_h)/(A_hieght[i+1]-A_hieght[i])) + A_value[i+1] * ((b_h - A_hieght[i])/(A_hieght[i+1]-A_hieght[i])))
                break
    return result_height, result

def interpolation_2(list_x, list_y, interpolate_x):
    print(list_x)
    print(list_y)
    y_interp = interp1d(list_x, list_y, bounds_error=False)
    interpolate_y = y_interp(interpolate_x)
    return interpolate_y

def objective(x, a, b, c, d, f):
	return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + f

def interpolation_3(list_x, list_y, interpolate_x):
    popt, _ = curve_fit(objective, list_x, list_y)
    # summarize the parameter values
    a, b, c, d, f = popt
    interpolate_y = objective(interpolate_x, a, b, c, d, f)
    return interpolate_y