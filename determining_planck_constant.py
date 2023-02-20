import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import seaborn as sns

sns.set_theme()

y = [1.33059767, 1.41547249, 1.4964217, 1.38297366, 1.39540369, 2.14221882, 2.60097467]
x = [478229.29, 494351.32, 509398.91, 529274.30, 561535.29, 648809.14, 750904.65]

yerr = [0.012360585108488581, 0.012963434413901116, 0.012986089200325983, 0.013274924175250913, 0.02142212556381303, 0.02281015358361129, 0.025951242929463464]
xerr = [3641.97, 5020.76, 3710.36, 9969.66, 12827.74, 10503.83, 7217.16]


y = 1.602*10**(-19)*np.array(y,dtype=float)
yerr = 1.602*10**(-19)*np.array(yerr,dtype=float)

x = 10**9*np.array(x,dtype=float)
xerr = 10**9*np.array(xerr,dtype=float)


def linear(x, a, b):
    return a*x+b

popt, pcov = curve_fit(linear, x, y)
perr = np.sqrt(np.diag(pcov))


fit=np.zeros(7)
low_bound=np.zeros(7)
high_bound=np.zeros(7)

for i in range(7):
    fit[i]=(popt[0])*x[i]+popt[1]
    low_bound[i]=(popt[0]-perr[0])*x[i]+popt[1]-perr[1]
    high_bound[i]=(popt[0]+perr[0])*x[i]+popt[1]+perr[1]


plt.figure(dpi=1500)
plt.errorbar(x, y, xerr = xerr, yerr=5*yerr, fmt = '.', color = 'grey')
plt.plot(x,y,'.', color = 'black', markersize = 6)
#yerr is scaled by a factor of 5

plt.plot(x, fit, linewidth=0.5, color='black', label = r'Linear fit, with $slope=7.696\times 10^{-34} \pm 0.974\times 10^{-34}J\cdot s$')
plt.fill_between(x, low_bound, high_bound, alpha=0.2)

plt.plot(x, 6.626*10**(-34)*x, '--', label = r"Expected Relationship, with $slope = 6.626\times 10^{-34}J\cdot s$")

plt.xlabel("Frequency (Hz)")
plt.ylabel(r'$e \cdot$ Turn on Voltage (J)')
plt.legend()

plt.savefig('Planck Constant.png')


print("a and b:", popt)
print("error a and b: ", perr)
print("h:", popt[0], "+-", perr[0], "J*s")
