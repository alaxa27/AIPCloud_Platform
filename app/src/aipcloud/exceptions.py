# AIPCloud
#
# Author : Maxime Jumelle
# Date : 04/07/2017

class UnfittedException(Exception):

    def __init___(self):
        Exception.__init__(self, "The model is unfitted.")

class UnloadedException(Exception):

    def __init___(self):
        Exception.__init__(self, "The model is not loaded.")
