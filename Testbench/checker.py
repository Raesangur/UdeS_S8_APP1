# Checker Object:
# 
#
# Input_Monitor -> Model -> [Checker] -> Output_Monitor


from typing import Any, Dict, List

import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge
from cocotb.log import SimLog

class Checker:
    """
    Reusable checker of a checker instance

    Args
        logicblock_instance: handle to an instance of a logic block

    Attributes:
        input_model: Component Model
        output_monitor: Component Output Monitor    
        checkercoro: State of the Checker (eg. running/not_running)
    """

    def __init__(self, logicblock_instance: SimHandleBase):
        self.dut = logicblock_instance

        self.input_model= Model()

        self.output_monitor = Monitor(
            clk=self.dut.clk_i,
            valid=self.dut.done,
            datas=dict(SignalC=self.dut.o_SignalC, SignalD=self.dut.o_SignalD)
        )

        self._checkercoro = None

        self.log = SimLog("cocotb.MMC.%s" % (type(self).__qualname__))

    def start(self) -> None:
        """Starts Checker coroutine"""
        if self._checkercoro is not None:
            raise RuntimeError("Checker already started")
        self._checkercoro = cocotb.start_soon(self._check())

    def stop(self) -> None:
        """Stops Checker"""
        if self._checkercoro is None:
            raise RuntimeError("Checker never started")
        self._checkercoro.kill()
        self._checkercoro = None


    # Insert logic to decide when to check the model against the HDL result.
    # then compare output monitor result with model result
    # This example might not work every time.
    async def _checker(self) -> None:
        while True:
            # dummy await, allows to run without checker implementation and verify monitors
            await cocotb.triggers.ClockCycles(self.dut.clk, 1000, rising=True)
            """
            actual = await self.output_mon.values.get()
            expected_inputs = await self.input_mon.values.get()
            expected = self.model(
                InputsA=expected_inputs["SignalA"], InputsB=expected_inputs["SignalB"]
            )

            # compare expected with actual using assertions. Exact indexing must
            # be adapted to specific case and model return value
            assert actual["SignalC"] == expected[0]
            assert actual["SignalD"] == expected[1]
            """


if __name__ == "__main__":
    print("Test Checker")
