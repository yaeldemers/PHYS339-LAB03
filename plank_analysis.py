# Import seaborn
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from uncertainties import ufloat, unumpy
from intersect import intersection

# Apply the default theme
sns.set_theme()

inputVoltage = np.load("orangeVoltage.npy")[:,50:250]
inputCurrent = np.load("orangeCurrent.npy")[50:250]

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

poptExp, pcovExp = curve_fit(exp, voltage[0:175], current[0:175], maxfev = 5000) 
perrExp = np.sqrt(np.diag(pcovExp))

poptLin, pcovLin = curve_fit(exp, voltage[0:25], current[0:25], maxfev = 5000) 
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
plt.savefig('figures/orange-LED-IV.png', dpi=300)
plt.show()

# Yellow Turn on voltage: 1.4964217 +/- 0.012986089200325983 lin(0:25) exp(50:)
# Blue Turn on voltage: 2.14221882 +/- 0.02281015358361129 lin(0:50) exp (0:110)
# Red Turn on voltage: 1.33059767 +/- 0.012360585108488581 lin(0:8) exp (8:)
# Green Turn On Voltage: 1.39540369 +/- 0.02142212556381303 lin(0:50) exp (50:150)
# Green-yellow Turn On Voltage: 1.38297366 +/- 0.013274924175250913 lin(0:25) exp (0:150)
# UV  Turn On Voltage: 2.60097467 +/- 0.025951242929463464 lin(0:30) exp (0:200)
# Orange  Turn On Voltage: 1.41547249 +/- 0.012963434413901116 lin(0:25) exp (0:175)

# Chi2 to assess quality of the fit
#difference = abs(current[:]-expected_out)

#chi2 = np.sum(np.square(difference)/expected_out) #TODO divide by std dev square