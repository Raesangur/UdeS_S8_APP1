#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta
import cocotb
import monitor
import checker
import model

class Testbench(metaclass=ABCMeta):
    self.generator  = None
    self.monitorIn  = Monitor()
    self.monitorOut = Monitor()
    self.checker    = Checker()
    self.model      = Model()
    self.driver     = None


    def __init__(self):
        print("Starting test: " + self.__class__.__name__)
        self._trace_debug()
        

    def reset_and_init(self):
        self.driver.reset()
        self.driver.init(self.generator)

    @abc.abstractmethod
    def run(self):
        pass

    
    def _trace_debug():
        PYCHARMDEBUG = os.environ.get('PYCHARMDEBUG')
        print(PYCHARMDEBUG)

        if(PYCHARMDEBUG == "enabled"):
            pydevd_pycharm.settrace('localhost', port=5333, stdoutToServer=True, stderrToServer=True)



if __name__ == "__main__":
    print("Test TestBench")
