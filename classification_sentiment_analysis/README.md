The datasets folder mentioned in the notebooks include the files that were used in both the iterations of Self Training (BERT) 
The files of the datasets folder mentioned in the notebooks are available at the following Google Drive link: https://drive.google.com/drive/folders/1Ge7aZGWHzyT1jCjsZWo6XcjwwboIXnDg?usp=sharing

The preprocessor and the trained models of both Self Training iterations are available at the drive link: https://drive.google.com/drive/folders/1h9VpYDXO2r8i7RXYdtg1FWXMHDcEiLpU?usp=sharing

The files of the prediction folder which includes all tweets, cleaned tweets to label and labelled tweets using the final model are available at the drive link: https://drive.google.com/drive/folders/1vUjS9pI7s9QhNYXhN6X3Z0R1r7gKcQqu?usp=sharing

Labelling sentiments to tweets is done in 3 ways:
1. Multiclass emotion classification (anger, fear, joy, sadness, neutral) using BERT and self-training -
Semi-supervised Self Training is applied in 2 iterations.
Steps are as follows:
step 1. Generation of an initial labelled dataset using [], [] and 1500 manually labelled neutral tweets from the collected tweet set. (Train: Test ratio 75:25)
step 2. Fine-tuning BERT in 3 iterations to obtain first self-training iteration accuracy of 83.92% on the test set.
step 3. Using the first iteration trained BERT model to label tweets of Covid-19.
step 4. Filtering tweets having label confidence > 95%
step 5. Generation of second iteration dataset
Train set: 3000 labelled tweets for each class, 1000 labelled texts from the dataset of iteration 1 for each class
Total train set size: 20,000
Test set: 1000 labelled tweets for each class, 500 labelled texts from the dataset of iteration 1 for each class
Total test set size: 7500
step 6. Fine-tuning BERT in 3 iterations to obtain second self-training iteration accuracy of 93.38% on the test set.
step 7. Using trained BERT to label all tweets.
 
2. Positive, Negative and Neutral classification -
This classification was performed using Vader []. The compound score was obtained for 		individual tweets and the compound scores were converted to labels 0 (Neutral), 1 		(Positive) and -1 (Negative) using the threshold values []:
Positive sentiment: compound score >= 0.05
Neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
Negative sentiment: compound score <= -0.05
 
3. Positivity Score -
Positivity score is the compound score assigned to individual tweets using Vader []. The 		score is calculated for 1 day time period from 1st Feb 2020 to 30th April 2020. The 		positivity score for 1 day is obtained using the formula:
Positivity score = Total score of individual tweets / Count of tweets
The score indicates the positivity of people on that day. A higher score indicates high 		positivity. The score can also be negative indicating negative sentiment.
Results on analysis are then plotted using different visualisations.
 



