from random import randint

from BaseEnvironment import *
from MMC_SQRT import *


class Q1B(BaseEnvironment):
    async def test(self):
        rand = [randint(0, 255) for x in range(randint(1, 10))]
        print(rand)

        for r in rand:
            await self.SendValue(r)
            print(await self.ReadResult())

@cocotb.test()
async def q1b(dut):
    mmc = MMC_SQRT(dut.inst_topvhdl.inst_square_root)
    mmc.start()

    runObject = Q1B(dut)
    await runObject.run()


