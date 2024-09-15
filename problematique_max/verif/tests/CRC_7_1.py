import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Join
from cocotbext.uart import UartSource, UartSink
from utilsVerif import print_cocotb_BinaryValue, build_command_message, get_expected_crc
from cocotb.log import SimLog
from MMC_CRC import MMC_CRC8
import secrets

# Test CRC.7.1: Lorsque i_valid est à ’1’, le crc change au prochain coup d’horloge pour la valeur calculé par le polynôme XX (voir code Python).
@cocotb.test()
async def CRC_7_1(dut):
    print("**************************************************************************************")
    print("CRC.7.1: Validate CRC8 o_crc with model")
    print("**************************************************************************************")


    # Instanciation du MMC
    inst_MMC_CRC8 = MMC_CRC8(dut.inst_packet_merger.inst_crc_calc, monitor_type = 0, test_type = 2)
    inst_MMC_CRC8.start()

    # Initialisation of clock and input pins
    dut.reset.value = 1
    dut.in_sig.value = 1
    await cocotb.start(Clock(dut.clk, 10, units='ns').start())
    await cocotb.triggers.ClockCycles(dut.clk, 10, rising = True)

    #dut.reset.value = 0

    # Initialisation Driver and Sink for the dut UART RX/TX channels
    uart_driver = UartSource(dut.in_sig, baud=1000000, bits=8)
    uart_sink   = UartSink(dut.out_sig, baud=1000000, bits=8)

    # Start thread for the reply function for the expected UART response.
    Task_returnMessage = await cocotb.start(wait_reply(dut, uart_sink))

    # Generate Product Version ID Register Value:
    #SomeValue = cocotb.binary.BinaryValue(value=0x1023456789ABDCEF, n_bits=64, bigEndian=False)
    #random_data_value = build_command_message(0, 0xBADEFACEB00B, 0)
    for i in range(10):
        random_data_value = secrets.token_bytes(6)

        print(f"Random Packet #{i}: {random_data_value}")

        # Send arbitrary value, then wait for transaction to complete
        await uart_driver.write(random_data_value)
        await uart_driver.wait()


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


