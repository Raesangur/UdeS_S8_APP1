import cocotb
from cocotb.clock import Clock

import os

import pydevd_pycharm


# Decorator to tell cocotb this function is a coroutine
@cocotb.test()
async def lab1_E1(dut):
    print("Test Max")

    PYCHARMDEBUG = os.environ.get('PYCHARMDEBUG')

    print(PYCHARMDEBUG)

    if(PYCHARMDEBUG == "enabled"):
        pydevd_pycharm.settrace('localhost', port=6420, stdoutToServer=True, stderrToServer=True)

    # set a signal to some value
    dut.reset.value = 1

    # fetch value from a signal in the dut
    fetch_value = dut.reset.value

    # Confirm type of read signal. Expected: cocotb.binary.BinaryValue
    print(type(fetch_value))

    # start a clock signal
    await cocotb.start(Clock(dut.clk, 10, units='ns').start())

    # wait for 1000 clock periods
    await cocotb.triggers.ClockCycles(dut.clk, 10, rising=True)

    dut.reset.integer = 1
    await cocotb.triggers.ClockCycles(dut.clk, 10, rising=True)
    dut.reset.integer = 0
    

    trame = [1,0,0,0,1,1,1,0]

    for i in trame:
        dut.in_sig.value = i
        await cocotb.triggers.ClockCycles(dut.clk, 100, rising=True)

    print("Bon mat1in")
