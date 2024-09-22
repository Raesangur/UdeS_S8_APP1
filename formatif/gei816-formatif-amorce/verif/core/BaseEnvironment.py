import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotbext.uart import UartSource, UartSink
from cocotb.log import SimLog

import os
import pydevd_pycharm



class BaseEnvironment:
    def __init__(self, dut):
        # keep pointer to dut in class
        self.dut = dut
        self.log = SimLog("cocotb.base.%s" % (type(self).__qualname__))

    # Common sequence for all tests
    async def run(self):
        PYCHARMDEBUG = os.environ.get('PYCHARMDEBUG')
        print(PYCHARMDEBUG)
        if (PYCHARMDEBUG == "enabled"):
            pydevd_pycharm.settrace('localhost', port=9090, stdoutToServer=True, stderrToServer=True)

        self.BuildEnvironment()
        await self.InitSignalsClockAndReset()
        self.StartEnvironment()
        await self.test()
        await self.postTest()

    def BuildEnvironment(self):
        self.uart_driver = UartSource(self.dut.rx_uart_serial_in, baud=1000000, bits=8)
        self.uart_sink   = UartSink(self.dut.tx_uart_serial_out, baud=1000000, bits=8)

    def StartEnvironment(self):
        pass

    async def InitSignalsClockAndReset(self):
        self.dut.rx_uart_serial_in.value = 1
        self.dut.reset.value = 1

        self.c = Clock(self.dut.clk, 100, 'ns')
        await cocotb.start(self.c.start())

        ## delay for reset
        await cocotb.triggers.ClockCycles(self.dut.clk, 10, rising=True)

        ## release reset
        self.dut.reset.value = 0
        await cocotb.triggers.ClockCycles(self.dut.clk, 2, rising=True)


    # Virtual function, forces to use derived class.
    async def test(self):
        # Mimmick C++ Pure virtual function.
        raise NotImplementedError()

    # Put anything happening at the end of the simulation here.
    async def postTest(self):
        await cocotb.triggers.ClockCycles(self.dut.clk, 10, rising=True)
        self.dut.reset.value = 1
        await cocotb.triggers.ClockCycles(self.dut.clk, 2, rising=True)

    # Wrapper around driver, to send values to the dut.
    async def SendValue(self, ValueToDut):
        await self.uart_driver.write(ValueToDut.to_bytes(1, "little"))
        await self.uart_driver.wait()

    # Read back the value and convert to integer.
    async def ReadResult(self):
        # result_BytesArray = await self.???.read(count=1)
        result_BytesArray = await self.uart_sink.read(count=1)
        result_bytes = bytes(result_BytesArray)
        result_int = int.from_bytes(result_bytes, "little")
        return result_int




