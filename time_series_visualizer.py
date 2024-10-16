import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value']<= df['value'].quantile(0.975))
]

df.index = pd.to_datetime(df.index)

#print(df.head())

def draw_line_plot():
    fig, ax= plt.subplots(figsize=(14,4.5))
    sns.lineplot(x='date', y='value', data=df, ax=ax)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    





    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby(pd.Grouper(freq='ME')).mean()
    df_bar.reset_index(inplace=True)
    
    df_bar['Year'] = df_bar['date'].dt.year
    df_bar['Month'] = df_bar['date'].dt.month_name()
    df_bar['Month_Num'] = df_bar['date'].dt.month
    
    df_bar.sort_values(by=['Year', 'Month_Num'], inplace=True)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
               'August', 'September', 'October', 'November', 'December']
    df_bar['Month'] = pd.Categorical(df_bar['Month'], categories=month_order, ordered=True)

    # Draw bar plot
    fig, ax= plt.subplots(figsize=(10,6))
    df_bar.groupby(['Year', 'Month'])['value'].mean().unstack().plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')
    




    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2)=plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1, palette='pastel')
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, palette='pastel')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
      
    plt.tight_layout()
    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
