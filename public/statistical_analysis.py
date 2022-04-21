import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt

# evaluation dataset
anatomy = 'knee'
# acceleration factor
Reval = 4
print(Reval)
acq = 'CORPDFS_FBK'
print(acq)

df = pd.read_csv(f'./resources/{anatomy}/eval_{anatomy}_R{Reval}.csv')

# trained networks
networks = df['network'].unique()
#eval_network = 'PM-DUNET'
eval_network = 'UNET'
# eval_network = 'VN'
print(eval_network)

# training datasets
training_anatomy = df['anatomy'].unique()
ref_training_anatomy = 'knee 100'

print(networks)
print(training_anatomy)

# evaluation metric: ['SSIM', 'PSNR', 'NMSE'] we stick to SSIM
metric = 'SSIM'
print(df['acquisition'].unique())
# filter dataframe
def get_dataframe(anatomy, network):
    df_ref = df[df['anatomy'] == anatomy]
    df_ref = df_ref[df_ref['network'] == network]
    df_ref = df_ref[df_ref['acquisition'] == acq]
    return df_ref

# we want to perform a statistical analysis for each network in 'networks'
# if anatomy = 'knee', our reference ref_training_anatomy is 'knee 100'
df_ref = get_dataframe(ref_training_anatomy, eval_network)
print('Nr samples in df_ref:', len(df_ref))
metric_ref = df_ref[metric]

"""
    Which test to use?
    1. question: dependent or independent samples?
        -> dependent: samples are paired or related (e.g., different algorithms on same data, or same data evaluated with different algorithms) 
            Research questions: focused on the paired samples; is one algorithm better? Is a specific therapy successfull?
        -> independent: samples are unrelated
            Research question: do the samples follow the same distribution?
    
        Dependent/Paired samples:
            We want to test if the difference between two samples is 0, >0, or <0.
            Two tests can be used:  
                - Parametric test: T-test for related samples (stats.ttest_rel) for normally distributed data 
                - Nonparametric test: Wilcoxon Signed-Rank test (stats.wilcoxon) when we don't know the distribution
        Independent samples:
            We want to test if two samples are equally distributed or not. 
            Two tests can be used:  
                - Parametric test: T-test for independent samples (stats.ttest_ind) for normally distributed data 
                - Nonparametric test: Mann-Whiteney-U test (stats.mannwhitneyu) when we don't know the distribution

    2. question: Are our samples normally distributed?
        We can use parametric test like the t-test, if we know that our samples are normally distributed. 
        If we know that they are not normally distributed, or if we don't want to make any assumption about 
        the data distribution, we use nonparametric test.

        We can test for normality using, e.g. the Shapiro-Wilk, which tests the null hypothesis that the data was drawn from a normal distribution (stat.shapiro).

    We are more interested if the samples are equally distributed. We don't care about the difference between paired samples. 
    Our data is not normally distributed (see output of Shapiro test and histogram plot)

    -> We use the Mann-Whitney-U test!

"""
# test if the sample is normally distributed:
print()
print('TEST FOR NORMALITY:')
alpha = 0.05
stat, p = stats.shapiro(metric_ref)
print('Statistics=%.4f, p=%.4f' % (stat, p))
print(f'{p} < {alpha}:')
print('Sample does not look Gaussian (reject H0) => Wilcoxon Signed-Rank test')
print()

# visual: does the sample follow a normal distribution? No!
plt.hist(metric_ref)
plt.show()

for tai, ta in enumerate(training_anatomy):
    if ta != ref_training_anatomy:

        # if not tai ==1:
        #     continue
        print(f'Test `{ref_training_anatomy}` against `{ta}`')
        df_compare = get_dataframe(ta, eval_network)
        metric_compare = df_compare[metric]

        print('  Nr samples in df_ref:', len(df_compare))

        # metric_ref contains the samples for the 'reference'
        # metric_compare contains the samples for the other cases we want to compare to.

        # test for normal distribution
        print()
        stat, p = stats.shapiro(metric_compare)
        # print('Statistics (Shapiro)=%.4f, p=%.4f' % (stat, p))
        # print()

        """
            H0: no difference between x (here: metric_ref) and y (here: metric_compare): x-y = 0
            H1: alternative hypothesis
                - alternative='two-sided':  x-y != 0
                - alternative='greater':    x-y > 0
                - alternative='less':       x-y < 0
        """
        alter = 'two-sided'
        # print(np.asarray(metric_ref) - np.asarray(metric_compare))
        diffnorm = np.linalg.norm(abs(np.asarray(metric_ref) - np.asarray(metric_compare)))
        print('Norm of difference: {:1.3f}'.format(diffnorm))

        # # Wilcoxon test
        # w, p = stats.wilcoxon(metric_ref, metric_compare, alternative=alter) 
        # print(w, p)
        # Wilcoxon test
        w, p = stats.mannwhitneyu(metric_ref, metric_compare, alternative=alter) 
        print(w, p)

        # T-test 
        # t, p = stats.ttest_rel(metric_ref, metric_compare, alternative=alter)
        # print(t, p)
        
        if p<alpha:
            print('Significant!')
        else:
            print('Not significant!')

        if p < 0.001:
            print('p < 0.001:', p<0.001)
        elif p<0.01:
            print('p < 0.01:', p<0.01)
        elif p<0.05:
            print('p < 0.05:', p<0.05)
        print()

"""
import pandas as pd

# evaluation dataset
anatomy = 'knee'
# acceleration factor
Reval = 4*

df = pd.read_csv(f'./resources/{anatomy}/eval_{anatomy}_R{Reval}.csv')

# trained networks
networks = df['network'].unique()
eval_network = 'PM-DUNET'

# training datasets
training_anatomy = df['anatomy'].unique()
ref_training_anatomy = 'knee 100'

# evaluation metric: ['SSIM', 'PSNR', 'NMSE'] we stick to SSIM
metric = 'SSIM'

# filter dataframe
def get_dataframe(anatomy, network):
    df_ref = df[df['anatomy'] == anatomy]
    df_ref = df_ref[df_ref['network'] == network]
    return df_ref

# we want to perform a statistical analysis for each network in 'networks'
# if anatomy = 'knee', our reference ref_training_anatomy is 'knee 100'
df_ref = get_dataframe(ref_training_anatomy, eval_network)
print('Nr samples in df_ref:', len(df_ref))
#metric_ref = df_ref[metric]
metric_ref = df_ref[['filename', metric]].reset_index(drop=True)
metric_ref.rename(columns={metric: f'{metric} {anatomy}'}, inplace=True)

for ta in training_anatomy:
    if ta != ref_training_anatomy:
        print(f'Test `{ref_training_anatomy}` against `{ta}`')
        df_compare = get_dataframe(ta, eval_network)
        metric_compare = df_compare[[metric]].reset_index(drop=True)
        metric_compare.rename(columns={metric: f'{metric}_{ta}'}, inplace=True)
        #metric_compare = df_compare[['filename', metric]]

        combined = pd.concat([metric_ref, metric_compare], axis=1)
        print('  Nr samples in df_ref:', len(df_compare))

        #TODO analysis - paired t-test
        # metric_ref contains the samples for the 'reference'
        # metric_compare contains the samples for the other cases we want to compare to.

print(combined)

#print(metric_ref)
"""     
