import math
import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import statsmodels.formula.api as smf
from adjustText import adjust_text

matplotlib.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 12,
        "pgf.rcfonts": False,
        "axes.unicode_minus": False,
        "axes.titlesize":14,
        "axes.labelsize":14,
        "xtick.labelsize":10,
        "ytick.labelsize":10,
        "figure.dpi":200,
        "savefig.dpi":300,
        "figure.figsize":(8,6),
        "lines.linewidth":1.5
    }
)

def weekdaywiseplot(df, x, y, xlabel, ylabel, title):
    df['interval'] = "AM Peak"
    df.loc[(df['pickup_hour']>6) & (df['pickup_hour']<13), 'interval'] = "Mid-day"
    df.loc[(df['pickup_hour']>=13) & (df['pickup_hour']<=18), 'interval'] = "PM Peak"
    df.loc[(df['pickup_hour']>18) | (df['pickup_hour']<4), 'interval'] = "Night"
    colors = {'Night':'blue', 'AM Peak':'orange', 'Mid-day':'green', 'PM Peak':'red'}
#     colors = {'Night':'#0077BB', 'AM Peak':'#DDAA33', 'Mid-day':'#BBCC33', 'PM Peak':'#CC3311'}
    df['colors'] = df['interval'].map(colors)
    figure, axes = plt.subplots(4,2, sharex=True, sharey=True, figsize=(10, 8))
    # figure.delaxes(axes[3,1])
    axes[3,1].axis('off')
    axes[2,1].xaxis.set_tick_params(labelbottom=True)
    j=1
    for day in range(7):
        df1 = df[df['pickup_day'] == day]
        colors = cm.rainbow(np.linspace(0, 1, len(df1['pickup_hour'])))
        # because there are 52 weeks in a year, so divided the volume columns by 52
        ax_x,ax_y = math.floor((j-1)/2),j%2 -1
        texts = []
        for i, txt in enumerate(df1['pickup_hour']):
            axes[ax_x,ax_y].scatter(df1.iloc[i][x], df1.iloc[i][y],s = df1.iloc[i]['d or n'], color = df1.iloc[i]['colors'], edgecolors='black', linewidths=0.5)
            # axes[ax_x,ax_y].annotate((txt+3 if txt<=20 else txt-21), (df1.iloc[i][x], df1.iloc[i][y]),fontsize=10) # +np.random.choice([-0.02,0.02])
            texts.append(axes[ax_x,ax_y].text(x = df1.iloc[i][x], y = df1.iloc[i][y], s = (txt+3 if txt<=20 else txt-21), fontsize=8) )
        adjust_text(texts, only_move={'points':'y', 'texts':'xy'}, force_text=0.25, force_points=0.25, ax = axes[ax_x,ax_y],arrowprops=dict(arrowstyle='-', color='black', alpha=.5))
        axes[ax_x,ax_y].plot(df1[x], df1[y], '0.8')
        axes[ax_x,ax_y].set_title(df1.iloc[0]['weekday'], fontsize=12)
        j=j+1
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Night',markerfacecolor='blue', markersize=8, markeredgecolor='black', markeredgewidth=0.5),
                       Line2D([0], [0], marker='o', color='w', label='AM Peak',markerfacecolor='orange', markersize=12, markeredgecolor='black', markeredgewidth=0.5),
                       Line2D([0], [0], marker='o', color='w', label='Mid-day',markerfacecolor='green', markersize=12, markeredgecolor='black', markeredgewidth=0.5),
                       Line2D([0], [0], marker='o', color='w', label='PM Peak',markerfacecolor='red', markersize=12, markeredgecolor='black', markeredgewidth=0.5)]
    axes[3,1].legend(handles=legend_elements,loc='center', prop={'size': 12}, fontsize=12)
    figure.suptitle(title)
    figure.supxlabel(xlabel)
    figure.supylabel(ylabel)
    figure.tight_layout()

def periodplot_agg(df, x, y, xlabel, ylabel, title,r_type):
    """
    This is a Python function that creates a period plot with different transformations of the x-axis
    and fits a regression line based on the chosen transformation type.
    
    Args:
      df: The input dataframe
      x: The name of the column in the dataframe that will be used as the independent variable for the
    plot.
      y: The dependent variable in the regression model.
      xlabel: The label for the x-axis of the plot.
      ylabel: The label for the y-axis of the plot.
      title: The title of the plot
      r_type: The type of regression to perform on the data. It can be "reciprocal", "linear", "sqrt",
    "log", or "reciprocal_offset".
    """
    figure, axes = plt.subplots()
    df1 = df.copy()
    x1=df1[x]
    df1['reciprocal'] = 1/df1[x]
    df1['sqrt'] = np.sqrt(df1[x])
    df1['logx'] = np.log10(df1[x]-min(df1[x])+0.01)
    df1['logy'] = np.log10(df1[y])
    df1['reciprocal_offset'] = 1/(df1[x]-min(df1[x])+0.01)
    if r_type == "reciprocal":
        results = smf.ols(y+' ~ reciprocal', data=df1).fit()
        print(results.mse_resid)
        axes.scatter(df1[x], df1[y], alpha=0.2)
        x_range = np.linspace(math.floor(min(x1)), math.ceil(max(x1)), num=20)
        x_trans_range = 1/x_range
        axes.plot(x_range, results.params[1]*x_trans_range+results.params[0], c='black', linewidth=3.0, linestyle='dashed')
    elif r_type == "linear":
        results = smf.ols(y+' ~ '+x, data=df1).fit()
        print(results.mse_resid)
        axes.scatter(df1[x], df1[y], alpha=0.2)
        x_range = np.linspace(math.floor(min(x1)), math.ceil(max(x1)), num=20)
        axes.plot(x_range, results.params[1]*x_range+results.params[0], c='black', linewidth=3.0, linestyle='dashed')
    elif r_type == "sqrt":
        results = smf.ols(y+' ~ sqrt', data=df1).fit()
        print(results.mse_resid)
        axes.scatter(df1[x], df1[y], alpha=0.2)
        x_range = np.linspace(math.floor(min(x1)), math.ceil(max(x1)), num=20)
        x_trans_range = np.sqrt(x_range)
        axes.plot(x_range, results.params[1]*x_trans_range+results.params[0], c='black', linewidth=3.0, linestyle='dashed')
    elif r_type == "log":
        results = smf.ols('logy ~ logx', data=df1).fit()
        print(results.mse_resid)
        axes.scatter(df1[x], df1[y], alpha=0.2)
        x_range = np.linspace(math.floor(min(x1)), math.ceil(max(x1)), num=20)
        x_trans_range = np.log10(x_range-math.floor(min(x1))+0.01)
        axes.plot(x_range, 10**(results.params[1]*x_trans_range+results.params[0]), c='black', linewidth=3.0, linestyle='dashed')
    elif r_type == "reciprocal_offset":
        results = smf.ols(y+' ~ reciprocal_offset', data=df1).fit()
        print(results.mse_resid)
        print(results.params)
        axes.scatter(df1[x], df1[y], alpha=0.2)
        x_range = np.linspace(math.floor(min(x1)), math.ceil(max(x1)), num=20)
        x_trans_range = 1/(x_range-min(x1)+0.01)
        axes.plot(x_range, results.params[1]*x_trans_range+results.params[0], c='black', linewidth=3.0, linestyle='dashed')
    else:
        axes.scatter(df1[x], df1[y], alpha=0.2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    # plt.legend(loc="lower right",  prop={'size': 12})
    
def periodplot_disagg(df, x, y, xlabel, ylabel, title):
    """
    This function creates a scatter plot with a regression line for different time intervals and
    calculates the mean squared error and parameters of the regression model.
    
    Args:
      df: The input dataframe containing the data to be plotted.
      x: The independent variable to be plotted on the x-axis.
      y: The dependent variable in the regression model.
      xlabel: The label for the x-axis of the plot.
      ylabel: The label for the y-axis of the plot.
      title: The title of the plot
    """
    df['interval'] = "AM Peak"
    df.loc[(df['pickup_hour']>6) & (df['pickup_hour']<13), 'interval'] = "Mid-day"
    df.loc[(df['pickup_hour']>=13) & (df['pickup_hour']<=18), 'interval'] = "PM Peak"
    df.loc[(df['pickup_hour']>18) | (df['pickup_hour']<4), 'interval'] = "Night"
    df1 = df.copy()
    df1['interval_cat']=0
    df1.loc[(df1['pickup_hour']>6) & (df1['pickup_hour']<13), 'interval_cat']=1
    df1.loc[(df1['pickup_hour']>=13) & (df1['pickup_hour']<=18), 'interval_cat']=2
    df1.loc[(df1['pickup_hour']>18) | (df1['pickup_hour']<4), 'interval_cat']=3
    df1['sqrt'] = np.sqrt(df1[x])
    results = smf.ols(y+" ~ sqrt + C(interval, Treatment('Night'))", data=df1).fit()
    print(results.mse_resid)
    print(results.params)
    colors = {'Night':'blue', 'AM Peak':'orange', 'Mid-day':'green', 'PM Peak':'red'}
    symbols = {'Night':'o', 'AM Peak':'^', 'Mid-day':'s', 'PM Peak':'D'}
    df1['colors'] = df1['interval'].map(colors)
    df1['markers'] = df1['interval'].map(symbols)
    figure, axes = plt.subplots()
    for interval in df1['interval'].unique():
        df2 = df1[df1['interval'] == interval]
        axes.scatter(df2[x], df2[y], color=df2['colors'].iloc[0], marker = df2['markers'].iloc[0], alpha=0.2, label = df2['interval'].iloc[0])
        x1=df2[x]
        x_range = np.linspace(math.floor(min(x1)), math.ceil(max(x1)), num=20)
        x_trans_range = np.sqrt(x_range)
        if interval == "Night":
            aa = results.params[0]
        elif interval == "AM Peak":
            aa = results.params[0]+results.params[1]
        elif interval == "Mid-day":
            aa = results.params[0]+results.params[2]
        else:
            aa = results.params[0]+results.params[3]
        axes.plot(x_range, results.params[4]*x_trans_range+aa,
                  c=df2['colors'].iloc[0], linewidth=5.0, linestyle='dashed')
    plt.title(title)
    plt.legend(loc="lower right",  prop={'size': 12})
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
       
def plot_willingness_to_share(df, title):
    """
    This function plots the willingness-to-share against the average number of trips for a given dataset
    and title.
    
    Args:
      df: a pandas DataFrame containing the data to be plotted
      title: The title of the plot.
    """
    x = 'count_total'
    y = 'requested_per'
    xlabel = r"Average number of trips $n^a_n(h,d)$"
    ylabel = r"Willingness-to-share $\theta_{s_a,n}(h,d)$"
    weekdaywiseplot(df, x, y, xlabel, ylabel, title)

def plot_match_rate(df, title, fit , disaggregate = False):
    """
    This function plots a match rate against the number of authorized shared trips, with the option to
    disaggregate the data.
    
    Args:
      df: a pandas DataFrame containing the data to be plotted
      title: The title of the plot.
      fit: a boolean variable indicating whether to fit a linear regression line to the plot or not. If
    fit is True, a regression line will be added to the plot. If fit is False, no regression line will
    be added.
      disaggregate: A boolean parameter that determines whether to plot the data disaggregated by a
    certain variable or not. If set to True, the function will call the periodplot_disagg() function to
    plot the data disaggregated by a certain variable. If set to False, the function will call the
    periodplot_agg(). Defaults to False
    """
    x = 'count_shared_requested_mean'
    y = 'matched_percent'
    xlabel = r"Number of authorized shared trips $n_{s_a,n}^a(h,d,m)$"
    ylabel = r'Matched percentage $\theta_{s_m,n}(h,d,m)$'
    if not disaggregate:
        periodplot_agg(df, x, y, xlabel, ylabel, title, fit)
    else:
        periodplot_disagg(df, x, y, xlabel, ylabel, title)

def plot_unit_fare_ratio(df, title, fit, disaggregate = False):
    """
    This function plots the unit fare ratio against the total number of trips, with the option to
    disaggregate the data.
    
    Args:
      df: a pandas DataFrame containing the data to be plotted
      title: The title of the plot. It is a string.
      fit: a boolean variable indicating whether to fit a linear regression line to the plot or not. If
    fit is True, a regression line will be plotted. If fit is False, no regression line will be plotted.
      disaggregate: A boolean parameter that determines whether the plot should be disaggregated or not.
    If set to True, the plot will show data for each individual category in the dataset. If set to
    False, the plot will show aggregated data for the entire dataset. Defaults to False
    """
    x = 'count_mean_total'
    y = 'cost_ratio_mile'
    xlabel = r'Total number of trips $n^a(h,d,m)$'
    ylabel = r'Unit fare ratio $e^d(h,d,m)$'
    if not disaggregate:
        periodplot_agg(df, x, y, xlabel, ylabel, title, fit)
    else:
        periodplot_disagg(df, x, y, xlabel, ylabel, title)
   
