import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Join, FallingEdge, RisingEdge, Timer
from cocotbext.uart import UartSource, UartSink
from utilsVerif import print_cocotb_BinaryValue, build_command_message, get_expected_crc
from cocotb.log import SimLog
from cocotb.handle import SimHandleBase
import secrets
import random
from MMC_REG import MMC_REG

async def initReset(dut):

    #Preset all top inputs, from spec sheet : reset, clk, clkMHz, in_sig, resetCyclic, sipms[1:0]
    dut.reset.value         = 1
    dut.clk.value           = 0
    dut.clkMHz.value        = 1
    dut.in_sig.value        = 1
    dut.resetCyclic.value   = 1
    dut.sipms[0].value      = 0
    dut.sipms[1].value      = 1

    # Confirm type of read signal. Expected: cocotb.binary.BinaryValue
    print(f"[DEBUG] reset.value type : {type(dut.reset.value)}")
    print(f"[DEBUG] clk.value type : {type(dut.clk.value)}")
    print(f"[DEBUG] in_sig.value type : {type(dut.in_sig.value)}")
    print(f"[DEBUG] resetCyclic.value type : {type(dut.resetCyclic.value)}")
    print(f"[DEBUG] sipms.value type : {type(dut.sipms.value)}")

    # start a clock signal
    await cocotb.start(Clock(dut.clk, 10, units='ns').start())

    # wait for 10 clock periods triggers every rising edge
    await cocotb.triggers.ClockCycles(dut.clk, 10, rising=True)

    # disable reset
    dut.reset.value = 0
    await cocotb.triggers.ClockCycles(dut.clk, 1, rising=True)

    dut.in_sig.value = 0
    await cocotb.triggers.ClockCycles(dut.clk, 1, rising=True)

    print("[DEBUG] INIT DONE!")

# Test 
@cocotb.test()
async def REG_3_a(dut):
    print("**************************************************************************************")
    print("REG.3.a: We can write badeface")
    print("**************************************************************************************")
    #inst_MMC_REG = MMC_REG(dut.registers_dut, monitor_type = 1, test_id = 1)
    #inst_MMC_REG.start()
    # Initialisation of clock and input pins
    await cocotb.start(Clock(dut.clk, 10, units='ns').start())
    await cocotb.triggers.ClockCycles(dut.clk, 1, rising = True)
    dut.registers_dut.reset.value = 1
    await cocotb.triggers.ClockCycles(dut.clk, 1, rising = True)
    dut.registers_dut.reset.value = 0


    # Ajouter l'initialisation des pattes d'entrée et de l'horloge
    await initReset(dut)

    # Driver and Sink for the dut UART RX/TX channels
    uart_driver = UartSource(dut.in_sig, baud=1000000, bits=8)
    uart_sink   = UartSink(dut.out_sig, baud=1000000, bits=8)

    # Start thread for the reply function for the expected UART response.
    Task_returnMessage = await cocotb.start(wait_reply(dut, uart_sink))
    #assert hex(int(packetSplitter)) == hex(0x800badeface)


    #######################################################
    # DataMode Adress
    ######################################################
    # Send Write command
    reg9 = build_command_message(0x01, 0x0, 0xbadeface)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()
    await Task_returnMessage
    await cocotb.triggers.ClockCycles(dut.clk, 100, rising = True)

    # Send read command
    reg9 = build_command_message(0x0, 0x0, 0x00000000)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()

    # Send CRC
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    await Task_returnMessage

    packetSplitter = Task_returnMessage.result()
    print(f"[DEBUG] Task_returnMessage type : {type(packetSplitter)}")
    print(packetSplitter)
    print(hex(int(packetSplitter)))
    assert hex(int(packetSplitter)) == hex(0x800badeface)

    #######################################################
    # Bias Mode
    ######################################################
    # Send Write command
    reg9 = build_command_message(0x1, 0x1, 0xbadeface)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()
    await Task_returnMessage

    # Send read command
    reg9 = build_command_message(0x0, 0x1, 0x00000000)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()

    # Send CRC
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    await Task_returnMessage

    packetSplitter = Task_returnMessage.result()
    print(f"[DEBUG] Task_returnMessage type : {type(packetSplitter)}")
    print(packetSplitter)
    print(hex(int(packetSplitter)))
    assert hex(int(packetSplitter)) == hex(0x800badeface)


    #######################################################
    # EnableCntRate
    ######################################################
    # Send Write command
    reg9 = build_command_message(0x1, 0x2, 0xbadeface)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    # Send read command
    reg9 = build_command_message(0x0, 0x2, 0x00000000)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()

    # Send CRC
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    await Task_returnMessage

    packetSplitter = Task_returnMessage.result()
    print(f"[DEBUG] Task_returnMessage type : {type(packetSplitter)}")
    print(packetSplitter)
    print(hex(int(packetSplitter)))
    assert hex(int(packetSplitter)) == hex(0x800badeface)



    #######################################################
    # EnableEventCntRate
    ######################################################
    # Send Write command
    reg9 = build_command_message(0x1, 0x3, 0xbadeface)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    # Send read command
    reg9 = build_command_message(0x0, 0x3, 0x00000000)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()

    # Send CRC
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    await Task_returnMessage

    packetSplitter = Task_returnMessage.result()
    print(f"[DEBUG] Task_returnMessage type : {type(packetSplitter)}")
    print(packetSplitter)
    print(hex(int(packetSplitter)))
    assert hex(int(packetSplitter)) == hex(0x800badeface)


    #######################################################
    # TdcTreshold
    ######################################################
    # Send Write command
    reg9 = build_command_message(0x1, 0x4, 0xbadeface)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    # Send read command
    reg9 = build_command_message(0x0, 0x4, 0x00000000)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()

    # Send CRC
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    await Task_returnMessage

    packetSplitter = Task_returnMessage.result()
    print(f"[DEBUG] Task_returnMessage type : {type(packetSplitter)}")
    print(packetSplitter)
    print(hex(int(packetSplitter)))
    assert hex(int(packetSplitter)) == hex(0x800badeface)


    #######################################################
    # SrcSelected
    ######################################################
    # Send Write command
    reg9 = build_command_message(0x1, 0x5, 0xbadeface)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    # Send read command
    reg9 = build_command_message(0x0, 0x5, 0x00000000)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()

    # Send CRC
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    await Task_returnMessage

    packetSplitter = Task_returnMessage.result()
    print(f"[DEBUG] Task_returnMessage type : {type(packetSplitter)}")
    print(packetSplitter)
    print(hex(int(packetSplitter)))
    assert hex(int(packetSplitter)) == hex(0x800badeface)


    ######################################################
    # ClearSyncFlag
    ######################################################
    # Send Write command
    reg9 = build_command_message(0x1, 0x7, 0xbadeface)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    # Send read command
    reg9 = build_command_message(0x0, 0x7, 0x00000000)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()

    # Send CRC
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    await Task_returnMessage

    packetSplitter = Task_returnMessage.result()
    print(f"[DEBUG] Task_returnMessage type : {type(packetSplitter)}")
    print(packetSplitter)
    print(hex(int(packetSplitter)))
    assert hex(int(packetSplitter)) == hex(0x800badeface)



    #######################################################
    # ChannelEnableBits
    ######################################################
    # Send Write command
    reg9 = build_command_message(0x1, 0x8, 0xbadeface)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    # Send read command
    reg9 = build_command_message(0x0, 0x8, 0x00000000)
    print(f"[DEBUG] {hex(reg9)}")
    await uart_driver.write(reg9.buff)
    await uart_driver.wait()

    # Send CRC
    crc8 = get_expected_crc(reg9.buff)
    crc8bin = cocotb.binary.BinaryValue(value=crc8, n_bits=8, bigEndian=False)
    await uart_driver.write(crc8bin.buff)
    await uart_driver.wait()

    await Task_returnMessage

    packetSplitter = Task_returnMessage.result()
    print(f"[DEBUG] Task_returnMessage type : {type(packetSplitter)}")
    print(packetSplitter)
    print(hex(int(packetSplitter)))
    assert hex(int(packetSplitter)) == hex(0x800badeface)




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
        assert False, "Timeout for wait reply"
        #return None

    else:
        # cocotbext-uart returns byteArray. Convert to bytes first, then to Binary value for uniformity.
        message_bytes = bytes(await uart_sink.read(count=6))
        message = cocotb.binary.BinaryValue(value=message_bytes, n_bits=48, bigEndian=False)
        print("After a wait of " + str(x) + "000 clocks, received message: ", end='')
        print("0x{0:0{width}x}".format(message.integer, width=12))
        print(f"[DEBUG] message type : {type(message)}")
        return message
