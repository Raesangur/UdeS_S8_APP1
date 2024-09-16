import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Join, FallingEdge, RisingEdge, Timer
from cocotbext.uart import UartSource, UartSink
from utilsVerif import print_cocotb_BinaryValue, build_command_message, get_expected_crc
from cocotb.log import SimLog
from cocotb.handle import SimHandleBase
import secrets
import random

# Test 
@cocotb.test()
async def TDC_5_e(dut):
    print("**************************************************************************************")
    print("TDC.5.e: The TDC shows the correct rising edge Time Stamp")
    print("**************************************************************************************")
    Wait_time = 0
    for i in range(1):
        #Generate random pulse length:
        Wait_time = Wait_time + random.randint(1000,10000)*40

        # Initialisation of clock and input pins
        await cocotb.start(Clock(dut.clk, 10, units='ns').start())
        dut.inst_tdc_channel_0.o_pulseWidth.value = 0
        dut.inst_tdc_channel_0.o_timestamp.value = 0
        dut.inst_tdc_channel_0.i_trigger.value = 0
        dut.inst_tdc_channel_0.i_enable_channel.value = 0

        #System Reset
        dut.reset.value = 1
        dut.inst_tdc_channel_0.reset.value = 1
        await cocotb.triggers.ClockCycles(dut.clk, 1, rising = True)
        dut.reset.value = 0
        dut.inst_tdc_channel_0.reset.value = 0
        
        #TDC Clear
        dut.inst_tdc_channel_0.i_clear.value = 1
        await cocotb.triggers.ClockCycles(dut.clk, 1, rising = True)
        dut.inst_tdc_channel_0.i_clear.value = 0
        await cocotb.triggers.ClockCycles(dut.clk, 1, rising = True)

        #Assert i_enable_channel
        dut.inst_tdc_channel_0.i_enable_channel.value = 1
        await cocotb.triggers.ClockCycles(dut.clk, 1, rising = True)

        #We Assert the i_trigger
        await cocotb.triggers.Timer(Wait_time, 'ps')
        dut.inst_tdc_channel_0.i_trigger.value = 1
        await cocotb.triggers.Timer(300, 'ns')
        
        #We Deassert the i_trigger and wait for o_busy to deassert
        dut.inst_tdc_channel_0.i_trigger.value = 0
        await cocotb.triggers.ClockCycles(dut.clk, 1000, rising = True)

        Wait_time = Wait_time + 30000
        time_stamp = dut.inst_tdc_channel_0.o_timestamp.value
        print("------------------------------------------------")
        print(f"Waiting Time {i}: {Wait_time}ps")
        print(f"Time Stamp data {i}: {time_stamp}")
        print(f"Time Stamp  measured {i}: {time_stamp*40}ps")
        print(f"Time Stamp  difference {i}: {(time_stamp*40-Wait_time)/1000}ns")

        #We validate time pulse is correct
        assert time_stamp.value*40 == Wait_time
