import grpc
import numpy as np
from radiens.exceptions.grpc_error import handle_grpc_error
from radiens.grpc import (allegoserver_pb2, allegoserver_pb2_grpc,
                              common_pb2)
from radiens.signal_group.SignalGroup import SignalGroup
from radiens.utils.config import new_server_channel
from radiens.utils.constants import BACKBONE_MODE_OUT, DOUT_MODE_OUT

CLIENT_NAME = 'Allego'


# ====== getters ======
def get_config(addr):
    with new_server_channel(addr) as chan:
        AllegoCoreStub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            res = AllegoCoreStub.GetConfig(common_pb2.StandardRequest())
            
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        else:
            cable_dict = {}
            for p in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
                try:
                    cable_dict[p] = eval('res.cableLengths.{}'.format(p))
                except AttributeError:
                    pass
            return {'system_server_port': res.allegoCoreServerPort,
                    'base_samp_freq': res.baseSampFreq,
                    'stream_loop_dur_ms': res.streamLoopDurMs,
                    'headstage_cable_lens': cable_dict,
                    'backbone_mode': BACKBONE_MODE_OUT[res.backboneMode]}

def get_status(addr):
    with new_server_channel(addr) as chan:
        AllegoCoreStub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            res = AllegoCoreStub.GetStatus(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        else:
            return {'streaming': {'mode': 'on' if res.streaming.streamMode == 1 else 'off',
                                'time_range': [res.streaming.primaryCacheTRange[0], res.streaming.primaryCacheTRange[1]],
                                'hardware_memory': res.streaming.hardwareMemoryLevel},
                    'recording': {'mode': 'on' if res.recording.recordMode == 1 else 'off',
                                'active_filename': res.recording.activeFileName,
                                'duration': res.recording.duration,
                                'error': res.recording.error}}
        
def get_signal_group(addr, stream_group_id=None):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan)
        try:
            req = common_pb2.SignalGroupIDRequest()
            req.streamGroupId=stream_group_id

            raw = stub.GetSignalGroup(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        else: 
            return SignalGroup(raw)

def get_signals(addr, stream_group_id: str, samp_freq: float):
    sigarray = []; time_range = []
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Pcache1Stub(chan) 
        req = common_pb2.GetSignalsRequest(streamGroupId=stream_group_id, params=common_pb2.GetSignalsRequest.GetSigsParams(timeRange=[]))
        req.params.timeWindow=1
        req.params.spacing=0
        req.params.magnitude=-1
        req.params.plotWidthPoints=samp_freq
        req.params.gpioOnTop=False
        req.params.auxMagnitude=-1
        req.params.componentID='allego_python_client'
        
        try:
            raw = stub.GetSignals(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        else:
            sigarray = np.frombuffer(raw.data, dtype=np.float32)
            sigarray = np.reshape(sigarray, (raw.shape[0], raw.shape[1]))
            time_range = raw.timeRange

            return sigarray, time_range

def get_digital_out_states(addr):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan) 
        try:
            res = stub.GetDIOReg(common_pb2.StandardRequest())
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)
        else:
            return {
                'digital_outs_mode': DOUT_MODE_OUT[res.mode],
                'states': [{'chan_idx': i.ntvChanIdx, 'state': i.manualState } for i in res.doutChanRegisters]
        }


# ======= setters ========
def set_digital_out_manual(addr, dout1_state: bool, dout2_state: bool):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.AllegoCoreStub(chan) 

        req1 = allegoserver_pb2.DIOModeManualRequest()
        req1.chanIdx=0
        req1.state=dout1_state

        req2 = allegoserver_pb2.DIOModeManualRequest()
        req2.chanIdx=1
        req2.state=dout2_state

        try:
            stub.SetDIOManual(req1)
            stub.SetDIOManual(req2)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)

def set_time_to_cache_head(addr, stream_group_id=None):
    with new_server_channel(addr) as chan:
        stub = allegoserver_pb2_grpc.Pcache1Stub(chan)
        req = common_pb2.SignalGroupIDRequest()
        req.streamGroupId=stream_group_id
        try:
            stub.SetTimeRangeToHead(req)
        except grpc.RpcError as ex:
            handle_grpc_error(ex, CLIENT_NAME)





