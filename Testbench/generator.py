# Generator Object:
# 
# Generate Random or Specific Signals for the driver


from typing import Any, Dict, List

import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge
from cocotb.log import SimLog


class Generator:
    """
    Generic Generator Model

    Args
    signals: List of signal to be asserted by the driver

    Methods:
    _generate_random: Generate Radom Signals
    _generate_signals: Generate a Specific Signal
    """

    def __init__(self):

if __name__ == "__main__":
    print("Test Generator")
