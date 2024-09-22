from random import randint

from BaseEnvironment import *
from MMC_SQRT import *

class Q1A(BaseEnvironment):
    async def test(self):
        await self.SendValue(0xAA)
        val1 = await self.ReadResult()
        await self.SendValue(0x55)
        val2 = await self.ReadResult()
        await self.SendValue(0xFF)
        val3 = await self.ReadResult()

        print(val1)
        print(val2)
        print(val3)

@cocotb.test()
async def q1a(dut):
    mmc = MMC_SQRT(dut.inst_topvhdl.inst_square_root)
    mmc.start()

    runObject = Q1A(dut)
    await runObject.run()


