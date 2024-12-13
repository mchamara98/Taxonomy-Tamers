#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# Load datasets
import pandas as pd

# Define file paths directly, assuming the paths are correct
merged_data_path = ('/Users/shreyagowrishetty/Documents/merged data.xlsx')


# Read in the CSV files
merged_df = pd.read_excel(merged_data_path)
merged_df.head()


# In[3]:


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# In[11]:


# Bar Chart: Data Quality vs Algorithm Function with Annotated Labels
plt.figure(figsize=(14, 7))
ax = sns.countplot(data=merged_df, x='Data Quality', hue='Algorithm Function_x', palette='cool')

# Add annotated labels (count values) above each bar
for p in ax.patches:
    # Get the height of each bar (the count)
    height = p.get_height()
    
    # Annotate the value at the top of each bar
    ax.annotate(
        f'{height:.0f}',  # Display the count value (rounded to integer)
        (p.get_x() + p.get_width() / 2., height),  # Position of the label
        ha='center',  # Horizontal alignment
        va='bottom',  # Vertical alignment, adjust to be just above the bar
        fontsize=10,  # Font size for the value
        color='black',  # Text color
        xytext=(0, 5),  # Slightly offset the text above the bar
        textcoords='offset points'  # Text offset in points
    )

plt.title('Data Quality by Algorithm Function', fontsize=16)
plt.xlabel('Data Quality', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.legend(title='Algorithm Function', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.show()



# In[12]:


# Horizontal Bar Chart: Algorithm Count by Data Format with Annotated Labels
plt.figure(figsize=(10, 6))
data_format_counts = merged_df['Data Format'].value_counts()
ax = data_format_counts.plot(kind='barh', color=sns.color_palette('viridis'))

# Add annotated labels (count values) to each bar
for index, value in enumerate(data_format_counts):
    plt.text(value, index, f'{value}', va='center', ha='right', fontsize=10, color='white')

plt.title('Algorithm Count by Data Format', fontsize=16)
plt.xlabel('Count', fontsize=12)
plt.ylabel('Data Format', fontsize=12)
plt.show()


# In[6]:


# Pie Chart: Job Zone Distribution
job_zone_counts = merged_df['Job Zone'].value_counts()
plt.figure(figsize=(8, 8))
job_zone_counts.plot.pie(autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Job Zone Distribution', fontsize=16)
plt.ylabel('')  # Remove y-axis label for clarity
plt.show()


# In[14]:


# Bar Chart: Average Max Observations by Data Type with Annotated Labels and Color Highlight for Lowest Value
avg_observations = merged_df.groupby('Data Type')['Max Observations on One CPU'].mean().sort_values()

plt.figure(figsize=(10, 6))

# Create color palette and assign color based on value
colors = sns.color_palette('cubehelix', len(avg_observations))

# Highlight the lowest value with a different color (e.g., red)
lowest_value_index = avg_observations.idxmin()
colors = [
    'red' if index == lowest_value_index else color 
    for index, color in zip(avg_observations.index, colors)
]

ax = avg_observations.plot(kind='bar', color=colors)

# Add annotated labels (average values) above each bar
for p in ax.patches:
    height = p.get_height()
    ax.annotate(
        f'{height:.2f}',  # Display the average value with 2 decimal places
        (p.get_x() + p.get_width() / 2., height),  # Position of the label
        ha='center',  # Horizontal alignment
        va='bottom',  # Vertical alignment, just above the bar
        fontsize=10,  # Font size for the value
        color='black',  # Text color
        xytext=(0, 5),  # Slightly offset the text above the bar
        textcoords='offset points'  # Text offset in points
    )

plt.title('Average Max Observations on One CPU by Data Type', fontsize=16)
plt.xlabel('Data Type', fontsize=12)
plt.ylabel('Average Max Observations', fontsize=12)
plt.xticks(rotation=45)
plt.show()



# In[10]:


pip install wordcloud


# In[11]:


from wordcloud import WordCloud


# In[12]:


# Generate Word Cloud for Algorithm Function
text = ' '.join(merged_df['Algorithm Function_x'])
wordcloud = WordCloud(background_color='white', colormap='viridis', width=800, height=400).generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Algorithm Functions', fontsize=16)
plt.show()


# In[37]:


# After cleaning columns, proceed with the correlation matrix
numeric_columns = merged_df.select_dtypes(include=['number']).columns  # Adjusted for cleaned names

corr_matrix = merged_df[numeric_columns].corr()

plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap')
plt.show()



# In[18]:


# Stacked Bar Chart: Human in the Loop by Algorithm Function with Distinct Colors
plt.figure(figsize=(14, 7))

# Create a crosstab of the Human-In-The-Loop and Algorithm Function_x columns
crosstab_data = pd.crosstab(merged_df['Human-In-The-Loop'], merged_df['Algorithm Function_x'])

# Generate distinct colors for each Algorithm Function using a color palette
colors = sns.color_palette('tab20', n_colors=len(merged_df['Algorithm Function_x'].unique()))

# Plot the stacked bar chart
crosstab_data.plot(kind='bar', stacked=True, color=colors)

# Title and labels
plt.title('Human in the Loop by Algorithm Function', fontsize=16)
plt.xlabel('Human in the Loop', fontsize=12)
plt.ylabel('Count', fontsize=12)

# Display the legend outside the plot for clarity
plt.legend(title='Algorithm Function', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot with no x-axis label rotation
plt.xticks(rotation=0)

plt.show()



# In[ ]:




