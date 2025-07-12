import sys

class ProgramState:
    variable_storage = {}
    label_registry = {}

    @classmethod
    def terminate_execution(cls):
        sys.exit(0) 