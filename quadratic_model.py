#Improved model proposal using quadratic long term trend and cosine seasonal variation

proposed_stan_code = """
data {
    int<lower=0> N;        // The number of data
    real level[N];           // co2 ppm level data
    int<lower=0> total;   // total days
    real t[total];        // days since first measurement
}
parameters {
    real<lower=0> c0;  // y
    real<lower=0> c1;  // linear
    real<lower=0> c2;  // quad
    real phi_x;          // seasonal
    real phi_y;          // seasonal
    real<lower=0> c4;     // amplitude
    real<lower=0> noise;  // noise 
} 
transformed parameters {
    real c3;
    c3 = atan2(phi_x, phi_y); //phi
} 
model { //priors
    c0 ~ normal(356,28);
    c1 ~ normal(0,10);
    c2 ~ normal(0,10);
    phi_x ~ normal(0,1);
    phi_y ~ normal(0,1); 
    c4 ~ normal(0,10);
    noise ~ normal(0,1);
    
    for(i in 1:N) {
        level[i] ~ normal(c0+c1*t[i]+(c2*(t[i]^2))+(c4)*cos(((2*pi()*t[i])/365.25)+c3),noise);
    }
}
generated quantities {
    real pred[total];
    for(i in 1:total) {
        pred[i] = normal_rng(c0+c1*t[i]+(c2*(t[i]^2))+(c4)*cos(((2*pi()*t[i])/365.25)+c3),noise);
        }
} // generating quantities
"""

#Compile Stan Model
proposed_stan_model = pystan.StanModel(model_code = proposed_stan_code)

#Data for Stan Model
stan_data = { 
    'N': 3199, 
    'total':5288,
    'level': df.level[:3199], 
    't': df.days
}

#Fit Stan Model
results = proposed_stan_model.sampling(data=stan_data)

#Extract Samples
proposed_parameters = ['c0','c1','c2','c3','c4', 'noise']
samples = results.extract()

#generating pair plots for parameters
pair_plot_model(samples, proposed_parameters)

#autocorrelation plots
for param in proposed_parameters:
  plt.figure(figsize=(9,3))
  plot_acf(samples[param])
  plt.title('Autocorrelation of '+ str(param) +' samples')
plt.show()

#confidence interval of each sample
conf_int = np.percentile(pred, axis=0, q=[2.5, 97.5])
pred = samples['pred'] #extracting predicted posterior
avgPred  = [np.mean(pred[:,i]) for i in range(len(df))] #taking mean

start, end = 0, len(df) #cropping time, 1958 to 2060, edit to zoom in
x = df.date[start:end] #x-axis, date
plt.figure(figsize=(20,10)) #defining plot size
plt.plot(x, df.level[start:end], label = 'Original') #original data 
plt.plot(x, avgPred[start:end], label = 'Prediction') #model predicted data
plt.title('Original vs. Quadratic Model')  #plot labels
plt.ylabel('CO2 (ppm)') #y-axis labels
plt.xlabel('Time') #x-axis label
plt.legend() #show legend
plt.grid() #add grid
plt.show() #show plot