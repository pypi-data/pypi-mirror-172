"""

Libraries

"""

import sys, os
sys.path.insert(0, os.getcwd())
from precipitation.libraries import *
from precipitation.geo_tools import *
from precipitation.FACETA import *
from precipitation.hidro_tools import *

"""

Methods

"""

def create_hdf5_file_daily(raw_file, mode):
    paths = [
        'e:\\GPM IMERG Early Precipitation L3 1 day 0.1 degree x 0.1 degree (GPM_3IMERGDE)',
        'e:\\GPM IMERG Late Precipitation L3 1 day 0.1 degree x 0.1 degree V06 (GPM_3IMERGDL)',
        'e:\\GPM IMERG Final Precipitation L3 1 day 0.1 degree x 0.1 degree (GPM_3IMERGDF)',
    ]
    products = ['GPM_IMERG_Early', 'GPM_IMERG_Late', 'GPM_IMERG_Final']
    information = {
        'description' : [
            'Near real-time low-latency gridded global multi-satellite precipitation estimates',
            'Near real-time gridded global multi-satellite precipitation estimates with quasi-Lagrangian time interpolation',
            'Research-quality gridded global multi-satellite precipitation estimates with quasi-Lagrangian time interpolation, gauge data, and climatological adjustment',
        ],
        'dates_covered' : [
            'June 2000 - Present',
            'June 2000 - Present',
            'June 2000 - Sept. 2021 (next update currently scheduled for Jul. 2022)',
        ],
        'minimum_latency' : ['4 hours', '12 hours', '3.5 Months'],
        'spatial_resolution' : ['10km / 0.1 Degree', '10km / 0.1 Degree', '10km / 0.1 Degree'],
        'algorithm_version' : ['V06B', 'V06B', 'V06B']
    }
    with h5py.File(raw_file, mode) as file:
        for i in range(3):
            if products[i] not in file.keys():
                file_ = os.listdir(paths[i])[0]
                with h5py.File(Path(paths[i], file_), 'r') as r_file:
                    file.create_dataset(f'/{products[i]}/precipitationCal', data=r_file['precipitationCal'][:].T, chunks=(150, r_file['lat'].shape[0], 5), maxshape=(None, None, None))
                    file.create_dataset(f'/{products[i]}/time', data=r_file['time'][:], chunks=True, maxshape=(None, ))
                    file.create_dataset(f'/{products[i]}/lon', data=r_file['lon'][:])
                    file.create_dataset(f'/{products[i]}/lat', data=r_file['lat'][:])
                    file[products[i]].attrs['description']        = information['description'][i]
                    file[products[i]].attrs['dates_covered']      = information['dates_covered'][i]
                    file[products[i]].attrs['minimum_latency']    = information['minimum_latency'][i]
                    file[products[i]].attrs['spatial_resolution'] = information['spatial_resolution'][i]
                    file[products[i]].attrs['algorithm_version']  = information['algorithm_version'][i]
                for file_ in tqdm(os.listdir(paths[i])[1:]):
                    with h5py.File(Path(paths[i], file_), 'r') as r_file:
                        time_resize = r_file['time'].shape[0]
                        group = file[f'/{products[i]}']
                        group['precipitationCal'].resize((group['precipitationCal'].shape[2] + time_resize), axis=2)
                        group['precipitationCal'][:, :, -time_resize:] = r_file['precipitationCal'][:].T
                        group['time'].resize((group['time'].shape[0] + time_resize, ))
                        group['time'][-time_resize:] = r_file['time'][:]

def pmp_calc_hdf(dataset_name, hdf_group):
    """Calculate probable maximum precipitation.
    """
    if 'pmp' not in hdf_group.keys():
        if dataset_name in hdf_group.keys():
            if f'statistics_{dataset_name}' in hdf_group.keys():
                if 'mean' and 'std' and 'cv' in hdf_group[f'statistics_{dataset_name}'].keys():
                    phi_pmp = 5.2253*np.exp(1.958*hdf_group[f'statistics_{dataset_name}']['cv'][:])
                    pmp     = hdf_group[f'statistics_{dataset_name}']['mean'][:] + hdf_group[f'statistics_{dataset_name}']['std'][:]*phi_pmp
                    hdf_group.create_dataset(
                        'pmp',
                        data=np.transpose(np.array([phi_pmp, pmp]), axes=(1,2,0))
                    )
                    hdf_group['pmp'].attrs['-'] = ['phi_pmp', 'pmp']
                else:
                    raise KeyError('Calculate statistics first.')
            else:
                raise KeyError('Calculate statistics first.')
        else:
            raise KeyError('Data does not exist in the given group.')



"""

Classes

"""

