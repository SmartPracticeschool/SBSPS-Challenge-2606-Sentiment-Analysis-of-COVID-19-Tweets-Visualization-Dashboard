
Gradient Boosting Regression model was used to predict the positivity score (daily) if the 	government decides to extend lockdown.

Input Features: 
1. Confirmed Cases
2. Active Cases
3. Deaths 
4. Recovered Cases

Output: Positivity score indicating how positive will the people be if the government decides to extend lockdown.

Train and Test Metrics (Rounded up to 4 decimal places):

Mean Absolute Error (MAE):
Train  0.0262
Test  0.0312

Root Mean Square Error (RMSE):
Train  0.0501
Test  0.0496

Mean Squared Error (MSE):
Train  0.0025
Test 0.0025

R2 Score:

Train  0.815
Test 0.8214



The output provided is dynamic and depends on current Covid-19 Cases in India.
A Python REST API is built that can be called from the Dashboard to plot the predictive lockdown analytics graph daily. 

(The positivity score depends on Covid-19 Case dataof 2 days before the date for which the score is observed. Hence the cases graph ie confirmed, active, death, recovered is plotted with a lag of 2 days).
