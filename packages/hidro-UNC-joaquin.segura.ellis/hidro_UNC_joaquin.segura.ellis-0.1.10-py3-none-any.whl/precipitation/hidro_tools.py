"""

Libraries

"""

import sys, os
sys.path.insert(0, os.getcwd())
from precipitation.libraries import *

"""

Classes

"""

class Rainfall_Indices:
    """Get climate indices information from rainfall data.

    Parameters:

    - time : numpy.ndarray, dtype=datetime64 or np.dtype('M')
        A 1 dimension ndarray with that must be completed from the
        first to the last element with the required frequency.
    
    - data : numpy.ndarray, dtype=float
        A 1, 2 or 3 dimension ndarray in which one dimension 
        corresponds with time's dimension.

    - axis : int
        It is 0 for default but can be change to 1 or 2 if time's
        dimension is not 0 in data array.

    - period : list of strings
        A list with all periods to analyze. Just yearly period (Y)
        for default but can take seasonal periods (jja, son, djf,
        mam) or monthly period (M)

    - start_month : int
        It can take values from 1 to 12 refering each month of the
        year and just works for yearly period. It is 7 (July) for 
        default.
    """
    def __init__(self, time, data, axis=0, period=['Y'], start_month=7):
        self.time = time
        if axis != 0:
            self.data = self.reshape_data(data, axis)
        else:
            self.data = data
        self.period = period
        self.start_month = start_month
        self.time_indices = list()
        self.rmax = list()
        self.r95p = list()
        self.r95mm = list()
        self.rtot = list()
        self.cwd = list()

    def calculate(self):
        self.rmax_calc()
        self.r95p_calc()
        self.r95mm_calc()
        self.rtot_calc()
        self.cwd_calc()
    
    @staticmethod
    def reshape_data(data, axis):
        axes = [i for i in range(len(data.shape))]
        axes.remove(axis)
        return np.transpose(data, axes=[axis] + axes)
    
    @staticmethod
    def trim_data_yearly(time, data, start_month=7):
        inicial_datetime = time[0]
        if inicial_datetime != datetime.datetime(inicial_datetime.year, start_month, 1):
            if inicial_datetime < datetime.datetime(inicial_datetime.year, start_month, 1):
                data = data[np.where(time == datetime.datetime(inicial_datetime.year, start_month, 1))[0][0]:]
                time = time[np.where(time == datetime.datetime(inicial_datetime.year, start_month, 1))[0][0]:]
            else:
                data = data[np.where(time == datetime.datetime(inicial_datetime.year + 1, start_month, 1))[0][0]:]
                time = time[np.where(time == datetime.datetime(inicial_datetime.year + 1, start_month, 1))[0][0]:]
        final_datetime = time[-1] + datetime.timedelta(days=1)
        if final_datetime != datetime.datetime(final_datetime.year, start_month, 1):
            if final_datetime < datetime.datetime(final_datetime.year, start_month, 1):
                data = data[:np.where(time == datetime.datetime(final_datetime.year - 1, start_month, 1))[0][0]]
                time = time[:np.where(time == datetime.datetime(final_datetime.year - 1, start_month, 1))[0][0]]
            else:
                data = data[:np.where(time == datetime.datetime(final_datetime.year, start_month, 1))[0][0]]
                time = time[:np.where(time == datetime.datetime(final_datetime.year, start_month, 1))[0][0]]
        return time, data
    
    @staticmethod
    def cut_data_yearly(time, data, start_month=7):
        years = np.unique([time_.year for time_ in time])
        if start_month != 1:
            index_year = -2
            time_ = np.array([datetime.datetime(year, start_month, 1) for year in years[:-1]])
        else:
            index_year = -1
            time_ = np.array([datetime.datetime(year, start_month, 1) for year in years])
        data_ = [data[np.where(time == datetime.datetime(year, start_month, 1))[0][0]:np.where(time == datetime.datetime(year + 1, start_month, 1))[0][0]] for year in years[:index_year]]
        data_ = data_ + [data[np.where(time == datetime.datetime(years[index_year], start_month, 1))[0][0]:]]
        return time_, data_
    
    @staticmethod
    def trim_data_monthly(time, data, m=None):
        if m != None:
            inicial_datetime = time[0]
            if inicial_datetime != datetime.datetime(inicial_datetime.year, m[0], 1):
                if inicial_datetime < datetime.datetime(inicial_datetime.year, m[0], 1):
                    data = data[np.where(time == datetime.datetime(inicial_datetime.year, m[0], 1))[0][0]:]
                    time = time[np.where(time == datetime.datetime(inicial_datetime.year, m[0], 1))[0][0]:]
                else:
                    data = data[np.where(time == datetime.datetime(inicial_datetime.year + 1, m[0], 1))[0][0]:]
                    time = time[np.where(time == datetime.datetime(inicial_datetime.year + 1, m[0], 1))[0][0]:]
            final_datetime = time[-1] + datetime.timedelta(days=1)
            if final_datetime != datetime.datetime(final_datetime.year, m[-1], 1) + relativedelta(months=1):
                if final_datetime < datetime.datetime(final_datetime.year, m[-1], 1) + relativedelta(months=1):
                    data = data[:np.where(time == datetime.datetime(final_datetime.year - 1, m[-1], 1) + relativedelta(months=1))[0][0]]
                    time = time[:np.where(time == datetime.datetime(final_datetime.year - 1, m[-1], 1) + relativedelta(months=1))[0][0]]
                else:
                    data = data[:np.where(time == datetime.datetime(final_datetime.year, m[-1], 1) + relativedelta(months=1))[0][0]]
                    time = time[:np.where(time == datetime.datetime(final_datetime.year, m[-1], 1) + relativedelta(months=1))[0][0]]
            months = np.array([_.month for _ in time])
            data = np.concatenate([data[np.where(months == _)] for _ in m], axis=0)
            time = np.concatenate([time[np.where(months == _)] for _ in m], axis=0)
            time_sort = np.array(sorted(time))
            data = np.array([data[np.where(time == _)[0][0]] for _ in time_sort])
            time = time_sort
        else:
            inicial_datetime = time[0]
            if inicial_datetime != datetime.datetime(inicial_datetime.year, inicial_datetime.month, 1):
                data = data[np.where(time == datetime.datetime(inicial_datetime.year, inicial_datetime.month, 1) + relativedelta(months=1))[0][0]:]
                time = time[np.where(time == datetime.datetime(inicial_datetime.year, inicial_datetime.month, 1) + relativedelta(months=1))[0][0]:]
            final_datetime = time[-1] + datetime.timedelta(days=1)
            if final_datetime != datetime.datetime(final_datetime.year, final_datetime.month, 1):
                data = data[:np.where(time == datetime.datetime(final_datetime.year, final_datetime.month, 1))[0][0]]
                time = time[:np.where(time == datetime.datetime(final_datetime.year, final_datetime.month, 1))[0][0]]
        return time, data
    
    @staticmethod
    def cut_data_monthly(time, data, m=None):
        if m != None:
            time_ = list()
            data_ = list()
            years = np.unique(np.array([_.year for _ in time]))
            for year in years[:-1]:
                time_.append(datetime.datetime(year, m[0], 1))
                data_.append(data[np.where(time == time_[-1])[0][0]:np.where(time == time_[-1] + relativedelta(months=len(m), days=-1))[0][0] + 1])
            if 12 not in m and 1 not in m:
                time_.append(datetime.datetime(years[-1], m[0], 1))
                data_.append(data[np.where(time == time_[-1])[0][0]:])
        else:
            time_ = list()
            data_ = list()
            years = np.array([_.year for _ in time])
            years_ = np.unique(years)
            months = np.array([_.month for _ in time])
            for year in years_:
                months_ = months[np.where(years == year)]
                year_data = data[np.where(years == year)]
                for month in np.unique(months_):
                    time_.append(datetime.datetime(year, month, 1))
                    data_.append(year_data[np.where(months_ == month)])
        return np.array(time_), data_
    
    def get_data(self, p):
        if p == 'Y':
            time_, data_ = self.trim_data_yearly(self.time, self.data, self.start_month)
            q_95 = np.nanquantile(data_, .95, axis=0)
            time_, data_ = self.cut_data_yearly(time_, data_, self.start_month)
        elif p == 'M':
            time_, data_ = self.trim_data_monthly(self.time, self.data)
            q_95 = np.nanquantile(data_, .95, axis=0)
            time_, data_ = self.cut_data_monthly(time_, data_)
        elif p == 'jja':
            time_, data_ = self.trim_data_monthly(self.time, self.data, m=[6, 7, 8])
            q_95 = np.nanquantile(data_, .95, axis=0)
            time_, data_ = self.cut_data_monthly(time_, data_, m=[6, 7, 8])
        elif p == 'son':
            time_, data_ = self.trim_data_monthly(self.time, self.data, m=[9, 10, 11])
            q_95 = np.nanquantile(data_, .95, axis=0)
            time_, data_ = self.cut_data_monthly(time_, data_, m=[9, 10, 11])
        elif p == 'djf':
            time_, data_ = self.trim_data_monthly(self.time, self.data, m=[12, 1, 2])
            q_95 = np.nanquantile(data_, .95, axis=0)
            time_, data_ = self.cut_data_monthly(time_, data_, m=[12, 1, 2])
        elif p == 'mam':
            time_, data_ = self.trim_data_monthly(self.time, self.data, m=[3, 4, 5])
            q_95 = np.nanquantile(data_, .95, axis=0)
            time_, data_ = self.cut_data_monthly(time_, data_, m=[3, 4, 5])
        return time_, data_, q_95

    def rmax_calc(self):
        for p in self.period:
            time, data, q_95 = self.get_data(p)
            self.time_indices.append(time)
            rmax = np.array([np.nanmax(data_, axis=0) for data_ in data])
            rmax[rmax == 0] = np.nan
            self.rmax.append(rmax)
    
    def r95p_calc(self):
        for p in self.period:
            time, data, q_95 = self.get_data(p)
            self.time_indices.append(time)
            data = [np.where(data_ >= 1, data_, 0) for data_ in data]
            r95p = np.array([np.nansum(np.where(data_ >= q_95, data_, 0), axis=0) for data_ in data])
            r95p[r95p == 0] = np.nan
            self.r95p.append(r95p)
    
    def r95mm_calc(self):
        for p in self.period:
            time, data, q_95 = self.get_data(p)
            self.time_indices.append(time)
            r95mm = np.array([np.nansum(np.where(np.where(data_ >= 1, data_, 0.) >= q_95, 1., 0.), axis=0) for data_ in data])
            r95mm[r95mm == 0.] = np.nan
            self.r95mm.append(r95mm)
    
    def rtot_calc(self):
        for p in self.period:
            time, data, q_95 = self.get_data(p)
            self.time_indices.append(time)
            rtot = np.array([np.nansum(np.where(data_ >= 1, data_, 0), axis=0) for data_ in data])
            rtot[rtot == 0] = np.nan
            self.rtot.append(rtot)

    def cwd_calc(self):
        for p in self.period:
            time, data, q_95 = self.get_data(p)
            self.time_indices.append(time)
            data = [np.where(data_ >= 1., 1., 0.) for data_ in data]
            for i in range(len(data)):
                for j in range(1, data[i].shape[0]):
                    data[i][j] = (data[i][j-1] + data[i][j]) * data[i][j]
            cwd = np.array([np.nanmax(data_, axis=0) for data_ in data])
            cwd[cwd == 0.] = np.nan
            self.cwd.append(cwd)

class Rain_Gauge(Rainfall_Indices):
    """This class runs a pre-process to a rain gauge.
    """
    def __init__(self, path_csv=None):
        if path_csv != None:
            with open(path_csv, 'r', newline='') as csvfile:
                data = np.array([_ for _ in csv.reader(csvfile, delimiter=',')])
            self.id, self.name, self.lon, self.lat, self.elevation, self.province, self.country, self.institution, self.record_time = data[:9, 1]
            self.lon, self.lat, self.elevation = float(self.lon), float(self.lat), float(self.elevation)
            self.time = np.array([datetime.datetime.strptime(str(_), '%Y-%m-%d') for _ in data[10:, 0]])
            self.prec = data[10:, 1].astype('f')

    @staticmethod
    def detect_wet_period(time, prec):
        def get_relation(years, rainfall_indices, indice):
            result = np.zeros((4, years.shape[0]))
            for k in range(1, 5):
                for j in range(rainfall_indices.time_indices[k].shape[0]):
                    i = np.where(years == rainfall_indices.time_indices[k][j].year)[0]
                    if i.shape[0] > 0:
                        i = i[0]
                        result[k-1, i] = indice[k][j] / indice[0][i]
            return result
        rainfall_indices = Rainfall_Indices(time, prec, period=['Y', 'jja', 'son', 'djf', 'mam'], start_month=3)
        rainfall_indices.calculate()
        years = np.array([_.year for _ in rainfall_indices.time_indices[0]])
        #indice1 = rainfall_indices.r95p
        indice1 = rainfall_indices.rmax
        result1 = get_relation(years, rainfall_indices, indice1)
        #aux1 = np.array(['jja', 'son', 'djf', 'mam'])[np.nanquantile(result1, 0.75, axis=1) >= 0.2]
        result1 = np.nanmean(result1, axis=1)
        aux1 = np.array(['jja', 'son', 'djf', 'mam'])[result1 == np.nanmax(result1)]
        indice2 = rainfall_indices.rtot
        result2 = get_relation(years, rainfall_indices, indice2)
        #aux2 = np.array(['jja', 'son', 'djf', 'mam'])[np.nanquantile(result2, 0.75, axis=1) >= 0.2]
        result = np.unique(np.concatenate([aux1]))
        wet_period = 'annual'
        if 'djf' in result and 'jja' not in result:
            wet_period = 'summer'
        elif 'jja' in result:
            wet_period = 'winter'
        if wet_period == 'winter':
            start_month = 1
        else:
            start_month = 7
        return wet_period, start_month

    @staticmethod
    def detect_wet_months(time, prec, start_month):
        rainfall_indices = Rainfall_Indices(time, prec, period=['Y', 'M'], start_month=start_month)
        rainfall_indices.calculate()
        years = np.array([_.year for _ in rainfall_indices.time_indices[0]])
        result1 = list()
        result2 = list()
        for j, year in enumerate(years):
            i = list(rainfall_indices.time_indices[1]).index(datetime.datetime(year, start_month, 1))
            data = np.array([rainfall_indices.time_indices[1][i:i+12], rainfall_indices.rmax[1][i:i+12]])
            data = data[:, ~np.isnan(data[1].astype('f'))].T
            if data.shape[0] > 0:
                aux = [_.month for _ in data[np.where(data[:, 1] >= np.quantile(data[:, 1], 0.99))[0], 0]]
                #aux = [_.month for _ in data[np.where(data[:, 1] == np.nanmax(data[:, 1]))[0], 0]]
                result1.append(aux)
                #result2.append(aux)
                data = np.array([rainfall_indices.time_indices[1][i:i+12], rainfall_indices.rtot[1][i:i+12]])
                data = data[:, np.argsort(data[1])]
                data = np.array([data[0], data[1], np.cumsum(data[1])]).T
                result2.append([_.month for _ in data[np.where(data[:, 2] > 0.1 * rainfall_indices.rtot[0][j])[0], 0]])
        return np.unique(np.concatenate(result1)), np.unique(np.concatenate(result2))

    @staticmethod
    def get_indexes(year, month, years, months, start_month):
        if month < start_month:
            year += 1
        aux_years = years == year
        aux_months = months == month
        return aux_years * aux_months
    
    def year_filter(self, y, years, months):
        prec_year = self.prec[np.any([self.get_indexes(y, m, years, months, self.start_month) for m in self.maxs_months], axis=0)]
        prec_year = np.where(prec_year >= 1, prec_year, 0)
        if np.all(prec_year == 0):
            return True
        else:
            return False

    def discard_incomplete_years(self, save_path, delete_years):
        rainfall_indices = Rainfall_Indices(self.time, self.prec, period=['Y'], start_month=self.start_month)
        rainfall_indices.calculate()
        years = np.array([_.year for _ in self.time])
        months = np.array([_.month for _ in self.time])
        months_ = np.arange(self.start_month, self.start_month + 12)
        months_[months_ > 12] -= 12
        years_ = np.unique(years)
        if self.start_month != 1:
            years_ = years_[:-1]
        ymax = np.nanmax(self.prec)
        for y in years_:
            if self.year_filter(y, years, months):
                self.prec[np.any([self.get_indexes(y, m, years, months, self.start_month) for m in months_], axis=0)] = np.nan
            if y in delete_years:
                self.prec[np.any([self.get_indexes(y, m, years, months, self.start_month) for m in months_], axis=0)] = np.nan

    def calculate(self, save_path, delete_years):
        self.wet_period, self.start_month = self.detect_wet_period(self.time, self.prec)
        self.maxs_months, self.wet_months = self.detect_wet_months(self.time, self.prec, self.start_month)
        self.time, self.prec = self.trim_data_yearly(self.time, self.prec, self.start_month)
        self.discard_incomplete_years(save_path, delete_years)

    def save(self, path):
        with open(path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['id', self.id])
            csvwriter.writerow(['name', self.name])
            csvwriter.writerow(['lon', self.lon])
            csvwriter.writerow(['lat', self.lat])
            csvwriter.writerow(['elevation', self.elevation])
            csvwriter.writerow(['province/state', self.province])
            csvwriter.writerow(['country', self.country])
            csvwriter.writerow(['institution', self.institution])
            csvwriter.writerow(['record_time', self.record_time])
            csvwriter.writerow(['wet_period', self.wet_period])
            csvwriter.writerow(['start_month', self.start_month])
            csvwriter.writerow(['time', 'prec (mm)'])
            for i in range(self.time.shape[0]):
                csvwriter.writerow([self.time[i].date(), self.prec[i]])

    def load(self, path_csv):
        if path_csv != None:
            with open(path_csv, 'r', newline='') as csvfile:
                data = np.array([_ for _ in csv.reader(csvfile, delimiter=',')])
            self.id, self.name, self.lon, self.lat, self.elevation, self.province, self.country, self.institution, self.record_time = data[:9, 1]
            self.lon, self.lat, self.elevation = float(self.lon), float(self.lat), float(self.elevation)
            self.wet_period = data[10, 1]
            self.start_month = int(data[11, 1])
            self.time = np.array([datetime.datetime.strptime(str(_), '%Y-%m-%d') for _ in data[10:, 0]])
            self.prec = data[12:, 1].astype('f')