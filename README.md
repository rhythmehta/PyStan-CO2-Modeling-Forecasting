# PyStan-CO2-Modeling-Forecasting
Modeling and forecasting atmospheric CO₂ from 1958 into the future

Data file: "weekly_in_situ_co2_mlo.csv" via [Mauna Loa Observatory Dataset from Scripps CO<sub>2</sub> program](https://scrippsco2.ucsd.edu/data/atmospheric_co2/mlo.html)

## Quadratic Model

- N; // number of observations
- level[N]; // CO2 PPM measured values
- total;   // total days
- t[total]; // days since first measurement
- c0;  // intercept
- c1;  // linear trend
- c2;  // quadratic trend
- phi_x; // seasonal variation
- phi_y; // seasonal variation
- c4; // amplitude
- noise;  // noise 
- c3 = atan2(phi_x, phi_y); //phi

### Likelihood
- level[i] ~ normal(c0+ c1* t[i]+ (c2* (t[i]^2)) + (c4)* cos(((2* pi* t[i])/ 365.25)+ c3), noise)

## Linear Model

- n; //number of observations
- x_t[n]; //CO2 ppm measured values
- t[n]; //number of days since measurements started in 1958
- c0; //intercept
- c1; //linear trend
- c2; //seasonal variation
- c3; //seasonal variation
- c4; //gaussian noise

### Likelihood 
- x_t[i] ~ normal(c0 + c1* t[i] + c2* cos((2* pi* t[i])/ 365.25 + c3), c4);

### function 1, y = mx + c
- f1 = c0 + c1*t

### function 2, with seasonal variation
- f2 = c0 + c1* t + c2* cos((2* pi* t)/ 365.25 + c3
