import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('./csv/train.csv')


# Select the relevant columns for the correlation analysis
features = df[['spread', 'home_id', 'home_streak', 'hgp', 'hw', 'hl',
                 'visitor_id', 'visitor_streak', 'vgp', 'vw', 'vl']]

# Compute the correlation matrix
correlation_matrix = features.corr()

# Visualize the correlation matrix using a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()