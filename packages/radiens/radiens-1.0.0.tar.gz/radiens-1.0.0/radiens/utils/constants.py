from pathlib import Path

DEFAULT_IP = 'localhost'
DEFAULT_HUB = 'default'


# ports
ALLEGO_CORE_PORT = 50051
PCACHE_PORT = 50052
KPI_PORT = 50053
NEURONS1_PORT = 50054

# default server addresses
CORE_ADDR = '{}:{}'.format(DEFAULT_IP, ALLEGO_CORE_PORT)
PCACHE_ADDR = '{}:{}'.format(DEFAULT_IP, PCACHE_PORT)
KPI_ADDR = '{}:{}'.format(DEFAULT_IP, KPI_PORT)
NEURONS1_ADDR = '{}:{}'.format(DEFAULT_IP, NEURONS1_PORT)


# services
CORE_SERVICE = 'core'
PCACHE_SERVICE = 'pcache'

# only allego stream group
PRIMARY_CACHE_STREAM_GROUP_ID = 'Live Signals'

# default datasource paths
DATASOURCE_PATHS = {
            'dsrc_path': Path(Path.home(), 'radix', 'data'),
            'dsrc_type': 'xdat',
            'dsrc_name': 'sbpro'
}

# ports/signals
PORT_ENUM = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
SIGNAL_TYPE_ENUM = {0: 'amp', 1: 'adc', 2: 'din', 3: 'dout'}
SIGNAL_TYPES = ['amp', 'adc', 'din', 'dout']

# backbone
BACKBONE_MODE = {
    'SMARTBOX_PRO': 0,
    'SMARTBOX_SIM_GEN_SINE': 1,
    'SMARTBOX_SIM_GEN_SPIKES': 2,
    'SMARTBOX_SIM_DATASOURCE': 3,
}
BACKBONE_MODE_OUT = {
    0: 'SMARTBOX_PRO',
    1: 'SMARTBOX_SIM_GEN_SINE',
    2: 'SMARTBOX_SIM_GEN_SPIKES',
    3: 'SMARTBOX_SIM_DATASOURCE',
}
DOUT_MODE_OUT = {
    0: 'manual',
    1: 'events',
    2: 'gated'
}

# stream/record
STREAM_MODE = {'S_OFF': 0, 'S_ON': 1}
RECORD_MODE = {'R_OFF': 0, 'R_ON': 1}
STREAM_MODE_OUT = {0: 'S_OFF', 1: 'S_ON'}
RECORD_MODE_OUT = {0: 'R_OFF', 1: 'R_ON'}
