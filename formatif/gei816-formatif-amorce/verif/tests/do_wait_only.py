import cocotb

import os

from BaseEnvironment import BaseEnvironment
class CDoWaitOnly(BaseEnvironment):
    async def test(self):
        # wait for 1000 clock periods
        await cocotb.triggers.ClockCycles(self.dut.clk, 1000, rising=True)

@cocotb.test()
async def do_wait_only(dut):
    runObject = CDoWaitOnly(dut)
    runObject.log.info("Starting DoWaitOnly")
    await runObject.run()


