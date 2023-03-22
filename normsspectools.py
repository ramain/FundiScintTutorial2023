import numpy as np
import astropy.units as u
from astropy.io import fits
from astropy.time import Time

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def norm_sspec(S, ft, tau, Ngrid=2000, taumin=0.1, tauref=None, xr=1.):
    
    img = np.zeros( (Ngrid+1, len(tau) ) )
    if not tauref:
        tauref = max(tau)
        
    xgrid = np.linspace(-xr*max(ft), xr*max(ft), Ngrid+1, endpoint=True)    
    for i in range(len(tau)):
        taui = tau[i]
        if (taui > taumin):
            for j in range(Ngrid+1):
                fti = xgrid[j]*np.sqrt(taui/ tauref)
                findex = find_nearest(ft, fti)
                img[j, i] = S[findex, i]
                
    curvaxis = tauref / (xgrid)**2.0
    return img, xgrid, curvaxis
                   
    
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def parabola(x, x0, A, C):
    return A*(x-x0)**2 + C

def fit_parabola(x, y):
    """
    Fit a parabola and return the value and error for the peak
    """

    # increase range to help fitter
    ptp = np.ptp(x)
    x = x*(1000/ptp)

    # Do the fit
    params, pcov = np.polyfit(x, y, 2, cov=True)
    yfit = params[0]*np.power(x, 2) + params[1]*x + params[2]  # y values

    # Get parameter errors
    errors = []
    for i in range(len(params)):  # for each parameter
        errors.append(np.absolute(pcov[i][i])**0.5)

    # Get parabola peak and error
    peak = -params[1]/(2*params[0])  # Parabola max (or min)
    peak_error = np.sqrt((errors[1]**2)*((1/(2*params[0]))**2) +
                         (errors[0]**2)*((params[1]/2)**2))  # Error on peak

    peak = peak*(ptp/1000)
    peak_error = peak_error*(ptp/1000)

    return yfit, peak, peak_error


def fit_log_parabola(x, y):
    """
    Fit a log-parabola and return the value and error for the peak
    """

    # Take the log of x
    logx = np.log(x)
    ptp = np.ptp(logx)
    x = logx*(1000/ptp)  # increase range to help fitter

    # Do the fit
    yfit, peak, peak_error = fit_parabola(x, y)
    frac_error = peak_error/peak

    peak = np.e**(peak*ptp/1000)
    # Average the error asymmetries
    peak_error = frac_error*peak

    return yfit, peak, peak_error