"""

Libraries

"""

import sys, os
sys.path.insert(0, os.getcwd())
from precipitation.libraries import *
from precipitation.hidro_tools import *
from precipitation.FACETA import *
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import imageio
from global_land_mask import globe

"""

Methods

"""

def open_IMERG(path, folder, lon1, lon2, lat1, lat2):
    """This method returns an xarray.Dataset that merge all data in the folder of the path specified.
    *Warning* this uses a lot of RAM capacity.
    """
    daily_prec_files = os.listdir(f'{path}\\{folder}')
    data_list1 = list()
    time_list  = list()
    for file in daily_prec_files:
        f = open(f'{path}\\{folder}\\{file}', 'rb')
        data = pickle.load(f)
        f.close()
        for day in list(data.keys())[2:]:
            data_list1.append(data[day]['precipitationCal'])
            time_list.append(datetime.date(int(day[:4]), int(day[5:7]), int(day[8:])))
    ds = xr.Dataset(
        data_vars = {
            'precipitationCal' : (['time', 'lon', 'lat'], data_list1),
        },
        coords = {
            'lon'  : (['lon'], np.array([i/100 for i in range(int(lon1*100), int(lon2*100), 10)])),
            'lat'  : (['lat'], np.array([i/100 for i in range(int(lat1*100), int(lat2*100), 10)])),
            'time' : (['time'], pd.to_datetime(time_list)),
        },
        attrs = dict(description=folder),
    )
    return ds

def etopo(lon_new, lat_new, engine='netcdf4'):
    """Return topography for a define longitud and latitud
    """
    if 'ETOPO1_Bed_g_gdal.grd' in os.listdir(os.getcwd()):
        ds = xr.open_dataset('ETOPO1_Bed_g_gdal.grd', engine=engine)
    else:
        url = 'https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/data/bedrock/grid_registered/netcdf/ETOPO1_Bed_g_gdal.grd.gz'
        result = requests.get(url)
        result.raise_for_status()
        f = open('ETOPO1_Bed_g_gdal.grd','wb')
        f.write(result.content)
        f.close()
        ds = xr.open_dataset('ETOPO1_Bed_g_gdal.grd', engine=engine)
    lon_range  = ds['x_range'].values
    lat_range  = ds['y_range'].values
    topo_range = ds['z_range'].values
    spacing    = ds['spacing'].values
    dimension  = ds['dimension'].values
    z          = ds['z'].values
    lon = np.arange(lon_range[0], lon_range[1]+1/10000, (lon_range[1]-lon_range[0])/(dimension[0]-1))
    lon = np.where(lon>180, 180, lon)
    lat = np.arange(lat_range[0], lat_range[1]+1/10000, (lat_range[1]-lat_range[0])/(dimension[1]-1))
    lat = np.where(lat>90, 90, lat)
    topo = np.flip(np.reshape(z, (dimension[1], dimension[0])), axis=0)
    interpolation = scipy.interpolate.interp2d(lon, lat, topo)
    lon_grid, lat_grid = np.meshgrid(lon_new, lat_new)
    return np.where(globe.is_ocean(lat_grid, lon_grid), np.nan, interpolation(lon_new, lat_new)), interpolation

def search_loc(lons_, lats_, lons, lats):
    """ Search for nearest cordinates from lons and lats to lons_ and lats_.
    Return a numpy.array with the index where to find those coordinates.
    """
    lons_ = lons_
    lats_ = lats_
    lons  = np.sort(lons)
    lats  = np.sort(lats)
    low_lons  = np.searchsorted(lons, lons_)-1
    high_lons = np.searchsorted(lons, lons_)
    low_lats  = np.searchsorted(lats, lats_)-1
    high_lats = np.searchsorted(lats, lats_)
    return np.array([low_lons, high_lons, low_lats, high_lats])

"""

Classes

"""

class Download_IMERG:
    """Download IMERG data from "start_date" to "end_date" for the rectangle of longitud "lon1" to "lon2" and latitude "lat1" to "lat2".
    It saves the files in a new folder of name "title" located in "save_path".
    It is required to specify the version of IMERG needed (Early, Late and Final) and the frequency of data (1D for daily and 30T for half hourly).
    """

    def __init__(self, start_date, end_date, freq, version, lon1, lon2, lat1, lat2, save_path, HQ_IR=False):
        self.freq = freq
        self.version = version
        self.bbox = [lon1, lon2, lat1, lat2]
        self.save_path = save_path
        if freq == '30T':
            if self.version == 'Early':
                self.title = 'GPM IMERG Early Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V06 (GPM_3IMERGHHE)'
            elif self.version == 'Late':
                self.title = 'GPM IMERG Late Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V06 (GPM_3IMERGHHL)'
            elif self.version == 'Final':
                self.title = 'GPM IMERG Final Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V06 (GPM_3IMERGHH)'
            else:
                raise ValueError('Version is not valid, choose Early, Late or Final.')
        elif freq == '1D':
            if self.version == 'Early':
                self.title = 'GPM IMERG Early Precipitation L3 1 day 0.1 degree x 0.1 degree V06 (GPM_3IMERGDE)'
            elif self.version == 'Late':
                self.title = 'GPM IMERG Late Precipitation L3 1 day 0.1 degree x 0.1 degree V06 (GPM_3IMERGDL)'
            elif self.version == 'Final':
                self.title = 'GPM IMERG Final Precipitation L3 1 day 0.1 degree x 0.1 degree V06 (GPM_3IMERGDF)'
            else:
                raise ValueError('Version is not valid, choose Early, Late or Final.')
        else:
            raise ValueError('Time frequency must be 1D for daily and 30T for half-hourly.')
        self.datetime = pd.date_range(
            start=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
            end=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
            freq=self.freq,
        )[:-1]
        self.date = np.unique(self.datetime.date)
        self.urls = [self.generate_url(dt, freq, version) for dt in self.datetime]
        #self.file_paths = [Path(self.get_path(self.save_path, 'temp'), f'{dt.year:04}{dt.month:02}{dt.day:02}{dt.hour:02}{dt.minute:02}.hdf5') for dt in self.datetime]

    @staticmethod
    def generate_url(date, freq, version):
        if version == 'Final' or version == 'final':
            if freq == '1D':
                return f'https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.06/{date.year}/{date.month:02}/3B-DAY.MS.MRG.3IMERG.{date.year}{date.month:02}{date.day:02}-S000000-E235959.V06.nc4'
            elif freq == '30T':
                minutes = date.hour * 60 + date.minute
                day_of_year = date.strftime('%j')
                return f'https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHH.06/{date.year}/{day_of_year}/3B-HHR.MS.MRG.3IMERG.{date.year}{date.month:02}{date.day:02}-S{date.hour:02}{date.minute:02}00-E{date.hour:02}{date.minute+29:02}59.{minutes:04}.V06B.HDF5'
        if version == 'Late' or version == 'late':
            if freq == '1D':
                return f'https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDL.06/{date.year}/{date.month:02}/3B-DAY-L.MS.MRG.3IMERG.{date.year}{date.month:02}{date.day:02}-S000000-E235959.V06.nc4'
            elif freq == '30T':
                minutes = date.hour * 60 + date.minute
                day_of_year = date.strftime('%j')
                return f'https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHL.06/{date.year}/{day_of_year}/3B-HHR-L.MS.MRG.3IMERG.{date.year}{date.month:02}{date.day:02}-S{date.hour:02}{date.minute:02}00-E{date.hour:02}{date.minute+29:02}59.{minutes:04}.V06B.HDF5'
        if version == 'Early' or version == 'early':
            if freq == '1D':
                return f'https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDE.06/{date.year}/{date.month:02}/3B-DAY-E.MS.MRG.3IMERG.{date.year}{date.month:02}{date.day:02}-S000000-E235959.V06.nc4'
            elif freq == '30T':
                minutes = date.hour * 60 + date.minute
                day_of_year = date.strftime('%j')
                return f'https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHE.06/{date.year}/{day_of_year}/3B-HHR-E.MS.MRG.3IMERG.{date.year}{date.month:02}{date.day:02}-S{date.hour:02}{date.minute:02}00-E{date.hour:02}{date.minute+29:02}59.{minutes:04}.V06B.HDF5'

    @staticmethod
    def get_path(save_path, title):
        if title not in os.listdir(save_path):
            os.mkdir(Path(save_path, title))
        return Path(save_path, title)

    @staticmethod
    def download_url(args):
        url, fp = args[0], args[1]
        if fp.exists():
            try:
                with h5py.File(fp, 'r') as r:
                    pass
            except:
                os.remove(fp)
        else:
            try_count = 0
            while try_count < 5:
                try:
                    result = requests.get(url, timeout=15)
                    with open(fp,'wb') as f:
                        f.write(result.content)
                    try:
                        with open(fp,'rb') as f:
                            if f.readlines()[26] == 'Service Temporarily Unavailable':
                                print(f'{url} is temporarily unavailable')
                                tm.sleep(5)
                                os.remove(fp)
                                try_count += 1
                                continue
                            else:
                                break
                    except:
                        pass
                except:
                    try_count += 1
                    print(f'Error downloading from {url}')
                    tm.sleep(2)

    def download(self):
        inputs = zip(self.urls, self.file_paths)
        results = mp.pool.ThreadPool(mp.cpu_count() - 1).imap_unordered(self.download_url, inputs)

    def download_save(self):
        lons = [i/100 for i in range(-17995, 17996, 10)]
        lats = [i/100 for i in range(-8995, 8996, 10)]
        for date in self.date:
            if f'{date.year}-{date.month:02}-{date.day:02}.hdf5' not in os.listdir(self.get_path(self.save_path, self.title)):
                datetime_ = pd.date_range(start=date, end=date + datetime.timedelta(days=1), freq=self.freq)[:-1]
                urls = [self.generate_url(dt, self.freq, self.version) for dt in datetime_]
                file_paths = [Path(self.get_path(self.save_path, f'temp_{date.year}-{date.month:02}-{date.day:02}'), f'{dt.year:04}{dt.month:02}{dt.day:02}{dt.hour:02}{dt.minute:02}.hdf5') for dt in datetime_]
                inputs = zip(urls, file_paths)
                with mp.pool.ThreadPool(5) as executor: # mp.cpu_count() - 1
                    executor.imap_unordered(self.download_url, inputs)
                    while len(os.listdir(self.get_path(self.save_path, f'temp_{date.year}-{date.month:02}-{date.day:02}'))) != len(file_paths):
                        pass
                tm.sleep(5)
                precCal = list()
                #if HQ_IR:
                #    HQprec = list()
                #    IRprec = list()
                time = list()
                for temp_file in file_paths:
                    #HQprec = 0
                    #IRprec = 0
                    with h5py.File(temp_file, 'r') as temp:
                        if self.freq == '30T':
                            temp = temp['Grid']
                            aux = temp['precipitationCal'][0, lons.index(self.bbox[0]):lons.index(self.bbox[1])+1, lats.index(self.bbox[2]):lats.index(self.bbox[3])+1]
                            precCal.append(np.where(aux > 0, aux, 0) / 2)
                            #if HQ_IR:
                            #    HQprec = temp['HQprecipitation'][0, lons.index(lon1):lons.index(lon2)+1, lats.index(lat1):lats.index(lat2)+1]
                            #    HQprec = np.where(HQprec > 0, HQprec, 0) / 2
                            #    IRprec = temp['IRprecipitation'][0, lons.index(lon1):lons.index(lon2)+1, lats.index(lat1):lats.index(lat2)+1]
                            #    IRprec = np.where(IRprec > 0, IRprec, 0) / 2
                            time.append(str(datetime.datetime.utcfromtimestamp(temp['time'][0])))
                        else:
                            precCal.append(temp['precipitationCal'][0, lons.index(self.bbox[0]):lons.index(self.bbox[1])+1, lats.index(self.bbox[2]):lats.index(self.bbox[3])+1])
                            #if HQ_IR:
                            #    HQprec = temp['HQprecipitation'][0, lons.index(lon1):lons.index(lon2)+1, lats.index(lat1):lats.index(lat2)+1]
                            #    IRprec = temp['IRprecipitation'][0, lons.index(lon1):lons.index(lon2)+1, lats.index(lat1):lats.index(lat2)+1]
                            time.append(temp.attrs['BeginDate'])
                with h5py.File(Path(self.get_path(self.save_path, self.title), f'{date.year}-{date.month:02}-{date.day:02}.hdf5'), 'w') as r_file:
                    r_file.create_dataset('precipitationCal', data=np.array(precCal))
                    #if HQ_IR:
                    #    r_file.create_dataset('HQprecipitation', data=np.array(HQprec))
                    #    r_file.create_dataset('IRprecipitation', data=np.array(IRprec))
                    r_file.create_dataset('time', data=np.array(time).astype(h5py.string_dtype(encoding='utf-8')))
                    r_file.create_dataset('lon', data=np.array([i/100 for i in range(int(self.bbox[0]*100), int(self.bbox[1]*100)+1, 10)]))
                    r_file.create_dataset('lat', data=np.array([i/100 for i in range(int(self.bbox[2]*100), int(self.bbox[3]*100)+1, 10)]))
                #if HQ_IR:
                #    HQprec = list()
                #    IRprec = list()
                shutil.rmtree(self.get_path(self.save_path, f'temp_{date.year}-{date.month:02}-{date.day:02}'))
                print(f'{date.year}-{date.month:02}-{date.day:02}')

class Savemap:
    """Main class for saving coloured maps.
    """
    def __init__(
        self,
        path=os.getcwd(), name='image', data=None, coords=None, vmax=None, bounds=None, colours=None, cmap=None,
        points=None, points_values=None, points_cmap='viridis', points_bounds=None, points_scale_factor=10, cb_points=True,
        rect=None,
        texts=None, texts_coords=None,
        llcrnrlat=-60, urcrnrlat=-20, llcrnrlon=-77, urcrnrlon=-50,
    ):
        self.path = path
        self.name = name
        if '{}.png'.format(name) not in os.listdir(path):
            """----------Figure creation----------"""
            projection_crs = ccrs.PlateCarree()
            self.fig = plt.figure(figsize=(4,5), dpi=300)
            self.ax = self.fig.add_subplot(1, 1, 1, projection=projection_crs)
            self.ax.set_extent([llcrnrlon, urcrnrlon, llcrnrlat, urcrnrlat], crs=projection_crs)
            gl = self.ax.gridlines(draw_labels=True, linewidth=0.3, linestyle='--', alpha=0.5, dms=True)
            gl.top_labels    = False
            gl.right_labels  = False
            gl.xlabel_style  = {'size': 5}
            gl.ylabel_style  = {'size': 5}
            provinces = list(shpreader.Reader(Path(Path(os.getcwd()).parent, 'natural_earth_data', '10m_cultural', 'ne_10m_admin_1_states_provinces.shp')).geometries())
            lakes     = list(shpreader.Reader(Path(Path(os.getcwd()).parent, 'natural_earth_data', '10m_physical', 'ne_10m_lakes.shp')).geometries())
            countries = list(shpreader.Reader(Path(Path(os.getcwd()).parent, 'natural_earth_data', '10m_cultural', 'ne_10m_admin_0_countries.shp')).geometries())
            """--------Data representation--------"""
            if data is not None:
                self.colormap(self.fig, self.ax, data, coords, vmax, bounds, colours, cmap)
            """--------Text representation--------"""
            if (texts is not None) and (texts_coords is not None):
                self.set_text(self.ax, texts, texts_coords)
            """-------Points representation-------"""
            if points is not None and (type(points) == np.ndarray):
                self.draw_points(self.fig, self.ax, points, points_values, points_cmap, points_bounds, points_scale_factor, cb_points)
            elif points is not None:
                raise TypeError('Variable points must be a numpy.array with dtype float64 or int32.')
            """------Rectangle representation-----"""
            if rect is not None:
                self.draw_rectangle(self.ax, rect)
            """------------Save figure------------"""
            self.ax.add_geometries(provinces, projection_crs, edgecolor='black', facecolor='none', linewidth=0.2, linestyle=':')
            #self.ax.add_geometries(lakes    , projection_crs)
            self.ax.add_geometries(countries, projection_crs, edgecolor='black', facecolor='none', linewidth=0.4)
            self.fig.savefig('{}\\{}.png'.format(path, name))
            plt.close()
    
    def __str__(self):
        return f'Figure {self.name} saved in path {self.path}.'

    @staticmethod
    def colormap(fig, ax, data, coords, vmax, bounds, colours, cmap):
        if colours == None:
            colours = ['#004d00', '#339933', '#53c653', '#73e600', '#e6e600', '#ff9900', '#ff471a', '#993333', '#4d1919']
        if bounds == None:
            bounds = np.quantile(data, (0,.1,.2,.3,.4,.5,.6,.7,.8,.95))
        if vmax == None:
            vmax = bounds[-1]
        lon_grid, lat_grid = np.meshgrid(coords[0], coords[1])
        if cmap == None:
            cmap = mpl.colors.ListedColormap(colours)
            norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=len(bounds)-1)
            img     = ax.pcolormesh(coords[0],
                                    coords[1],
                                    ma.masked_array(data, globe.is_ocean(lat_grid, lon_grid)),
                                    cmap=cmap,
                                    norm=norm,
                                   )
        else:
            img     = ax.pcolormesh(coords[0],
                                    coords[1],
                                    ma.masked_array(data, globe.is_ocean(lat_grid, lon_grid)),
                                    cmap=cmap,
                                    vmax=vmax,
                                   )
        cax, kw = mpl.colorbar.make_axes(ax, 
                                         location='right',
                                         pad=0.05,
                                         shrink=0.95,
                                         aspect=30
                                        )
        cb      = fig.colorbar(img,
                               cax=cax,
                               boundaries=bounds,
                               spacing='proportional',
                               extend='both',
                               **kw
                              )
        cb.ax.tick_params(labelsize=5)

    @staticmethod
    def set_text(ax, texts, texts_coords):
        if (type(texts) == type(list())) and (type(texts_coords) == type(list())):
            if len(texts) == len(texts_coords):
                for i in range(len(texts)):
                    if len(texts_coords[i]) == 2 and type(texts_coords[i][0]) == type(float()) and type(texts_coords[i][1]) == type(float()):
                        ax.text(x=texts_coords[i][0], y=texts_coords[i][1], s=texts[i], fontsize=4)
                    else:
                        raise ValueError('List texts_coords items must be lists of length 2 with the x or longitud in the first item and the y or latitude in the second item as floats.')
            else:
                raise ValueError('Length of lists texts and texts_coords must be the same.')
        else:
            raise TypeError('Variables texts and texts_coords must be lists.')

    @staticmethod
    def draw_points(fig, ax, points, points_values, points_cmap, points_bounds, scale_factor, cb_points=True):
        """
        
        Plot a specified location (np.ndarray [lon, lat]) or locations (np.ndarray [[lon_1, lat_1],[...]])

        """
        if (points.dtype == 'float64' or points.dtype == 'int32'):
            if len(points.shape) == 1:
                if points_values is None:
                    points_values = 2
                elif (type(points_values) != type(int())) or (type(points_values) != type(float())):
                    raise TypeError('Variable points_values must be a float or int for a single point.')
                ax.plot(points[0], points[1], marker='o', markersize=points_values, color='#000066')
            elif len(points.shape) == 2:
                if points_values is None:
                    points_values = np.array([2 for _ in range(points.shape[0])])
                elif type(points_values) == np.ndarray:
                    if (points_values.dtype != 'float64') and (points_values.dtype != 'int32'):
                        raise TypeError('Variable points_values must be a numpy.array with dtype float64 or int32 for several points.')
                else:
                    raise TypeError('Variable points_values must be a numpy.array with dtype float64 or int32 for several points.')
                if points_bounds == None:
                    vmin  = None
                    vmax  = None
                    ticks = None
                else:
                    vmin  = points_bounds[0]
                    vmax  = points_bounds[-1]
                    ticks = [points_bounds[0], (points_bounds[0]+points_bounds[-1])/2, points_bounds[-1]]
                img = ax.scatter(points[:,0], points[:,1], marker='o', s=np.abs(scale_factor*points_values), c=points_values, cmap=points_cmap, vmin=vmin, vmax=vmax)
                if cb_points:
                    cax, kw = mpl.colorbar.make_axes(ax, 
                                                     location='bottom',
                                                     pad=0.05,
                                                     shrink=0.8,
                                                     aspect=30
                                                    )
                    cb      = fig.colorbar(img,
                                           cax=cax,
                                           boundaries=points_bounds,
                                           ticks=ticks,
                                           spacing='uniform',
                                           **kw
                                          )
                    cb.ax.tick_params(labelsize=5)
            else:
                raise ValueError('Shape of variable points must be 1 for a single point or 2 for several points.')
        else:
            raise TypeError('Variable points must be a numpy.array with dtype float64 or int32.')

    @staticmethod
    def draw_rectangle(ax, rect):
            if type(rect) == np.ndarray:
                if len(rect.shape) == 1:
                    x, y = [[rect[0],rect[0],rect[2],rect[2],rect[0]], [rect[1],rect[3],rect[3],rect[1],rect[1]]]
                    ax.plot(x, y, marker=None, color='blue')
                elif len(rect.shape) == 2:
                    for r in rect:
                        x, y = [[r[0],r[0],r[2],r[2],r[0]], [r[1],r[3],r[3],r[1],r[1]]]
                        ax.plot(x, y, marker=None, color='blue')
                else:
                    pass
            else:
                pass
    
    @staticmethod
    def GIF_data(path, file_name, path_data, duration=1.5):
        """Create a GIF with the data
        """
        if file_name not in os.listdir(path):
            with imageio.get_writer('{}\\{}.gif'.format(path, file_name), mode='I', duration=duration) as writer:
                for filename in os.listdir(path_data):
                    image = imageio.imread('{}\\{}'.format(path_data, filename))
                    writer.append_data(image)