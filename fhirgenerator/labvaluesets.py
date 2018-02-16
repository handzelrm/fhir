import generatebase
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class LabValueSets(generatebase.GenerateBase):
    def __init__(self,ResourceType,StructureDefinition):
        """Creates object with resource type and list of LOINC codes"""
        self.ResourceType = ResourceType
        self.LoincSet = []
        self.loinc = None
        self.jdata = self.json_request(self.ResourceType,StructureDefinition)
        self.dict_search()
        self.valueset = self.hard_valueset()

    def __str__(self):
        return f'ResourceType:{self.ResourceType}, LOINC ValueSet:{self.LoincSet}'

    @staticmethod
    def __repr__():
        return 'LabValueSet(ResourceType,StructureDefinition)'
