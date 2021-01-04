import pystan

linear_stan_code = """
data {  
    int<lower=1> n;       // number of observations   
    real<lower=0> x_t[n] ; // CO2 ppm measured values 
    int<lower=0> t[n];      // number of days since measurements started in 1958
}
parameters {  
    //prior parameters
    real<lower=0> c0; //intercept
    real<lower=0> c1; //linear trend
    real<lower=0> c2; //seasonal variation
    real<lower=0> c3; //seasonal variation
    real c4; //gaussian noise
}
model {
    c0 ~ normal(356, 28);
    c1 ~ normal(0,10);
    c2 ~ normal(0,10);
    c3 ~ normal(0,10);
    c4 ~ normal(0,1); 
    for(i in 1:n) {
        x_t[i] ~ normal(c0 + c1*t[i] + c2*cos((2*pi()*t[i])/365.25 + c3), c4); // likelihood
  }
}
"""

#Compile Stan Model
linear_stan_model = pystan.StanModel(model_code = linear_stan_code)

#Data for Stan Model
linear_stan_data = {
    'n' : n_weeks,
    'x_t': df.level[:n_weeks],
    't': df.days[:n_weeks]
}

#Fit Stan Model
linear_stan_results = linear_stan_model.sampling(data = linear_stan_data)
print(linear_stan_results) #printing results

#Extract samples
linear_samples = linear_stan_results.extract()
linear_parameters = ['c0', 'c1', 'c2','c3', 'c4']
c0, c1, c2, c3 = linear_samples['c0'], linear_samples['c1'], linear_samples['c2'], linear_samples['c3']
t = df.days[:n_weeks]

#linear model 1 function equation, y = mx + c
f1 = c0.mean() + c1.mean()*t

#plotting model vs original
plot_model(f1, nthWeek)

#linear model 2 with seasonal variation
f2 = c0.mean() + c1.mean()*t + c2.mean()*np.cos((2*np.pi*t)/365.25 + c3.mean())

#plotting model vs original
plot_model(f2, nthWeek)

#generating pair plots for parameters
pair_plot_model(linear_samples, linear_parameters)

#plotting autocorrelations plots for parameters
for param in linear_parameters:
  plt.figure(figsize=(12,4))
  plot_acf(linear_samples[param])
  plt.title('Autocorrelation of '+ str(param) +' samples')
plt.show()




	






