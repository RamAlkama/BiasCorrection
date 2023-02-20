# BiasCorrection: Quantile-Matching Bias Correction Approach
In the context of climate and environmental data, bias correction can be used to adjust for errors in historical weather records and to remove inconsistencies between models and observations.

Python is a popular programming language that can be used to perform bias correction. Here are some steps that can be followed to perform bias correction in Python:

    Import required libraries 
    Load the observational data and model data.
    Calculate the bias between the two datasets.
    Subtract the mean bias from the model data.
    

Quantile-Matching Bias Correction Approach is a statistical method used to adjust the bias in data by matching the distribution of observed data with the distribution of model data.

# The classical approach 
The classical approach involves comparing the cumulative distribution function (CDF) of the observed data with the CDF of the model data, and then adjusting the model data to match the observed data. This method is straightforward and easy to implement, but it assumes that the model and observed data have the same shape.

#  delta approach
The delta approach, on the other hand, is a modification of the classical approach that accounts for differences in the shape of the model and observed data. Instead of adjusting the model data to match the observed data directly, this method adjusts the difference between the model and observed data, also known as the delta. The delta is then added to the model data to obtain the corrected data. This method is more flexible and can handle differences in the shape of the data, but it is also more complex and requires more computation.

# Example of use:

python quantile2d.py -obs obs_1980_2010.nc -vobs tmp -hist sim_1980_2010.nc -vhist tas -fut sim_2070_2100.nc -vfut tas -o corrected_2070_2100.nc

    
