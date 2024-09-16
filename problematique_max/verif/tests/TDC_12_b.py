import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Join, FallingEdge, RisingEdge, Timer
from cocotbext.uart import UartSource, UartSink
from utilsVerif import print_cocotb_BinaryValue, build_command_message, get_expected_crc
from cocotb.log import SimLog
from cocotb.handle import SimHandleBase
import secrets
import random
from MMC_TDC import MMC_TDC

# Test 
@cocotb.test()
async def TDC_12_b(dut):
    print("**************************************************************************************")
    print("TDC.12.b: The i_trigger time pulse is capped at 5us")
    print("**************************************************************************************")
    inst_MMC_TDC = MMC_TDC(dut.inst_tdc_channel_0,monitor_type = 1, test_id = 5)
    inst_MMC_TDC.start()
    for i in range(1):
        #Generate random pulse length:
        Pulse_time = random.randint(125000,200000)*40 #40ps cycles

        # Initialisation of clock and input pins
        await cocotb.start(Clock(dut.clk, 10, units='ns').start())
        dut.inst_tdc_channel_0.o_hasEvent.value = 0
        dut.inst_tdc_channel_0.o_pulseWidth.value = 0
        dut.inst_tdc_channel_0.o_timestamp.value = 0
        dut.inst_tdc_channel_0.i_trigger.value = 0
        dut.inst_tdc_channel_0.i_enable_channel.value = 0
        await cocotb.triggers.ClockCycles(dut.clk, 1, rising = True)

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
        
        #await cocotb.triggers.ClockCycles(dut.clk, 100, rising = True)

        pulse_time = dut.inst_tdc_channel_0.o_pulseWidth.value
        print("------------------------------------------------")
        print(f"Pulse Length excitation {i}: {Pulse_time/1000}ns")

        await cocotb.triggers.ClockCycles(dut.clk, 10000, rising = True)
