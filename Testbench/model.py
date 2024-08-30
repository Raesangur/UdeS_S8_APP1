# Model Object:
# 
#
# Input_Monitor -> [Model] -> Checker -> Output_Monitor


from typing import Any, Dict, List

import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge
from cocotb.log import SimLog


class Model:
    """
    Generic Component Model

    Args
        
    """

    def __init__(self, logicblock_instance: SimHandleBase):

    # Model expects list of ints as inputs, returns a list of ints
    # modifiy as needed.
    def model(self, InputsA: List[int], InputsB: List[int]) -> List[int]:
        # equivalent model to HDL code
        model_result1 = 0
        model_result2 = 1
        return [model_result1, model_result2]


if __name__ == "__main__":
    print("Test Model")
