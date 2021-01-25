# PyStan-CO2-Modeling-Forecasting
Modeling and forecasting atmospheric CO₂ from 1958 into the future

Data file: "weekly_in_situ_co2_mlo.csv" via [Mauna Loa Observatory Dataset from Scripps CO<sub>2</sub> program](https://scrippsco2.ucsd.edu/data/atmospheric_co2/mlo.html)

## Linear Model

- n; //number of observations
- x_t[n]; //CO2 ppm measured values
- t[n]; //number of days since measurements started in 1958
- c0; //intercept
- c1; //linear trend
- c2; //seasonal variation
- c3; //seasonal variation
- c4; //gaussian noise

### linear model 1, y = mx + c
- f1 = c0 + c1*t

### linear model 2, with seasonal variation
- f2 = c0 + c1*t + c2*cos((2*pi*t)/365.25 + c3
