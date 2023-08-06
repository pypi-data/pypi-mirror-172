from pathlib import Path

import grpc
import numpy as np
import radiens.api.api_utils as ul
from radiens.exceptions.grpc_error import handle_grpc_error
from radiens.grpc import common_pb2, datasource_pb2, radiensserver_pb2_grpc
from radiens.grpc.common_pb2 import RadixFileTypes
from radiens.utils.config import new_server_channel

CLIENT_NAME = 'Videre'

# ====== getters ======
def list_dir(addr, directory):
    _directory = str(Path(directory).expanduser().resolve())
    with new_server_channel(addr) as chan:
        RadiensCoreStub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        req = common_pb2.ListDataSourcesRequest()
        req.directory=_directory

        try:
            res = RadiensCoreStub.ListDirectory(req)
            
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        else:
            return ul.parse_CpRmMvLsReply(res)

def load_dataset(addr, base_name_path):
    _base_name_path = Path(base_name_path).expanduser().resolve()
    parent_path = str(_base_name_path.parent)
    base_name = _base_name_path.stem
    contents = list_dir(addr, parent_path)
    if contents['num_dsource'] == 0:
        raise Exception #TODO: handle this
    for desc in contents['data_source_info']['descriptor']:
        if desc['base_name'] == base_name:
            with new_server_channel(addr) as chan:
                RadiensCoreStub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
                req = datasource_pb2.DataSourceSetSaveRequest()
                req.path = parent_path
                req.baseName = base_name
                req.fileType = RadixFileTypes.Value(desc['file_type'].upper())
                
                try:
                    res = RadiensCoreStub.SetDataSourceFromFile(req)
                except grpc.RpcError as ex:
                    handle_grpc_error(ex, CLIENT_NAME)
                else:
                    return ul.parse_data_source_set_save_reply(res)


def get_signals(addr, dsource_id: str, time_range):
    with new_server_channel(addr) as chan:
        stub = radiensserver_pb2_grpc.RadiensCoreStub(chan)
        req = common_pb2.HDSnapshotRequest(timeRange=time_range)
        req.streamGroupId=dsource_id
        try:
            raw = stub.GetHDSnapshot(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        else:
            sigarray = np.frombuffer(raw.signals.data, dtype=np.float32)
            sigs = np.reshape(sigarray, (raw.signals.shape[0], raw.signals.shape[1]))

        return sigs
