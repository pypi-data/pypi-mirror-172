"""

Libraries

"""

import sys, os
sys.path.insert(0, os.getcwd())
from precipitation.libraries import *

"""

Methods

"""

def weibull_distribution(data):
    """ Find Weibull's distribution frequencies for data from a numpy.array.
    """
    data = data[~np.isnan(data)]
    data = np.flip(np.sort(data))
    rank = np.array([i for i in range(1, data.shape[0] + 1)])
    prob = rank / (data.shape[0] + 1)
    return data, 1 / prob

def chi2(obs, cdf, n_params):
    """ Chi Square Goodness of Fit test. "obs" and "est" are the observed and estimated values.
    It returns the statistic and the p-value of the test.
    "obs" and "est" must be numpy.array both.
    """
    if len(obs) < 20:
        return np.nan
    elif len(obs) < 50:
        n_min = 5
        n_ = 10
    elif len(obs) < 100:
        n_min = 10
        n_ = 20
    else:
        n_min = np.floor(obs.shape[0] ** 2)
        n_ = np.ceil(obs.shape[0] / 5)
    f_obs = np.histogram(obs, bins=n_, range=(np.min(obs, axis=0) * 0.99, np.max(obs, axis=0) * 1.01))
    f_est = np.array(
        [cdf([f_obs[1][1]])[0]] + \
        [cdf([f_obs[1][i+1]])[0] - cdf([f_obs[1][i]])[0] for i in range(1, f_obs[0].shape[0] - 1)] + \
        [1 - cdf([f_obs[1][-2]])[0]]
    )
    while np.any(f_est == 0) and n_ > n_min:
        n_    = n_ - 1
        f_obs = np.histogram(obs, bins=n_, range=(np.min(obs, axis=0) * 0.99, np.max(obs, axis=0) * 1.01))
        f_est = np.array(
            [cdf([f_obs[1][1]])[0]] + \
            [cdf([f_obs[1][i+1]])[0] - cdf([f_obs[1][i]])[0] for i in range(1, f_obs[0].shape[0] - 1)] + \
            [1 - cdf([f_obs[1][-2]])[0]]
        )
    return sp.chisquare(f_obs[0], f_est * len(obs), ddof=n_params)[1]

def standard_error(obs, est, n_params=0):
    """ Return the Standard Error between "obs" and "est", which are the observed and estimated data.
    """
    return np.sum((np.sort(obs) - np.sort(est)) ** 2 / (obs.shape[0] - n_params)) ** 0.5

def percentage_error(obs, est, _abs=True):
    """ Return the Percentage Error between "obs" and "est", which are the observed and estimated data.
    """
    if _abs:
        return 100 * np.abs((est - obs) / obs)
    elif ~_abs:
        return 100 * (est - obs) / obs
    else:
        raise ValueError('"_abs" must be True or False.')

def FACETA_excel(file):
    print(f'--------------- {file} ---------------')
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    time = np.array([col for col in ws.iter_cols(min_row=2, max_col=1, values_only=True)])[0]
    data = np.array([col for col in ws.iter_cols(min_row=2, min_col=2, max_col=2, values_only=True)])[0]
    tests = Precipitation_test(data)
    sorted_data, return_period = weibull_distribution(data)
    lnmv = LogNormal_MV(data)
    gumm = Gumbel_MM(data)
    gumv = Gumbel_MV(data)
    gemm = GEV_MM(data)
    gemv = GEV_MV(data)
    lpmm = LogPearson3_MM(data)
    print(
        '\nOutliers -----------------------------', tests.outliers[~np.isnan(tests.outliers)].shape[0],
        '\nIndependence Anderson ----------------', tests.independence_a[1],
        '\nIndependence Wald Wolfowitz ----------', tests.independence_ww[1],
        '\nTrend Mann Kendall ------------------- 95%', tests.trend_mk[4], '99%', tests.trend_mk[5],
        '\nSigned Rank Wilcoxon (Homogeneity) ---', tests.signed_rank_w[1],
        '\nHomogeneity Pettitt ------------------', tests.homogeneity_p[0],
    )
    print(
        '\nMean ---------------------', np.nanmean(data, axis=0),
        '\nStandard Deviation -------', np.nanstd(data, axis=0),
        '\nMin ----------------------', np.nanmin(data, axis=0),
        '\nMax ----------------------', np.nanmax(data, axis=0),
        '\nq 10% --------------------', np.nanquantile(data, 0.10, axis=0),
        '\nq 25% --------------------', np.nanquantile(data, 0.25, axis=0),
        '\nMedian -------------------', np.nanquantile(data, 0.50, axis=0),
        '\nq 75% --------------------', np.nanquantile(data, 0.75, axis=0),
        '\nq 90% --------------------', np.nanquantile(data, 0.90, axis=0),
        '\nq 99% --------------------', np.nanquantile(data, 0.99, axis=0),
    )
    print(
        '\nLogNormal MV -------------', lnmv.goodness_fit,
        '\nGumbel MM ----------------', gumm.goodness_fit,
        '\nGumbel MV ----------------', gumv.goodness_fit,
        '\nGEV MM -------------------', gemm.goodness_fit,
        '\nGEV MV -------------------', gemv.goodness_fit,
        '\nLogPearson Type III MM ---', lpmm.goodness_fit,
    )
    T = [1.01, 2, 5, 10, 25, 50, 100]
    fig = plt.figure(figsize=(8,5), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(return_period, sorted_data, label='Weibull')
    ax.plot(T, lnmv.ppf(T)[0], c='Black', lw=0.5, ls='--')
    ax.plot(T, lnmv.ppf(T)[1], label='LogNormal MV', c='Black')
    ax.plot(T, lnmv.ppf(T)[2], c='Black', lw=0.5, ls='--')
    ax.plot(T, gumm.ppf(T)[1], label='Gumbel MM', c='Blue')
    ax.plot(T, gumv.ppf(T)[1], label='Gumbel MV', c='Red')
    ax.plot(T, gemm.ppf(T)[1], label='GEV MM', c='Orange')
    ax.plot(T, gemv.ppf(T)[1], label='GEV MV', c='Yellow')
    ax.plot(T, lpmm.ppf(T)[1], label='LogPearson Type III MM', c='LightGreen')
    ax.set(xlabel='Precipitation (mm)', ylabel='Return Period (years)')
    plt.legend()
    plt.show()
    name = file[:file.index('.')]
    with open(f'{name}.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['Return Period (years)', 'LogNormal MV', 'Gumbel MM', 'Gumbel MV', 'GEV MM', 'GEV MV', 'LogPearson Type III MM'])
        for t in T:
            spamwriter.writerow([t, lnmv.ppf([t])[1][0], gumm.ppf([t])[1][0], gumv.ppf([t])[1][0], gemm.ppf([t])[1][0], gemv.ppf([t])[1][0], lpmm.ppf([t])[1][0]])

"""

Classes

"""

class Statictical_Tests:
    """ Get results of tests for the time serie.
        Runs a list of tests to a ndarray along the given axis.
        Inputs:
            - data: numpy.array.
            - without_outliers: default is True. If False is set, next tests are executed without taking out the outliers.
            - iAN: default is True for independence_anderson to be applied.
            - iAN: default is True for independence_wald_wolfowitz to be applied.
            - tMK: default is True for trend_mann_kendall to be applied.
            - sWI: default is True for signed_rank_wilcoxon to be applied.
            - sWI: default is True for homogeneity_pettitt to be applied.
    """

    def __init__(self, data, axis=0, without_outliers=True, iAN=True, iWW=True, tMK=True, sWI=True, hPE=True):
        if axis != 0:
            self.data = self.reshape_data(data, axis)
        else:
            self.data = data
        self.wo = without_outliers
        self.iAN = iAN
        self.iWW = iWW
        self.tMK = tMK
        self.sWI = sWI
        self.hPE = hPE

    def calculate(self):
        self.outliers, self.w_outliers = self.outliers_chow(self.data)
        if self.wo:
            self.data = self.w_outliers
        if self.iAN:
            self.independence_a = self.independence_anderson(self.data)
        else:
            self.independence_a = False
        if self.iWW:
            self.independence_ww = self.independence_wald_wolfowitz(self.data)
        else:
            self.independence_ww = False
        if self.tMK:
            if len(self.data.shape) == 1:
                self.trend_mk = self.trend_mann_kendall(self.data)
            elif len(self.data.shape) == 2:
                self.trend_mk = [self.trend_mann_kendall(self.data[:, i]) for i in range(self.data.shape[1])]
            elif len(self.data.shape) == 3:
                print('Mann Kendall')
                self.trend_mk = [[self.trend_mann_kendall(self.data[:, i, j]) for j in range(self.data.shape[2])] for i in range(self.data.shape[1])]
        else:
            self.trend_mk = False
        if self.sWI:
            self.signed_rank_w = self.signed_rank_wilcoxon(self.data)
        else:
            self.signed_rank_w = False
        if self.hPE:
            if len(self.data.shape) == 1:
                self.homogeneity_p = self.homogeneity_pettitt(self.data)
            elif len(self.data.shape) == 2:
                self.homogeneity_p = [self.homogeneity_pettitt(self.data[:, i]) for i in range(self.data.shape[1])]
            elif len(self.data.shape) == 3:
                self.homogeneity_p = [[self.homogeneity_pettitt(self.data[:, i, j]) for j in range(self.data.shape[2])] for i in range(self.data.shape[1])]
        else:
            self.homogeneity_p = False

    @staticmethod
    def reshape_data(data, axis):
        axes = [i for i in range(len(data.shape))]
        axes.remove(axis)
        return np.transpose(data, axes=[axis] + axes)

    @staticmethod
    def outliers_chow(data):
        """ Apply Chow's outliers test to a ndarray.
        """
        result = namedtuple('Chow_outliers', ['outliers', 'data_without_outliers'])
        Kn_Chow = np.array([[10, 2.036],[11, 2.088],[12, 2.134],[13, 2.175],\
            [14, 2.213],[15, 2.247],[16, 2.279],[17, 2.309],[18, 2.335],\
            [19, 2.361],[20, 2.385],[21, 2.408],[22, 2.429],[23, 2.448],\
            [24, 2.467],[25, 2.486],[26, 2.502],[27, 2.519],[28, 2.534],\
            [29, 2.549],[30, 2.563],[31, 2.577],[32, 2.591],[33, 2.604],\
            [34, 2.616],[35, 2.628],[36, 2.639],[37, 2.65],[38, 2.661],\
            [39, 2.671],[40, 2.682],[41, 2.692],[42, 2.7],[43, 2.71],\
            [44, 2.719],[45, 2.727],[46, 2.736],[47, 2.744],[48, 2.753],\
            [49, 2.76],[50, 2.768],[51, 2.7752],[52, 2.7824],[53, 2.7896],\
            [54, 2.7968],[55, 2.804],[56, 2.8106],[57, 2.8172],[58, 2.8238],\
            [59, 2.8304],[60, 2.837],[61, 2.8428],[62, 2.8486],[63, 2.8544],\
            [64, 2.8602],[65, 2.866],[66, 2.8714],[67, 2.8768],[68, 2.8822],\
            [69, 2.8876],[70, 2.893],[71, 2.8978],[72, 2.9026],[73, 2.9074],\
            [74, 2.9122],[75, 2.917],[76, 2.9216],[77, 2.9262],[78, 2.9308],\
            [79, 2.9354],[80, 2.94],[81, 2.9442],[82, 2.9484],[83, 2.9526],\
            [84, 2.9568],[85, 2.961],[86, 2.965],[87, 2.969],[88, 2.973],\
            [89, 2.977],[90, 2.981],[91, 2.9848],[92, 2.9886],[93, 2.9924],\
            [94, 2.9962],[95, 3],[96, 3.0034],[97, 3.0068],[98, 3.0102],\
            [99, 3.0136],[100, 3.017],[101, 3.0202],[102, 3.0234],[103, 3.0266],\
            [104, 3.0298],[105, 3.033],[106, 3.0362],[107, 3.0394],[108, 3.0426],\
            [109, 3.0458],[110, 3.049],[111, 3.0519],[112, 3.0548],[113, 3.0577],\
            [114, 3.0606],[115, 3.0635],[116, 3.0664],[117, 3.0693],[118, 3.0722],\
            [119, 3.0751],[120, 3.078],[121, 3.0806],[122, 3.0832],[123, 3.0858],\
            [124, 3.0884],[125, 3.091],[126, 3.0936],[127, 3.0962],[128, 3.0988],\
            [129, 3.1014],[130, 3.104],[131, 3.1065],[132, 3.109],[133, 3.1115],\
            [134, 3.114],[135, 3.1165],[136, 3.119],[137, 3.1215],[138, 3.124],\
            [139, 3.1265],[140, 3.129]])
        z  = np.abs(sp.zscore(np.log(np.where(data > 0, data, np.nan)), axis=0, nan_policy='omit'))
        sz = z.shape[0]
        if sz < 20:
            threshold = 10
        else:
            threshold = Kn_Chow[np.where(Kn_Chow[:,0]==sz-10)[0][0], 1]
        return result(np.where(z > threshold, data, np.nan), np.where(z < threshold, data, np.nan))

    @staticmethod
    def independence_anderson(data):
        """ Apply Anderson's independence test to a ndarray.
        """
        result = namedtuple('Anderson_independence', ['index', 'result'])
        if len(data.shape) > 1:
            res_i = np.zeros(data.shape[1:])
            res_s = np.zeros(data.shape[1:]).astype('str')
            res_s[:] = 'invalid'
        else:
            res_i = 0.0
            res_s = 'invalid'
        n = data.shape[0]
        mean = np.nanmean(data, axis=0)
        dif = data - mean
        K = np.array([k for k in range(1, int(n/3)+1)])
        if len(K) != 0:
            r_k = np.array([np.nansum((dif[:-k] * dif[k:])[:n-k] / np.nansum(dif**2, axis=0), axis=0) for k in K])
            r99inf = (- 1 + sp.norm.ppf(0.005) * np.sqrt(n - K - 1)) / (n - K)
            r95inf = (- 1 + sp.norm.ppf(0.025) * np.sqrt(n - K - 1)) / (n - K)
            r95sup = (- 1 + sp.norm.ppf(0.975) * np.sqrt(n - K - 1)) / (n - K)
            r99sup = (- 1 + sp.norm.ppf(0.995) * np.sqrt(n - K - 1)) / (n - K)
            count_95 = np.nansum([r_k[i] < r95inf[i] for i in range(len(K))], axis=0) + np.nansum([r_k[i] > r95sup[i] for i in range(len(K))], axis=0)
            count_99 = np.nansum([r_k[i] < r99inf[i] for i in range(len(K))], axis=0) + np.nansum([r_k[i] > r99sup[i] for i in range(len(K))], axis=0)
            res_i = np.where(count_99/len(K) > 0.1, 1, res_i)
            res_s = np.where(count_99/len(K) > 0.1, 'not pass', res_s)
            res_i = np.where(count_95/len(K) > 0.1, 2, res_i)
            res_s = np.where(count_95/len(K) > 0.1, 'pass 99%', res_s)
            res_i = np.where(count_95/len(K) <= 0.1, 3, res_i)
            res_s = np.where(count_95/len(K) <= 0.1, 'pass 95%', res_s)
        return result(res_i, res_s)

    @staticmethod
    def independence_wald_wolfowitz(data):
        """Apply Wald-Wolfowitz's independence test to a ndarray.
        """
        def __p_pair(n1, n2, r):
            return 2 * ss.binom(n1 - 1, r/2 - 1) * ss.binom(n2 - 1, r/2 - 1) / ss.binom(n1 + n2, n1)
        def __p_odd(n1, n2, r):
            return (ss.binom(n1-1,(r-1)/2-1)*ss.binom(n2-1,(r-1)/2)+ss.binom(n1-1,(r-1)/2)*ss.binom(n2-1,(r-1)/2-1))/ss.binom(n1+n2,n1)
        result = namedtuple('Wald_Wolfowitz_independence', ['index', 'result', 'runs', 'lower_99', 'upper_99', 'lower_95', 'upper_95'])
        rank = np.where(data <= np.mean(data, axis=0), 1, 0)
        n1 = np.nansum(rank, axis=0)
        n2 = data.shape[0] - n1
        if len(data.shape) > 1:
            r = np.ones(data.shape[1:])
            pi = np.zeros(data.shape[1:])
            pd = np.zeros(data.shape[1:])
            res = np.zeros(r.shape).astype('str')
            res[:] = 'pass 95%'
        else:
            r = 1
            pi = 0
            pd = 0
            res = 'pass 95%'
        for i in range(1, rank.shape[0]):
            r = np.where(rank[i-1] != rank[i], r + 1, r)
        ri_99 = list()
        ri_95 = list()
        for r_ in range(2, data.shape[0] + 1):
            pi_ = np.where(r_ % 2 == 0, __p_pair(n1, n2, r_), __p_odd(n1, n2, r_))
            ri_99.append(np.where(pi + pi_ > 0.005, r_ + 2, np.nan))
            ri_95.append(np.where(pi + pi_ > 0.025, r_ + 2, np.nan))
            pi += pi_
        ri_99 = np.nanmin(np.array(ri_99), axis=0)
        ri_95 = np.nanmin(np.array(ri_95), axis=0)
        rd_99 = list()
        rd_95 = list()
        for r_ in range(data.shape[0] - 1):
            r_ = data.shape[0] - r_
            pd_ = np.where(r_ % 2 == 0, __p_pair(n1, n2, r_), __p_odd(n1, n2, r_))
            rd_99.append(np.where(pd + pd_ > 0.005, r_, np.nan))
            rd_95.append(np.where(pd + pd_ > 0.025, r_, np.nan))
            pd += pd_
        rd_99 = np.nanmax(np.array(rd_99), axis=0)
        rd_95 = np.nanmax(np.array(rd_95), axis=0)
        return result(
            np.where(r > rd_95, 1, np.where(r < ri_95, 1, np.where(r > rd_99, 2, np.where(r < ri_99, 2, np.zeros(r.shape))))),
            np.where(r > rd_95, 'pass 99%', np.where(r < ri_95, 'pass 99%', np.where(r > rd_99, 'not pass', np.where(r < ri_99, 'not pass', res)))),
            r,
            ri_99,
            rd_99,
            ri_95,
            rd_95,
        )

    @staticmethod
    def trend_mann_kendall(data):
        """Apply Mann Kendall's trend test, the Hamed-Rao modification, the pre whitening modification,
        the trend free pre whitening modification and the calculation of the sens slope to a 1 dimension ndarray.
        https://github.com/mmhs013/pymannkendall
        Output:
            dictionary with the next keys:
                - Name
                - Autocorrelation lag 1 with trend
                - Autocorrelation lag 1 without trend
                - Normal confidence interval
                - MK
                - MK-HR
                - MK-PW
                - MK-TF-PW
                - SS
        Citation:
        Hussain et al., (2019). pyMannKendall: a python package for non parametric Mann Kendall family of trend tests.. 
        Journal of Open Source Software, 4(39), 1556, https://doi.org/10.21105/joss.01556
        """
        def confidence_sens_slope(x, var_s, alpha):
            """Confidence interval for Sen's slope.
            """
            idx = 0
            n = len(x)
            d = np.ones(int(n*(n-1)/2))
            for i in range(n-1):
                j = np.arange(i+1,n)
                d[idx : idx + len(j)] = (x[j] - x[i]) / (j - i)
                idx = idx + len(j)
            N = n*(n-1)/2
            C_alpha = sp.norm.ppf(1-alpha/2) * var_s ** 0.5
            M1 = (N - C_alpha) / 2
            M2 = (N + C_alpha) / 2
            return [
                np.interp(M1 - 1, np.arange(len(d)), np.sort(d)),
                np.interp(M2, np.arange(len(d)), np.sort(d)),
            ]
        data = data[~np.isnan(data)]
        result = namedtuple('Mann_Kendall_trend', [
            'Autocorrelation_lag_1_with_trend', 'Autocorrelation_lag_1_without_trend',
            'Normal_lower', 'Normal_upper',
            'MK_95', 'MK_99',
            #'MK_HR_95', 'MK_HR_99',
            #'MK_PW_95', 'MK_PW_99',
            #'MK_TF_PW_95', 'MK_TF_PW_99',
            'Slope', 'Intercept',
            'SS_95_lower', 'SS_99_lower',
            'SS_95_upper', 'SS_99_upper',
        ])
        original = pymannkendall.original_test(data)
        slope = pymannkendall.sens_slope(data)
        slope_confidence = [confidence_sens_slope(data, original[6], 0.05), confidence_sens_slope(data, original[6], 0.01)]
        return result(
            sm.tsa.acf(data)[1],
            sm.tsa.acf(data - np.arange(1, data.shape[0] + 1) * slope[0])[1],
            sp.norm.ppf(1 - 0.05 / 2) / np.sqrt(data.shape[0]),
            - sp.norm.ppf(1 - 0.05 / 2) / np.sqrt(data.shape[0]),
            original[0],
            pymannkendall.original_test(data, alpha=0.01)[0],
            #pymannkendall.hamed_rao_modification_test(data)[0],
            #pymannkendall.hamed_rao_modification_test(data, alpha=0.01)[0],
            #pymannkendall.pre_whitening_modification_test(data)[0],
            #pymannkendall.pre_whitening_modification_test(data, alpha=0.01)[0],
            #pymannkendall.trend_free_pre_whitening_modification_test(data)[0],
            #pymannkendall.trend_free_pre_whitening_modification_test(data, alpha=0.01)[0],
            slope[0],
            slope[1],
            slope_confidence[0][0],
            slope_confidence[1][0],
            slope_confidence[0][1],
            slope_confidence[1][1],
        )

    @staticmethod
    def signed_rank_wilcoxon(data):
        """Apply Wilcoxon's signed-rank test to a ndarray.
        """
        result = namedtuple('Wilcoxon_signed_rank', ['index', 'result'])
        if len(data.shape) > 1:
            res_i = np.ones(data.shape[1:])
            res_s = np.ones(data.shape[1:]).astype('str')
            res_s[:] = 'not pass'
        else:
            res_i = 1
            res_s = 'not pass'
        _, p_valor = sp.wilcoxon(data - np.nanmean(data, axis=0), nan_policy='omit')
        return result(
            np.where(p_valor < 0.975, 3, np.where(p_valor > 0.025, 3, np.where(p_valor < 0.995, 2, np.where(p_valor > 0.005, 2, res_i)))),
            np.where(p_valor < 0.975, 'pass 95%', np.where(p_valor > 0.025, 'pass 95%', np.where(p_valor < 0.995, 'pass 99%', np.where(p_valor > 0.005, 'pass 99%', res_s)))),
        )

    @staticmethod
    def homogeneity_pettitt(data):
        """Apply Pettitt's test to a ndarray.
        """
        data = data[~np.isnan(data)]
        result95 = pyhomogeneity.pettitt_test(data)
        result99 = pyhomogeneity.pettitt_test(data, alpha=0.01)
        if result99[0]:
            return ['not pass', result99[1], result99[4][0], result99[4][1]]
        elif result95[0]:
            return ['pass 99%', result95[1], result95[4][0], result95[4][1]]
        else:
            return ['pass 95%', result95[1], result95[4][0], result95[4][1]]

class LogNormal_MV:
    """Distribución LogNormal de 3 parámetros estimados por Máxima Verosimilitud.

    Preparado para el análisis de datos provenientes de precipitaciones máximas anuales

    "pdf"
    - Obtiene los valores de la curva de densidad de probabilidad de los "x" dados.

    "ppf"
    - Obtiene los valores de la curva de frecuencias para los periodos de retorno "T" dados.
    """
    def __init__(self, data):
        self.sorted_data, self.return_period = weibull_distribution(data)
        self.n = data.shape[0]
        self.params = sp.lognorm.fit(self.sorted_data, floc=0)
    def pdf(self, x):
        return sp.lognorm.pdf(x, self.params[0], loc=self.params[1], scale=self.params[2])
    def cdf(self, x):
        return sp.lognorm.cdf(x, self.params[0], loc=self.params[1], scale=self.params[2])
    def ppf(self, T):
        if type(T) == list:
            T = np.array(T)
        try:
            fi       = 2.584458*np.log(T) ** (3/8) - 2.252573
            conf     = self.params[0] / np.sqrt(self.n) * np.sqrt(1 + (fi ** 2) / 2)
            ppf_mean = sp.lognorm.ppf(1 - 1/T, self.params[0], loc=self.params[1], scale=self.params[2])
            ppf_low  = np.exp(np.log(ppf_mean) - 1.96 * conf)
            ppf_high = np.exp(np.log(ppf_mean) + 1.96 * conf)
            return ppf_low, ppf_mean, ppf_high
        except:
            print('The type of "T" must be numpy.array or list.')
    def goodness_fit(self):
        result_goodness_fit = namedtuple('Goodness_of_Fit', ['Chi_Square', 'Standard_Error', 'Percentage_error'])
        return result_goodness_fit(
            chi2(self.sorted_data, self.cdf, 3),
            standard_error(self.sorted_data, self.ppf(self.return_period)[1], 3),
            percentage_error(self.sorted_data, self.ppf(self.return_period)[1], _abs=False),
        )

class GEV_MV:
    """Distribución Generalized Extreme Value de 3 parámetros estimados por Máxima Verosimilitud.

    Preparado para el análisis de datos provenientes de precipitaciones máximas anuales

    "pdf"
    - Obtiene los valores de la curva de densidad de probabilidad de los "x" dados.

    "ppf"
    - Obtiene los valores de la curva de frecuencias para los periodos de retorno "T" dados.
    """
    def __init__(self, data):
        self.sorted_data, self.return_period = weibull_distribution(data)
        self.n = data.shape[0]
        self.params = sp.genextreme.fit(self.sorted_data)
        self.stats  = sp.genextreme.stats(self.params[0], loc=self.params[1], scale=self.params[2], moments='mvsk')
    def pdf(self, x):
        return sp.genextreme.pdf(x, self.params[0], loc=self.params[1], scale=self.params[2])
    def cdf(self, x):
        return sp.genextreme.cdf(x, self.params[0], loc=self.params[1], scale=self.params[2])
    def ppf(self, T):
        if type(T) == list:
            T = np.array(T)
        try:
            conf = np.sqrt(self.stats[1] / self.n) * \
                np.sqrt(1.11 + 0.52 * (-np.log(-np.log(1 - 1 / T))) + \
                0.61 * (-np.log(-np.log(1 - 1 / T))) ** 2)
            ppf_mean = sp.genextreme.ppf(1 - 1/T, self.params[0], loc=self.params[1], scale=self.params[2])
            ppf_low  = ppf_mean - 1.96 * conf
            ppf_high = ppf_mean + 1.96 * conf
            return ppf_low, ppf_mean, ppf_high
        except:
            print('The type of "T" must be numpy.array or list.')
    def goodness_fit(self):
        result_goodness_fit = namedtuple('Goodness_of_Fit', ['Chi_Square', 'Standard_Error', 'Percentage_error'])
        return result_goodness_fit(
            chi2(self.sorted_data, self.cdf, 3),
            standard_error(self.sorted_data, self.ppf(self.return_period)[1], 3),
            percentage_error(self.sorted_data, self.ppf(self.return_period)[1], _abs=False),
        )

class GEV_MM:
    """Distribución Generalized Extreme Value de 3 parámetros estimados por el Método de los Momentos.

    Preparado para el análisis de datos provenientes de precipitaciones máximas anuales

    "pdf"
    - Obtiene los valores de la curva de densidad de probabilidad de los "x" dados.

    "ppf"
    - Obtiene los valores de la curva de frecuencias para los periodos de retorno "T" dados.
    """
    def __init__(self, data):
        self.sorted_data, self.return_period = weibull_distribution(data)
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        self.n = data.shape[0]
        # Coeficiente de asimetría de la muestra (skew)
        g = 0  
        for i in range(self.n):
          g = g + self.n * (data[i] - mean) ** 3
        g = g / ((self.n - 1) * (self.n - 2) * std ** 3)
        # Expresiones para "beta" (c) parámetro de forma de la distribución
        if g > -11.35 and g < 1.1396:
            self.c = 0.279434 - 0.333535 * g + 0.048306 * g ** 2 - 0.023314 * g ** 3 + \
                0.00376 * g ** 4 - 0.000263 * g ** 5
        if g > 1.14 and g < 18.95:
            self.c = 0.25031 - 0.29219 * g + 0.075357 * g ** 2 - 0.010883 * g ** 3 + \
                0.000904 * g ** 4 - 0.000043 * g ** 5
        self.params = sp.genextreme.fit_loc_scale(self.sorted_data, self.c)
        self.stats  = sp.genextreme.stats(self.c, loc=self.params[0], scale=self.params[1])
    def pdf(self, x):
        return sp.genextreme.pdf(x, self.c, loc=self.params[0], scale=self.params[1])
    def cdf(self, x):
        return sp.genextreme.cdf(x, self.c, loc=self.params[0], scale=self.params[1])
    def ppf(self, T):
        if type(T) == list:
            T = np.array(T)
        try:
            conf = np.sqrt(self.stats[1] / self.n) * \
                np.sqrt(1.11 + 0.52 * (-np.log(-np.log(1 - 1 / T))) + \
                0.61 * (-np.log(-np.log(1 - 1 / T))) ** 2)
            ppf_mean = sp.genextreme.ppf(1 - 1/T, self.c, loc=self.params[0], scale=self.params[1])
            ppf_low  = ppf_mean - 1.96 * conf
            ppf_high = ppf_mean + 1.96 * conf
            return ppf_low, ppf_mean, ppf_high
        except:
            print('The type of "T" must be numpy.array or list.')
    def goodness_fit(self):
        result_goodness_fit = namedtuple('Goodness_of_Fit', ['Chi_Square', 'Standard_Error', 'Percentage_error'])
        return result_goodness_fit(
            chi2(self.sorted_data, self.cdf, 2),
            standard_error(self.sorted_data, self.ppf(self.return_period)[1], 2),
            percentage_error(self.sorted_data, self.ppf(self.return_period)[1], _abs=False),
        )

class Gumbel_MV:
    """Distribución Gumbel de 2 parámetros estimados por Máxima Verosimilitud.

    Preparado para el análisis de datos provenientes de precipitaciones máximas anuales.

    "pdf"
    - Obtiene los valores de la curva de densidad de probabilidad de los "x" dados.

    "ppf"
    - Obtiene los valores de la curva de frecuencias para los periodos de retorno "T" dados.
    """
    def __init__(self, data):
        self.sorted_data, self.return_period = weibull_distribution(data)
        self.n = data.shape[0]
        self.params = sp.gumbel_r.fit(self.sorted_data)
    def pdf(self, x):
        return sp.gumbel_r.pdf(x, loc=self.params[0], scale=self.params[1])
    def cdf(self, x):
        return sp.gumbel_r.cdf(x, loc=self.params[0], scale=self.params[1])
    def ppf(self, T):
        if type(T) == list:
            T = np.array(T)
        try:
            fi       = (- np.sqrt(6) / math.pi) * (0.5772 + np.log(np.log(T / (T - 1))))
            conf     = np.sqrt(self.params[1]) / np.sqrt(self.n) * np.sqrt(1 + 1.1396 * fi + 1.1 * fi ** 2)
            ppf_mean = sp.gumbel_r.ppf(1 - 1/T, loc=self.params[0], scale=self.params[1])
            ppf_low  = ppf_mean - 1.96 * conf
            ppf_high = ppf_mean + 1.96 * conf
            return ppf_low, ppf_mean, ppf_high
        except:
            print('The type of "T" must be numpy.array or list.')
    def goodness_fit(self):
        result_goodness_fit = namedtuple('Goodness_of_Fit', ['Chi_Square', 'Standard_Error', 'Percentage_error'])
        return result_goodness_fit(
            chi2(self.sorted_data, self.cdf, 3),
            standard_error(self.sorted_data, self.ppf(self.return_period)[1], 3),
            percentage_error(self.sorted_data, self.ppf(self.return_period)[1], _abs=False),
        )

class Gumbel_MM:
    """Distribución Gumbel de 2 parámetros estimados por el Método de los Momentos.

    Preparado para el análisis de datos provenientes de precipitaciones máximas anuales.

    "pdf"
    - Obtiene los valores de la curva de densidad de probabilidad de los "x" dados.

    "ppf"
    - Obtiene los valores de la curva de frecuencias para los periodos de retorno "T" dados.
    """
    def __init__(self, data):
        self.sorted_data, self.return_period = weibull_distribution(data)
        self.n = data.shape[0]
        self.params = sp.gumbel_r.fit_loc_scale(self.sorted_data)
    def pdf(self, x):
        return sp.gumbel_r.pdf(x, loc=self.params[0], scale=self.params[1])
    def cdf(self, x):
        return sp.gumbel_r.cdf(x, loc=self.params[0], scale=self.params[1])
    def ppf(self, T):
        if type(T) == list:
            T = np.array(T)
        try:
            fi       = (- np.sqrt(6) / math.pi) * (0.5772 + np.log(np.log(T / (T - 1))))
            conf     = np.sqrt(self.params[1]) / np.sqrt(self.n) * np.sqrt(1 + 1.1396 * fi + 1.1 * fi ** 2)
            ppf_mean = sp.gumbel_r.ppf(1 - 1/T, loc=self.params[0], scale=self.params[1])
            ppf_low  = ppf_mean - 1.96 * conf
            ppf_high = ppf_mean + 1.96 * conf
            return ppf_low, ppf_mean, ppf_high
        except:
            print('The type of "T" must be numpy.array or list.')
    def goodness_fit(self):
        result_goodness_fit = namedtuple('Goodness_of_Fit', ['Chi_Square', 'Standard_Error', 'Percentage_error'])
        return result_goodness_fit(
            chi2(self.sorted_data, self.cdf, 2),
            standard_error(self.sorted_data, self.ppf(self.return_period)[1], 2),
            percentage_error(self.sorted_data, self.ppf(self.return_period)[1], _abs=False),
        )

class LogPearson3_MM:
    """Distribución LogPearson 3 de 3 parámetros estimados por el Método de los Momentos.

    Preparado para el análisis de datos provenientes de precipitaciones máximas anuales.

    "pdf"
    - Obtiene los valores de la curva de densidad de probabilidad de los "x" dados.

    "ppf"
    - Obtiene los valores de la curva de frecuencias para los periodos de retorno "T" dados.
    """
    def __init__(self, data):
        self.sorted_data, self.return_period = weibull_distribution(data)
        self.n = data.shape[0]
        self.params = sp.pearson3.fit(np.log10(self.sorted_data), method='MM')
        self.stats = sp.pearson3.stats(self.params[0], loc=self.params[1], scale=self.params[2])
        self.k = self.params[0] / 6
    def pdf(self, x):
        return sp.pearson3.pdf(np.log10(x), self.params[0], loc=self.params[1], scale=self.params[2])
    def cdf(self, x):
        return sp.pearson3.cdf(np.log10(x), self.params[0], loc=self.params[1], scale=self.params[2])
    def ppf(self, T):
        if type(T) == list:
            T = np.array(T)
        try:
            # Abramowitz y Stegun, 1965
            z      = list()
            for p in (1/T):
                if p > 0.5:
                    p = 1 - p
                    w = np.sqrt(np.log(1 / (p ** 2)))
                    z.append(-(w - ((2.515517 + 0.802853 * w + 0.010328 * w ** 2) \
                        / (1 + 1.432788 * w + 0.189269 * w ** 2 + 0.001308 * w **3))))
                else:
                    w = np.sqrt(np.log(1 / (p ** 2)))
                    z.append(w - ((2.515517 + 0.802853 * w + 0.010328 * w ** 2) \
                        / (1 + 1.432788 * w + 0.189269 * w ** 2 + 0.001308 * w **3)))
            z = np.array(z)
            # Wilson-Hilferty approximation, Kite 1977
            fi = z + (z ** 2 - 1) * self.k + 1/3 * (z ** 3 - 6 * z) * self.k ** 2 - \
                (z ** 2 - 1) * self.k ** 3 + z * self.k ** 4 + 1/3 * self.k ** 5
            a = 1 - (1.96 ** 2) / (2 * (self.n - 1))
            b = fi ** 2 - (1.96 ** 2) / self.n
            fi_U = (fi + np.sqrt(fi ** 2 - a * b)) / a
            fi_L = (fi - np.sqrt(fi ** 2 - a * b)) / a
            ppf_mean = 10 ** (self.stats[0] + fi   * np.sqrt(self.stats[1]))#sp.pearson3.ppf(1 - 1/T, self.params[0], loc=self.params[1], scale=self.params[2])
            ppf_low  = 10 ** (self.stats[0] + fi_L * np.sqrt(self.stats[1]))
            ppf_high = 10 ** (self.stats[0] + fi_U * np.sqrt(self.stats[1]))
            return ppf_low, ppf_mean, ppf_high
        except:
            print('The type of "T" must be numpy.array or list.')
    def goodness_fit(self):
        result_goodness_fit = namedtuple('Goodness_of_Fit', ['Chi_Square', 'Standard_Error', 'Percentage_error'])
        return result_goodness_fit(
            chi2(self.sorted_data, self.cdf, 3),
            standard_error(self.sorted_data, self.ppf(self.return_period)[1], 3),
            percentage_error(self.sorted_data, self.ppf(self.return_period)[1], _abs=False),
        )