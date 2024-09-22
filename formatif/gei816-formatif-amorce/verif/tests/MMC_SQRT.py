# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

# adapted from https://github.com/cocotb/cocotb/blob/stable/1.9/examples/matrix_multiplier/tests/test_matrix_multiplier.py

from typing import Any, Dict, List
from math import sqrt, floor

import cocotb
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.triggers import RisingEdge
from cocotb.log import SimLog

from templates.MMC_Template import *


class MMC_SQRT(MMC_Template):
    def __init__(self, logicblock_instance: SimHandleBase):
        self.dut = logicblock_instance
        self.log = SimLog("cocotb.MMC.%s" % (type(self).__qualname__))

        self.input_mon = DataValidMonitor_Template(
            clk=self.dut.clk,
            valid=self.dut.arg_valid,
            datas=dict(SignalA=self.dut.arg_valid,
                       SignalB=self.dut.arg),
        )

        self.output_mon = DataValidMonitor_Template(
            clk=self.dut.clk,
            valid=self.dut.sqrt_valid,
            datas=dict(SignalC=self.dut.sqrt_valid,
                       SignalD=self.dut.sqrt_res)
        )

        self._checkercoro = None

    # Model, modify as needed.
    def model(self, echantillons):
        return floor(sqrt(echantillons["SignalB"]))

    async def _checker(self) -> None:
        InSamplesList = []
        OutSamplesList = []
        ExpectedSamplesList = []
        while True:
            # dummy await, allows to run without checker implementation and verify monitors
            await cocotb.triggers.ClockCycles(self.dut.clk, 1, rising=True)

            while(not self.input_mon.values.empty()):
                InSamplesList.append(self.input_mon.values.get_nowait())
                print(InSamplesList)

            while(not self.output_mon.values.empty()):
                OutSamplesList.append(self.output_mon.values.get_nowait())
                print(OutSamplesList)

            if len(InSamplesList) == len(OutSamplesList) and len(InSamplesList) != 0:
                for sample in InSamplesList:
                    ExpectedSamplesList.append(self.model(sample))

                assert(len(ExpectedSamplesList) == len(OutSamplesList))

                for i in range(len(OutSamplesList)):
                    assert OutSamplesList[i]["SignalD"] == ExpectedSamplesList[i]

                InSamplesList = []
                OutSamplesList = []
                ExpectedSamplesList = []

            """
            Extraire toutes les valeurs d'un signal d'une telle liste:
            SignalSamples = [d['NomSignal'] for d in SamplesList]
            --> depuis https://stackoverflow.com/questions/7271482/getting-a-list-of-values-from-a-list-of-dicts
            
            Même chose, mais en changeant aussi les valeur d'un bus pour des entiers
            ValueList = [d['NomSignal'].integer for d in expected_inputs]
            
            Lire une valeur dès que disponible, attendre sinon
            actual = await self.mon.values.get()

            # compare expected with actual using assertions. 
            assert actual["SignalC"] == expected
            """

