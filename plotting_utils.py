import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd

def get_plotting_info(anatomy, Reval):
    # Paper figure ids
    if Reval == 4 and anatomy == 'knee':
        figid = 'figure2'
    elif Reval == 8 and anatomy == 'knee':
        figid = 'figure3'
    elif Reval == 4 and anatomy == 'brain':
        figid = 'figure4'
    elif Reval == 8 and anatomy == 'brain':
        figid = 'figure5'

    if anatomy == 'brain':
        title = f'Neuro R={Reval}'
    else:
        title = f'Knee R={Reval}'

    if anatomy == 'brain':
        upper = 0.97 if Reval==8 else 0.99
        lower = 0.82 if Reval==8 else 0.89
    else: # To-be-updated
        upper = 0.97 if Reval==8 else 0.99
        lower = 0.82 if Reval==8 else 0.86

    return figid, title, (lower, upper)

def get_color(elems):
    cmap = plt.cm.tab20c
    color = []
    for elem in elems:
        if 'knee 25' in elem:
            color.append(cmap((2*4+2)/20))
        elif 'knee 50' in elem:
            color.append(cmap((2*4+1)/20))
        elif 'knee' in elem:
            color.append(cmap(2*4/20))
        elif 'neuro' in elem:
            color.append(cmap(1/5))
        elif 'joint 25 uni' in elem:
            color.append(cmap((2)/20))
        elif 'joint 50 uni' in elem:
            color.append(cmap((1)/20))
        elif 'joint 100 uni' in elem:
            color.append(cmap((0)/20))
        elif 'joint 25' in elem:
            color.append(cmap((3*4+2)/20))
        elif 'joint 50' in elem:
            color.append(cmap((3*4+1)/20))
        elif 'joint 100' in elem:
            color.append(cmap((3*4+0)/20))
        else:
            color.append(cmap(3/5))
    return color

def get_legend(eval_dset, disp_dset):
    legend_elements = []
    color = get_color(eval_dset)
    for c, l in zip(color, disp_dset):
        legend_elements.append(Patch(facecolor=c, label=l))
    return legend_elements

def get_plotting_data(df, network_keys, anatomy_keys, eval_metric):
    df_final = None
    cols = ['network', 'dset', eval_metric, eval_metric+'_std']
    for nkey in network_keys:
        for ecol in anatomy_keys:
            df_eval = df[df['network']==nkey]
            row = [f'{nkey.ljust(10)}', f'{ecol.ljust(14)}']
            count = df_eval[df_eval['anatomy']==ecol].count()[eval_metric]
            metric_mean = df_eval[df_eval['anatomy']==ecol].mean()[eval_metric]
            metric_std = df_eval[df_eval['anatomy']==ecol].std()[eval_metric]
            row.append(metric_mean)
            row.append(metric_std)

            df_eval = pd.DataFrame([row], columns=cols)
            df_final = pd.concat([df_final, df_eval], ignore_index=True)

            x = df_final.set_index('network')[eval_metric].sort_values(ascending=True)
            y = df_final.set_index('dset')[eval_metric].sort_values(ascending=True)
    return x, y