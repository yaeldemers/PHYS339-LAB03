import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns


sns.set_theme()

def generating_spectra_plot(data, title):
    
    #generating wavelength array (x-axis)
    wav = np.transpose(data)[0]
    wav = np.array(wav)
    wavelength = wav.astype(np.float64)
    
    #generating intensity array (y-axis)
    Int = np.transpose(data)[1]
    Int = np.array(Int)
    intensity = Int.astype(np.float64)

    #creating plot
    F1 = plt.figure(figsize = (10,7))
    plt.plot(wavelength, intensity)

    # Find the x value corresponding to the maximum y value
    max_intensity = max(intensity) # Find the maximum y value
    max_wavelength = wavelength[intensity.argmax()]  
    
    #Computing the FWHM
    half_max= (max(intensity))/2
    left_x = wavelength[np.where(intensity[:np.argmax(intensity)] <= half_max)[0][-1]]
    right_x = wavelength[np.where(intensity[np.argmax(intensity):] <= half_max)[0][0] + np.argmax(intensity)]
    FWHM = (right_x-left_x)/2
    FWHM = round(FWHM, 4)
    
    print("Wavelength:",max_wavelength, (u"\u00B1"), FWHM)
    print("Max Intensity:", max_intensity)
    

    #Plot Specifications
    plt.xlabel("Wavelength (nm)", fontsize = 20)
    plt.ylabel('Intensity', fontsize = 20)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.title(title, fontsize = 25)
    plt.tight_layout()
        
    plt.show()
    
file = open("6a-green.csv")
csvreader = csv.reader(file)
green1 = []
for row in csvreader:
    green1.append(row)
    
generating_spectra_plot(green1, "Green 1")

file = open("6b-green.csv")
csvreader = csv.reader(file)
green2 = []
for row in csvreader:
    green2.append(row)
    
generating_spectra_plot(green2, "Green 2")

#Calculating average frequency value for Green Light
#weighted mean gives a more accurate estimate of the true mean

# Define the two wavelengths and their uncertainties
g1 = 533.88
g2 = 533.88
g1_sig = 17.89
g2_sig = 16.67

# Calculate the weights
w1 = 1/g1_sig**2
w2 = 1/g2_sig**2

# Calculate the weighted mean
mean = (w1*g1 + w2*g2) / (w1 + w2)

# Calculate the uncertainty in the weighted mean
sig_mean = np.sqrt(1 / (w1 + w2))

# Convert the mean wavelength to frequency
c = 299792458 # speed of light in m/s
nu_mean = c / mean

# Convert the uncertainty to frequency
sig_nu_mean = (c / mean**2) * sig_mean

# Print the result
print("The average frequency for green is {0:.2f} +/- {1:.2f} Hz".format(nu_mean, sig_nu_mean))