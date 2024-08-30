import cocotb
from cocotb.clock import Clock

import os

import pydevd_pycharm


# Decorator to tell cocotb this function is a coroutine
@cocotb.test()
async def lab1(dut):
    print("Starting test_lab1")

    PYCHARMDEBUG = os.environ.get('PYCHARMDEBUG')

    print(PYCHARMDEBUG)

    if(PYCHARMDEBUG == "enabled"):
        pydevd_pycharm.settrace('localhost', port=5333, stdoutToServer=True, stderrToServer=True)

    # set a signal to some value
    dut.reset.value = 1
    dut.in_sig.value = 1

    # start a clock signal
    await cocotb.start(Clock(dut.clk, 10, units='ns').start())

    # wait for 100ns
    await cocotb.triggers.ClockCycles(dut.clk, 10, rising=True)

    # drop reset and send data
    dut.reset.value = 0
    for i in range(8):
        dut.in_sig.value = i % 2
        await cocotb.triggers.ClockCycles(dut.clk, 100, rising=True)

    # wait for 100ns
    await cocotb.triggers.ClockCycles(dut.clk, 10, rising=True)
    print("Bon matin")
