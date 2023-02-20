# Import seaborn
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from uncertainties import ufloat, unumpy
from intersect import intersection

# Apply the default theme
sns.set_theme()

inputVoltage = np.load("runs/grellowVoltage.npy")[:,50:250]
inputCurrent = np.load("runs/grellowCurrent.npy")[50:250]

"""
Uncertainty in current was not saved when taking the measurements
We will calculate it here assuming that the uncertainty of V0 and V1
was the same. This seems like a safe assumption given that both 
measurements were repeated 250 times (200 when ommiting transient)
with the same equipments and unit conversion.
"""

R = ufloat(901, 0.5)
buffer = ufloat(1,0)
volt0Error = unumpy.uarray(np.ones(len(inputCurrent)), inputVoltage[1])
volt1Error = unumpy.uarray(np.zeros(len(inputCurrent)), inputVoltage[1])
tempError = (np.abs(volt0Error-volt1Error)-buffer)/R

# Applying the error to the voltage and current
voltageWithError = unumpy.uarray(inputVoltage[0], inputVoltage[1])
currentWithError = unumpy.uarray(inputCurrent, 0) + tempError

# Separating values and errors for plotting purposes
current = unumpy.nominal_values(currentWithError)
currentError = unumpy.std_devs(currentWithError)

voltage = unumpy.nominal_values(voltageWithError)
voltageError = unumpy.std_devs(voltageWithError)

def exp(x, a, b):
   return  a*(np.exp(x/b)-1)

full_span = np.linspace(voltage[0], voltage[199], 200)

# values tweaked to find best fit separation
"""
Yellow: lin(0:25) exp(50:) x
Blue:  lin(0:50) exp (0:110)
Red Turn: lin(0:8) exp (8:) x
Green: lin(0:50) exp (50:150) x
Green-yellow: lin(0:25) exp (0:150) x
UV: lin(0:30) exp (0:200) x 
Orange: lin(0:25) exp (0:175) x 
"""

expLow, expHigh = 0, 150
linLow, linHigh = 0, 25

poptExp, pcovExp = curve_fit(exp, voltage[expLow:expHigh], current[expLow:expHigh], maxfev = 5000) 
perrExp = np.sqrt(np.diag(pcovExp))

poptLin, pcovLin = curve_fit(exp, voltage[linLow:linHigh], current[linLow:linHigh], maxfev = 5000) 
perrLin = np.sqrt(np.diag(pcovLin))

# Data for best fit curve
expected_out_exp=exp(full_span, poptExp[0], poptExp[1])
expected_out_lin=exp(full_span, poptLin[0], poptLin[1])

x , y = intersection(full_span, expected_out_lin, full_span, expected_out_exp)

plt.subplots(figsize=(15, 5))
# Using subplot function and creating plot one
plt.subplot(1, 2, 1)  # row 1, column 2, count 1
plt.errorbar(voltage, current, yerr=currentError, xerr=voltageError, fmt=".", ecolor="black", elinewidth=0.5)
plt.plot(full_span, expected_out_exp)
plt.plot(full_span, expected_out_lin)
plt.xlim([1.5, voltage[199]+0.025])
plt.title("$(a)$")
plt.ylabel("Current (A)")
plt.xlabel("$\Delta V$ through orange diode")
 
# using subplot function and creating plot two
# row 1, column 2, count 2
plt.subplot(1, 2, 2)
plt.errorbar(voltage, current, yerr=0, xerr=0, fmt=".", ecolor="black", elinewidth=0.5)
plt.plot(full_span, expected_out_exp)
plt.plot(full_span, expected_out_lin)
plt.ylim([10**(-8), current[199]])
plt.axvline(x = x, color = 'black', linestyle="--")
plt.yscale("log")
plt.title("$(b)$")
plt.ylabel("Log Current (A)")
plt.xlabel("$\Delta V$ through orange diode")

# space between the plots
plt.tight_layout()

# show plot
#plt.savefig('figures/orange-LED-IV.png', dpi=300)
plt.show()

# Chi2 to assess quality of the fit
expected_out = exp(full_span[expLow:expHigh], poptExp[0], poptExp[1])

difference = abs(current[expLow:expHigh]-expected_out)
index = []
currentError=currentError[expLow:expHigh]

# Some value have zero error, remove them from the chi2
for i in range(len(currentError)):
    if currentError[i]==0:
        index.append(i)

currentError = np.delete(currentError, index)
difference = np.delete(difference, index)
expected_out = np.delete(expected_out, index)

dof = len(difference)-2

reducedChi2 = np.sum(np.square(difference)/(currentError**2))/dof
chi2 = np.sum(np.square(difference)/(expected_out))
