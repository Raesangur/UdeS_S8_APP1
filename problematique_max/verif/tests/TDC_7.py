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
async def TDC_7(dut):
    print("**************************************************************************************")
    print("TDC.7: Validate Unique Channel ID")
    print("**************************************************************************************")

    # Instanciation du MMC
    inst_MMC_TDC = MMC_TDC(dut.inst_tdc_channel_1, monitor_type = 1, test_type = 1)
    inst_MMC_TDC.start()

    # Initialisation of clock and input pins
    #dut.reset.value = 1
    #dut.in_sig.value = 1
    #await cocotb.start(Clock(dut.clk, 10, units='ns').start())
    #await cocotb.triggers.ClockCycles(dut.clk, 10, rising = True)

    #dut.reset.value = 0
    
    
    #id_TDC1 = dut1.inst_tdc_channel_0.o_chanID.value
    #id_TDC2 = dut.inst_tdc_channel_1.o_chanID.value
    
    #print(f"TDC 1 id: {id_TDC1}")
    #print(f"TDC 2 id: {id_TDC2}")


    # Initialisation Driver and Sink for the dut UART RX/TX channels
    #uart_driver = UartSource(dut.in_sig, baud=1000000, bits=8)
    #tdc2 = UartSource(dut.in_sig, baud=1000000, bits=8)
    #uart_sink   = UartSink(dut.out_sig, baud=1000000, bits=8)

    # Start thread for the reply function for the expected UART response.
    #Task_returnMessage = await cocotb.start(wait_reply(dut, uart_sink))

    # Generate Product Version ID Register Value:
    #request_id = build_command_message(0b00000, 0x08, 0x0)
    #request_id = cocotb.binary.BinaryValue(value=0x08, n_bits=8, bigEndian=False)
    #await uart_driver.write(request_id)
    #await uart_driver.wait()
    
    #await Task_returnMessage

    #To get the type returned from a Task, you must call task.result()
    #packetSplitter = Task_returnMessage.result()
    print(packetSplitter)
    #random_data_value = build_command_message(0, 0xBADEFACEB00B, 0)
    #for i in range(10):
    #    random_data_value = secrets.token_bytes(6)
#
 #       print(f"Random Packet #{i}: {random_data_value}")
#
        # Send arbitrary value, then wait for transaction to complete
#        await uart_driver.write(random_data_value)
 #       await uart_driver.wait()


# L.E4 function to wait for response message
async def wait_reply(dut, uart_sink):

    # Non-infinite wait loop. Throw cocotb exception if timeout is reached (to do)
    for x in range(0, 100):
        if(uart_sink.count() >= 7): ## 6 octets du message + le CRC
            break;
        await cocotb.triggers.ClockCycles(dut.clk, 1000, rising=True)

    if(x == 99):
        print("Timeout")
        logger = SimLog("cocotb.Test")
        logger.info("Timeout for wait reply")
        raise RuntimeError("Timeout for wait reply")
        # or use plain assert.
        #assert False, "Timeout for wait reply"
        return None

    else:
        # cocotbext-uart returns byteArray. Convert to bytes first, then to Binary value for uniformity.
        message_bytes = bytes(await uart_sink.read(count=6))
        message = cocotb.binary.BinaryValue(value=message_bytes, n_bits=48, bigEndian=False)
        #print("After a wait of " + str(x) + "000 clocks, received message: ", end='')
        #print("0x{0:0{width}x}".format(message.integer, width=12))
        return message


