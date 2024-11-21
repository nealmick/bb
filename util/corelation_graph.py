import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('./csv/train.csv')

# Define the list of input features
input_features = ['spread','home_streak','hw','hl','visitor_streak','vw','vl']
labels = ['fg3_pct']
for currentPlayer in range(0,1):
    derp = ['home_', 'visitor_']
    for foo in derp:#home vistor
            for label in labels:
                stat = foo+str(currentPlayer)+'_'+label#make lables
                input_features.append(stat)
# Extract the home and visitor game scores into separate Series
home_score = df['home_score']
visitor_score = df['visitor_score']

# Calculate the correlation between each feature and the home and visitor game scores
correlation_home = df[input_features].corrwith(home_score)
correlation_visitor = df[input_features].corrwith(visitor_score)

# Concatenate the correlation values for both home and visitor scores
correlation_combined = pd.concat([correlation_home, correlation_visitor], axis=1)
correlation_combined.columns = ['Home Score Correlation', 'Visitor Score Correlation']

# Sort the correlation values in descending order and select the top 10 features
top_10_features = correlation_combined.nlargest(10, ['Home Score Correlation', 'Visitor Score Correlation'])

# Create a bar chart to visualize the correlations
top_10_features.plot(kind='bar', figsize=(12, 6))
plt.xlabel('Features')
plt.ylabel('Correlation')
plt.title('Feature Correlation')
plt.legend(loc='lower right')
plt.xticks(rotation=45, ha='right')

# Adjust the layout to prevent label cutoff
plt.tight_layout()
plt.show()
