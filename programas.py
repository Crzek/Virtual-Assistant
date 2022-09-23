#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class App:

    """clase app, donde se guardaran las programs con sus nombre y sus rutas donde se encuentra"""

    def __init__(self, name, path ):
        self.Name = name            #str
        self.Path = path            #str

    def __str__(self):
        return f"App: {self.Name}---{self.Path}"

    def __repr__(self):
        return __str__()

    def get_name(self):
        return self.Name

    def get_path(self):
        return self.Path


    def set_name(self,value):
        self.Name = value

    def set_path(self,value):
        self.Path = value
