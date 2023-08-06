# Hidro UNC

Test version.

0.0.11
	- Change in Precipitation_test class:
		- staticmethod trend_mann_kendall_DataArray change from 
		"return(da.name, 'Se acepta con una confianza del 95%.', 'No se observa tendencia.')" to 
		"return([da.name, 'Se acepta con una confianza del 95%.', 'No se observa tendencia.', result])".

		- "result" was added to all the return fuctions of trend_mann_kendall_DataArray.

		- __init__ change from
		"self.da_o, self.da_ = self.outliers_chow_DataArray(da)[:2]" to
		"self.da_o, self.da_, self.o_res = self.outliers_chow_DataArray(da)".

0.0.12
	- Change in Precipitation_test class:
		- added staticmethods:
			- trend_mann_kendall_DataArray_hamed_rao
			- trend_mann_kendall_DataArray_trend_free_pre_whitening
			- trend_mann_kendall_DataArray_sens_slope

0.0.13
	- Change in Precipitation_test class:
		- added 0 filter in independence_anderson_DataArray.

0.0.14
	- Change in Precipitation_test class:
		- change trend_mann_kendall_DataArray_pre_whitening to trend_mann_kendall_DataArray_trend_free_pre_whitening.
		- independence_anderson_DataArray is deactivated.
		- independence_wald_wolfowitz_DataArray work in progress.

0.0.15
	- Change in Precipitation_test class:
		- independence_anderson_DataArray is reactivated.
		- added if you want to applied the tests with or without outliers from outliers_chow_DataArray.

0.0.16
	- Change in Precipitation_test class:
		- added some options to choose whether a test is applied or not.
		- name of staticmethod signed_rank_wilcoxon change to signed_rank_wilcoxon_DataArray.
		- all Mann Kendall's tests were joined in a unique staticmethod replacing the staticmethod trend_mann_kendall_DataArray.
		- added the pre_whitening_modification_test to Mann Kendall's results.
	
	0.0.16.1 - 2
		- Error correction.

0.0.17
	- Change in Precipitation_test class:
		- added the posibility to use the independence_wald_wolfowitz_DataArray test.
	- Change in xarray_tools.py:
		- added Wald Wolfowitz's test for xarray.Dataset and a list of xarray.Dataset.
	
	0.0.17.1 - 2 - 3 - 4 - 5 - 6 - 7
		- Error correction.

0.0.18
	- Change in Precipitation_test class:
		- added the posibility to use the homogeneity_pettitt_DataArray test.
	- Change in xarray_tools.py:
		- added Pettitt's test for xarray.Dataset and a list of xarray.Dataset.
	
	0.0.18.1 - 2
		- Error correction.

0.0.19
	- Change in Precipitation_test class:
		- added 1% alpha for Mann Kendall's tests.

0.0.20
	- Change in Precipitation_test class:
		- added confidence intervals for Sen's slope in Mann Kendall's tests.
	
	0.0.20.1 - 2
		- Error correction.

0.0.21
	- Change in Precipitation_Analysis:
		- deleted the option to analize climate indexes for durations higher than a day.

0.0.22
	- Change in Precipitation_test_geo in geo_tools.py:
		- added multiprocessing python for better performance.
	
	0.0.22.1 - 2 - 3 - 4
		- Error correction.

0.0.23
	- Replaced save_map method for Savemap class.
	
	0.0.23.1 - 2 - 3 - 4 - 5 - 6
		- Error correction.

0.0.24
	- Change in geo_tools.py:
		- added a new class for getting IMERG maximums from an hdf5 file.
	
	0.0.24.1 - 2
		- Error correction.

0.0.25
	- Change in geo_tools.py:
		- added a new class for getting IMERG statistical tests reading from an hdf5 file.
	
	0.0.25.1 - 2 - 3
		- Error correction.

0.0.26
	- Change in geo_tools.py:
		- Savemap class change from receiving a xarray.Dataarray to a numpy.array and a numpy.array with longitude in index 0 and latitude in index 1.
	
	0.0.26.1 - 2 - 3
		- Error correction.
	
	0.0.26.4
		- Stop drawing lakes in maps.
	
	0.0.26.5
		- Error correction.

0.1.0
	- Total rework starts:
		- Deleted xarray_tools.py
		- hidro_tools.py: 
			- Precipitation_Analysis rework for receiving numpy.array objects and time with datetime library.
	
	0.1.0.1
		- Sweeping up the garbage.
	
	0.1.0.2
		- Error correction.

0.1.1
	- Rework of Precipitation_test class

0.1.2
	- Rework of Probability Distribution Functions classes
	
	0.1.2.1
		- Error correction.

0.1.3
	- geo_tools.py
		- Added the option to download IMERG Late product

0.1.4
	- Added some reviewed methods and classes.
	
	0.1.4.1
		- Error correction.
	
	0.1.4.2
		- Get sum from 0 to 0 for half hourly IMERG.
	
	0.1.4.3 - 4
		- Error correction.

0.1.5
	- Added the option to download half hourly Late and Early IMERG products.
	
	0.1.5.1 - 2 - 3
		- Error correction.
	
	0.1.5.4
		- Error correction, added IMERG download timeout of 15 seconds.
	
	0.1.5.5 - 6 - 7 - 8 - 9 - 10
		- Error correction.

0.1.6
	- Added Percentage Error function to FACETA.py and to all the distribution classes.
	- Change the distribution classes to not calculate the bias indexes until call with goodness_fit method.

0.1.7
	- Change the name of Precipitation_Analysis to Rainfall_Indices and changed its funcionalities.

0.1.8
	- Change the name of Precipitation_test to Statictical_Tests and changed its funcionalities.

	0.1.8.1 - 2
		- Error correction.

0.1.9
	- Updated search_loc function.
	
	0.1.9.1 - 2 - 3
		- Error correction.

0.1.10
	- Updated Rainfall_Indices class.
	- Created the Rain_Gauge class in hidro_tools.py.
	- Updated index from README.md.
	
	0.1.10.1
		- Error correction.

# Index

precipitation

	hidro_tools.py
	
		Methods

			None

		Classes

			Rainfall_Indices(time, data, axis=0, period=['Y'], start_month=7)
			Rain_Gauge(path_csv=None)

	FACETA.py
	
		Methods

			weibull_distribution(da)
			chi2(obs, cdf, n_params)
			standard_error(obs, est, n_params=0)
			percentage_error(obs, est, _abs=True)
			FACETA_excel(file)

		Classes

			Statictical_Tests(data, axis=0, without_outliers=True, iAN=True, iWW=True, tMK=True, sWI=True, hPE=True)
			LogNormal_MV(data)
			GEV_MV(data)
			GEV_MM(data)
			Gumbel_MV(data)
			Gumbel_MM(data)
			LogPearson3_MM(data)

	geo_tools.py

		Methods

			open_IMERG(path, folder, lon1, lon2, lat1, lat2)
			etopo(lon_new, lat_new, engine='netcdf4')
			search_loc(lons_, lats_, lons, lats)

		Classes

			Download_IMERG(start_date, end_date, freq, version, lon1, lon2, lat1, lat2, save_path, HQ_IR=False)
			Savemap(path=os.getcwd(), name='image', data=None, coords=None, vmax=None, bounds=None, colours=None, cmap=None, points=None, points_values=None, points_cmap='viridis', points_bounds=None, points_scale_factor=10, cb_points=True, rect=None, texts=None, texts_coords=None, llcrnrlat=-60, urcrnrlat=-20, llcrnrlon=-77, urcrnrlon=-50)

	h5py_tools.py

		Methods

			create_hdf5_file_daily(raw_file, mode)
			pmp_calc_hdf(dataset_name, hdf_group)

		Classes

			None