# Monitor Object:
# 
#
# [Input_Monitor] -> Model -> Checker -> [Output_Monitor]


from typing import Any, Dict, List

import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge
from cocotb.log import SimLog


class Monitor:
    """
    Generic Monitor

    Args:
        clk
        valid
        datas

    Attributes:
        values: Signal stream Queue
        clk: clock signal
        valid: control signal noting a transaction occured
        _coro: Says if Monitor is running
        datas: named handles to be sampled when transaction occurs

    Methods:
        __init__: Class constructor
        start: Call _run if monitor is not already running
        stop: Stop Monitor if Running
        
        _run: Read Signals from dut and append them in self.values  
        _sample: Return Needed Signals from 
    """

    def __init__(
        self, clk: SimHandleBase, valid: SimHandleBase, datas: Dict[str, SimHandleBase]
    ):
        self.values = Queue[Dict[str, int]]()
        self._clk = clk
        self._datas = datas
        self._valid = valid
        self._coro = None # is monitor running? False if "None"

        self.log = SimLog("cocotb.Monitor.%s" % (type(self).__qualname__))

    def start(self) -> None:
        """Start monitor"""
        if self._coro is not None:
            raise RuntimeError("Monitor already started")
        self._coro = cocotb.start_soon(self._run())

    def stop(self) -> None:
        """Stop monitor"""
        if self._coro is None:
            raise RuntimeError("Monitor never started")
        self._coro.kill()
        self._coro = None


    async def _run(self) -> None:
        while True:
            await RisingEdge(self._clk)
            # this condition decides when to record the signal states
            if self._valid.value.binstr != "1":
                # wait until valid is asserted, instead of checking every clock cycle.
                await RisingEdge(self._valid)
                # skip whatever comes after, and start the while loop again
                continue
            # store the samples, as formatted by the _sample method
            self.values.put_nowait(self._sample())

    def _sample(self) -> Dict[str, Any]:
        """
        Samples the data signals and builds a transaction object

        Return value is what is stored in queue. Meant to be overriden by the user.
        """
        # possible messages to test monitor
        self.log.info("use this to print some information at info level")
        #self.log.info({name: handle.value for name, handle in self._datas.items()})


        # for loop going through all the values in the signals to sample (see constructor)
        return {name: handle.value for name, handle in self._datas.items()}

if __name__ == "__main__":
    print("Test Monitor")
