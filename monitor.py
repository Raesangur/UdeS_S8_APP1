#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta
import cocotb


class Monitor(metaclass=ABCMeta):
    self.inputs = []

    def __init__(self, inputs):

    @abc.abstractmethod
    def read(self):
        pass
