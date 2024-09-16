import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Join
from cocotbext.uart import UartSource, UartSink
from utilsVerif import print_cocotb_BinaryValue, build_command_message, get_expected_crc
from cocotb.log import SimLog
from cocotb.handle import SimHandleBase
from MMC_TDC import MMC_TDC
import secrets

# Test 
@cocotb.test()
async def TDC_2_a(dut):
    print("**************************************************************************************")
    print("TDC.2.a: We don't trigger an interpolation when i_enable_channel is deasserted")
    print("**************************************************************************************")

    # Instanciation du MMC
    inst_MMC_TDC = MMC_TDC(dut.inst_tdc_channel_0, test_id = 1)
    inst_MMC_TDC.start()

    # Initialisation of clock and input pins
    dut.reset.value = 1
    await cocotb.start(Clock(dut.clk, 10, units='ns').start())
    await cocotb.triggers.ClockCycles(dut.clk, 10, rising = True)
    dut.reset.value = 0
    
    #We Deassert i_enable_channel
    dut.inst_tdc_channel_0.i_enable_channel.value = 0

    #We Assert the i_trigger
    dut.inst_tdc_channel_0.i_trigger.value = 1
    await cocotb.triggers.ClockCycles(dut.clk, 1000, rising = True)
    
    #We validate o_busy is deasserted
    #assert dut.inst_tdc_channel_0.o_busy.value == 0
