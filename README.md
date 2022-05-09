# Understanding domain shift in learned MRI reconstruction: A quantitative analysis on fastMRI knee and neuro sequences

In this work, we investigate the problem of domain shift in the context of state-of-the-art MRI reconstruction networks with respect to variations in training data. We provide visualization tools and support our findings with statistical analysis for the networks evaluated on the fastMRI knee and neuro data. We observe that the signal-to-noise ratio of the examined sequences plays an essential role, and we statistically prove the hypothesis that the type/amount of training data is less important for low acceleration factors. Finally, we provide a visualization tool facilitating the examination of the networks’ performance on each individual subject of the fastMRI data. 

## Structure
- [figures](figures/) - Directory containing all generated figures
- [resources](recources/) - Directory containing all required csv files provided by Hammernik et al.
- [plotting_utils.py](plotting_utils.py) - Script containing all key helper functions for plotting
- [statistical_analysis.py](statistical_analysis.py) - Script used for the Mann-Whitney U Test to examine the impact of variations in training data on individual networks (statistical significance)
- [plotting_networks.ipynb](plotting_networks.ipynb) - Notebook for investigations and experiments based on ranked lists
- [plotting_scatterplot.ipynb](plotting_scatterplot.ipynb) - Notebook for investigations and experiments based on scatterplots
- [box_plots.ipynb](box_plots.ipynb) - Notebook for investigations and experiments based on box plots
- [fastmri_stats.ipynb](fastmri_stats.ipynb) - Notebook for our fastMRI knee and neuro dataset exploration
- [interactive_plotting.ipynb](interactive_plotting.ipynb) - Notebook for generating the interactive subject-to-network performance visualization tool

## Citations
> [**$Σ$-net: Systematic Evaluation of Iterative Deep Neural Networks for Fast Parallel MR Image Reconstruction**](https://arxiv.org/abs/1912.09278)
> 
> Kerstin Hammernik, Jo Schlemper, Chen Qin, Jinming Duan, Ronald M. Summers, Daniel Rueckert
> 
> *[arXiv 1912.09278](https://arxiv.org/abs/1912.09278)*

> [**Systematic evaluation of iterative deep neural networks for fast parallel MRI reconstruction with sensitivity-weighted coil combination.**](https://doi.org/10.1002/mrm.28827)
> 
> Kerstin Hammernik, Jo Schlemper, Chen Qin, Jinming Duan, Ronald M. Summers, Daniel Rueckert
> 
> *[Magn Reson Med. 2021; 86: 1859– 1872](https://doi.org/10.1002/mrm.28827)*

## Acknowledgements
This work was supported by TUMKolleg, a collaborative project between the Technical University of Munich, Germany, and the grammar school Otto-von-Taube-Gymnasium Gauting, Germany.