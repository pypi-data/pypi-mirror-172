import radiens.api.api_allego as api
from radiens.utils.constants import (CORE_ADDR, PCACHE_ADDR,
                                         PRIMARY_CACHE_STREAM_GROUP_ID)


class AllegoClient:
    """A python API for allego
    """
    def __init__(self):
        """
        """

        self.samp_freq = None



    # ======= getters =======
    def get_status(self):
        """
        Gets the status of Allego.

        Returns:
            status (dict): has keys 'streaming' and 'recording' that map to dictionaries describing their respective status

        Example: 
            >>> client.get_status()
            {'recording': {'active_filename': 'allego_0__uid1020-00-53-02',
                        'duration': 0.0,
                        'error': '',
                        'mode': 'off'},
            'streaming': {'hardware_memory': 0.0, 'mode': 'off', 'time_range': [0.0, 0.0]}}
        """
        return api.get_status(CORE_ADDR)

    def get_config(self):
        """
        Gets the configuration of Allego.

        Returns:
            config (dict): has various keys relating to the configuration

        Example:
            >>> client.get_config()
            {'backbone_mode': 'SMARTBOX_SIM_GEN_SPIKES',
            'base_samp_freq': 20000.0,
            'headstage_cable_lens': {'A': 3.0,
                                    'B': 3.0,
                                    'C': 3.0,
                                    'D': 3.0,
                                    'E': 3.0,
                                    'F': 3.0,
                                    'G': 3.0,
                                    'H': 3.0},
            'stream_loop_dur_ms': 200,
            'system_server_port': ':50051'}

        """

        config = api.get_config(CORE_ADDR)
        self.samp_freq = config['base_samp_freq']

        return config
    
    def get_signal_group(self):
        """
        Gets the signal group (channel metadata).

        Returns:
            signal_group (SignalGroup): object containing metadata information for all channels

        """
        return api.get_signal_group(CORE_ADDR, PRIMARY_CACHE_STREAM_GROUP_ID)

    def get_signals(self):
        """
        Gets the the most recent signals since last call of itself or :py:meth:`set_time_to_cache_head`.

        Returns:
            sigarray (ndarray[numpy.float32]): raw signal data; the mapping contained in signal_group (see :py:meth:`get_signal_group`)
            time_range (list[float]): time range (in seconds) of sigarray
        """
        if self.samp_freq is None:
            self.samp_freq = api.get_config(CORE_ADDR)['base_samp_freq']

        return api.get_signals(PCACHE_ADDR, PRIMARY_CACHE_STREAM_GROUP_ID, self.samp_freq)

    def get_digital_out_states(self):
        """
        Gets digital out state.

        Returns:
            dout_state_dict (dict): has keys 'digital_outs_mode' and 'states'.

        Example:
            >>> client.get_digital_out_states()
            {'digital_outs_mode': 'manual',
            'states': [{'chan_idx': 0, 'state': True}, {'chan_idx': 1, 'state': False}]}
        """
        return api.get_digital_out_states(CORE_ADDR)

    # ======= setters =======
    def set_time_to_cache_head(self):
        """
        Sets current time to most recent time point in signal cache.

        This should be called before the first call of :py:meth:`get_signals`. the first call of :py:meth:`get_signals` 
        will return the new signals since the last call to :py:meth:`set_time_to_cache_head` 
        """
        return api.set_time_to_cache_head(PCACHE_ADDR, PRIMARY_CACHE_STREAM_GROUP_ID)

    def set_digital_out_manual(self, dout1_state: bool, dout2_state: bool):
        """
        Sets digital out state.

        Parameters:
            dout1_state (bool): new dout 1 state
            dout2_state (bool): new dout 2 state

        """
        return api.set_digital_out_manual(CORE_ADDR, dout1_state, dout2_state)


