import radiens.api.api_videre as api
import radiens.utils.config as cfg
from radiens.utils.constants import CORE_SERVICE, DEFAULT_HUB, DEFAULT_IP


class VidereClient:
    """
    A python API for Videre
    """
    def __init__(self):
        """
        """
        self.__core_port = cfg.get_radiens_core_port()
        self.hubs = {DEFAULT_HUB: {'ip_address': DEFAULT_IP, 'port': self.__core_port}}
        self.dataset_map = {}

    def add_hub(self, new_hub):
        # Add a hub (ip address of videre server)
        #   Args:
        #       hub : dict 
        #           key(s) (str): hub name(s)
        #           values (dict): {'ip_address': ip_address}
        for k in new_hub:
            if 'ip_address' in new_hub[k]:
                self.hubs[k] = {
                    'ip_address': new_hub[k]['ip_address'],
                    'port': new_hub[k]['port'] if 'port' in new_hub[k] else self.__core_port
                }
        
    def __server_address(self, hub_name, service):
        # creates server address from hub and service
        if service == 'core':
            return '{}:{}'.format(self.hubs[hub_name]['ip_address'], self.hubs[hub_name]['port'])
        else:
            raise AssertionError('invalid service name = {}'.format(service))



    # ======= API start =======
    def list_dir(self, directory, hub_name=DEFAULT_HUB):
        """
        list datasets from specified directory

        Parameters: 
            directory (Union[str, pathlib.PosixPath]): path to directory that contains dataset(s)

        Returns:
            datasets (dict): dictionary with metadata pertaining to all datasets in requested directory

        Example:
            >>> client.list_dir("Users/example/recording_data")
            {'data_source_info': {'descriptor': [{'base_name': 'allego_0__uid0823-10-56-41',
                                                'file_type': 'xdat',
                                                'path': 'Users/example/recording_data/'},
                                                {'base_name': 'allego_0__uid1014-15-03-32',
                                                'file_type': 'xdat',
                                                'path': 'Users/example/recording_data/'}],
                                'stat': [{'dataset_checksum': '62daa95366c8760122ea0706e141a67f991ee1c5605a98596c0ae859231e2683',
                                            'dataset_uid': 'ce7f4a7e-bb50-4e6b-ad0d-3ab0c5a8ea5e',
                                            'duration_sec': 14.8032,
                                            'is_meta_data_file': True,
                                            'num_bytes': 47455590,
                                            'num_bytes_meta_data': 85350,
                                            'num_bytes_primary_data': 47370240,
                                            'num_channels': 38,
                                            'num_files': 3,
                                            'sample_freq': 20000,
                                            'time_stamp': {'nanos': 53210000,
                                                        'seconds': 1661266601}},
                                        {'dataset_checksum': '9ae779f46e38a6589b84594c07f62c5f5797f13e61a1481d41f862b956c96de2',
                                            'dataset_uid': '348d18dc-e5b5-4046-8fae-d0e4f2f53566',
                                            'duration_sec': 16.5952,
                                            'is_meta_data_file': True,
                                            'num_bytes': 53189991,
                                            'num_bytes_meta_data': 85351,
                                            'num_bytes_primary_data': 53104640,
                                            'num_channels': 38,
                                            'num_files': 3,
                                            'sample_freq': 20000,
                                            'time_stamp': {'nanos': 705758000,
                                                        'seconds': 1665777812}}]},
            'dest_path': 'Users/example/recording_data',
            'msg': '',
            'num_bytes': 100645581,
            'num_dsource': 2,
            'num_files': 6}

        You can access dataset/recording information via the ``'data_source_info'`` key of the returned **datasets** dictionary. Said key
        maps to another dictionary with keys ``'descriptor'`` and ``stat`` describing various metadata. 

        Notice that there are 2 data sources (``'num_dsource'``) but 6 files total (``num_files``). This is because an xdat recording
        corresponds to 3 files with suffixes ``*.xdat.json``, ``*_data.xdat``, ``*_timestamp.xdat``.
        """
        return api.list_dir(self.__server_address(hub_name, CORE_SERVICE), directory)

    def load_dataset(self, base_name_path, hub_name=DEFAULT_HUB):
        """
        Loads a dataset on Videre 

        Parameters: 
            base_name_path (Union[str, pathlib.PosixPath]): full path and base name (no extension) to dataset

        Returns:
            dataset_id (str)

        Side effects:
            Sets value of ``dataset_id`` as key in ``dataset_map`` attribute on client. See the following example.
        
        Example:
            >>> dataset_id = client.load_dataset("/Users/example/recording_data/allego_0__uid0823-10-56-41")
            >>> client.dataset_map[dsource_id]
            {'base_name': 'allego_0__uid0823-10-56-41',
            'duration': 14.8032,
            'file_type': 'xdat',
            'num_chans': {'aux': 2, 'din': 2, 'dout': 2, 'pri': 32},
            'samp_freq': 20000.0,
            'shape': [296064, 38],
            'time_range': [0.0, 14.8032],
            'time_stamp_range': [0, 296064]}
            
        """
        dataset = api.load_dataset(self.__server_address(hub_name, CORE_SERVICE), base_name_path)
        dataset_id = dataset['dsourceID']
        status = dataset['status']
        self.dataset_map[dataset_id] = {
            'samp_freq': status['samp_freq'], 'base_name': status['base_file_name'],
            'file_type': status['file_type'], 'time_range': status['time_range'], 
            'shape': status['shape'], 'duration': status['duration'], 
            'num_chans': status['signal_group'].num_sigs, 'time_stamp_range': status['time_stamp_range']}
        return dataset_id


    def get_signals(self, dataset_id, time_range, hub_name=DEFAULT_HUB):
        """
        Gets the the signals for specified time range

        Parameters: 
            dataset_id (str): can be obtained from :py:meth:`load_dataset`
            time_range (list[float])

        Returns:
            sigarray (ndarray[numpy.float32]): raw signal data; the mapping contained in signal_group (see :py:meth:`get_signal_group`)
            time_range (list[float]) 
        """
        
        return api.get_signals(self.__server_address(hub_name, CORE_SERVICE), dataset_id, time_range)


