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
async def TDC_5_d(dut):
    print("**************************************************************************************")
    print("TDC.5.d: The TDC measure the correct pulse length")
    print("**************************************************************************************")

    for i in range(10):
        #Generate random pulse length:
        Pulse_time = random.randint(5000,125000)*40

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
        await cocotb.triggers.ClockCycles(dut.clk, 10, rising = True)

        #Assert i_enable_channel
        dut.inst_tdc_channel_0.i_enable_channel.value = 1
        await cocotb.triggers.ClockCycles(dut.clk, 1, rising = True)

        #We Assert the i_trigger
        dut.inst_tdc_channel_0.i_trigger.value = 1
        #await RisingEdge(dut.inst_tdc_channel_0.o_busy)
        #await cocotb.triggers.ClockCycles(dut.clk, 100, rising = True)
        await cocotb.triggers.Timer(Pulse_time, 'ps')
        
        #We Deassert the i_trigger and wait for o_busy to deassert
        dut.inst_tdc_channel_0.i_trigger.value = 0
        #await cocotb.triggers.FallingEdge(dut.inst_tdc_channel_0.o_hasEvent)
        await cocotb.triggers.ClockCycles(dut.clk, 1000, rising = True)

        pulse_time = dut.inst_tdc_channel_0.o_pulseWidth.value
        print("------------------------------------------------")
        print(f"Pulse Length {i}: {Pulse_time}ps")
        print(f"Pulse Length data {i}: {pulse_time}")
        print(f"Pulse Length  measured {i}: {pulse_time*40}ps")
        

        #We validate time pulse is correct
        assert pulse_time*40 == Pulse_time
