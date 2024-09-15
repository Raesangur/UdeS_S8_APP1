# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

# adapted from https://github.com/cocotb/cocotb/blob/stable/1.9/examples/matrix_multiplier/tests/test_matrix_multiplier.py

from typing import Any, Dict, List

import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge
from cocotb.log import SimLog
from utilsVerif import get_expected_crc

class DataValidMonitor_Template:
    """
    Reusable Monitor of one-way control flow (data/valid) streaming data interface

    Args
        clk: clock signal
        valid: control signal noting a transaction occured
        datas: named handles to be sampled when transaction occurs
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
        #self.log.info("use this to print some information at info level")
        #self.log.info({name: handle.value for name, handle in self._datas.items()})


        # for loop going through all the values in the signals to sample (see constructor)
        return {name: handle.value for name, handle in self._datas.items()}

class MMC_TDC:

    def __init__(self, logicblock_instance: SimHandleBase, monitor_type: int, test_type: int ):
        self.log = SimLog("MMC_TDC Constructor")
        self.dut = logicblock_instance
        if monitor_type == 0:
            self.input_mon = DataValidMonitor_Template(
                clk=self.dut.clk,
                valid=self.dut.i_enable_channel,
                datas=dict(i_reset=self.dut.i_reset, i_trigger=self.dut.i_trigger, i_clear=self.dut.i_clear),
            )

            self.output_mon = DataValidMonitor_Template(
                clk=self.dut.clk,
                valid=self.dut.o_hasEvent,
                datas=dict(o_busy=self.dut.o_busy, o_chanID=self.dut.o_chanID, o_timestamp=self.dut.o_timestamp, o_pulseWidth=self.dut.o_pulseWidth),        
            )
        else:
            self.input_mon = DataValidMonitor_Template(
                clk=self.dut.clk,
                valid=self.dut.i_enable_channel,
                datas=dict(i_reset=self.dut.i_reset, i_trigger=self.dut.i_trigger, i_clear=self.dut.i_clear),
            )

            self.output_mon = DataValidMonitor_Template(
                clk=self.dut.clk,
                valid=self.dut.o_busy,
                datas=dict(o_hasEvent=self.dut.o_hasEvent, o_chanID=self.dut.o_chanID, o_timestamp=self.dut.o_timestamp, o_pulseWidth=self.dut.o_pulseWidth),        
            )


        self._checkercoro = None

        self.log = SimLog("cocotb.MMC.%s" % (type(self).__qualname__))

    def start(self) -> None:
        """Starts monitors, model, and checker coroutine"""
        if self._checkercoro is not None:
            raise RuntimeError("Monitor already started")
        self.input_mon.start()
        self.output_mon.start()
        self._checkercoro = cocotb.start_soon(self._checker())

    def stop(self) -> None:
        """Stops everything"""
        if self._checkercoro is None:
            raise RuntimeError("Monitor never started")
        self.input_mon.stop()
        self.output_mon.stop()
        self._checkercoro.kill()
        self._checkercoro = None

    # Model expects list of ints as inputs, returns a list of ints
    # modifiy as needed.
    def model(self, InputsA: List[int], InputsB: List[int]) -> List[int]:
        # equivalent model to HDL code
        crc_val = get_expected_crc(InputsB.buff[:-1])
        model_result1 = crc_val == InputB.buff[-1]
        model_result2 = crc_val
        return [model_result1, model_result2]


    # Insert logic to decide when to check the model against the HDL result.
    # then compare output monitor result with model result
    # This example might not work every time.
    async def _checker(self) -> None:
        test_done = False
        while not test_done:
            # dummy await, allows to run without checker implementation and verify monitors
            await cocotb.triggers.ClockCycles(self.dut.clk, 1000, rising=True)
            
            # SD1: Send a i_trigger signals while keeping i_enable_channel false. o_busy should always stays deasserted
            if test_type == 1:
                

            # SD2: Create 10 i_trigger pulse signals width corresponding to a 'one hot" - 200ns time width. The output o_pulseWidth should correspond to a "one hot" encoding. (LSB is 40ps)    
            if test_type == 2:

            # SD3: We assert i_trigger  with pulses shorter than 20ns, o_busy should stay deasserted
            if test_type == 3:

            # SD4: Send a i_trigger signal shorter than 20ns, o_busy is not asserted.
            if test_type == 4:

            # SD5: Send a i_trigger signal longer than 5us. o_pulseWidth should read 0x0001E848
            if test_type == 5:
                actual = []
                while not self.input_mon.values.empty():
                    actual.append(await self.output_mon.values.get())

                expected_inputs = await self.input_mon.values.get()
                expected = self.model(
                    InputsA=expected_inputs["i_last"], InputsB=expected_inputs["i_data"]
                )

                # compare expected with actual using assertions. Exact indexing must
                # be adapted to specific case and model return value
                assert actual["o_match"] == expected[0]
                assert actual["o_crc8"] == expected[1]


