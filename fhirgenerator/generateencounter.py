import generatebase
import generatepatient
import generatelocation
import generatecondition

import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.encounter as enc
import fhirclient.models.fhirdate as fd
import fhirclient.models.fhirreference as fr
import fhirclient.models.humanname as hn
import fhirclient.models.location as l
import fhirclient.models.patient as p
import fhirclient.models.period as period
import fhirclient.models.practitioner as pr

class GenerateEncounter(generatebase.GenerateBase):

    def __init__(self, Patient=None, Location=None, Condition=None):
        """Uses fhirclient.models to create encounter resource"""
        if Patient == None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient

        if Location == None:
            self.Location = generatelocation.GenerateLocation().Location
        else:
            self.Location = Location

        if Condition == None:
            self.Condition = generatecondition.GenerateCondition(Patient=self.Patient).Condition
        else:
            self.Condition = Condition

        Encounter = enc.Encounter()
        Coding = c.Coding()
        Coding.code = 'outpatient'
        Encounter.class_fhir = Coding

        Encounter.status = 'finished'
        
        EncounterLocation = enc.EncounterLocation()
        EncounterLocation.location = self._create_FHIRReference(self.Location)        
        Encounter.location = [EncounterLocation]
      
        Encounter.subject = self._create_FHIRReference(self.Patient)
        
        EncounterDiagnosis = enc.EncounterDiagnosis()
        EncounterDiagnosis.condition = self._create_FHIRReference(self.Condition)        
        Encounter.diagnosis = [EncounterDiagnosis]

        # self._validate(Encounter)
        self.response = Encounter.create(server=self.connect2server().server)
        Encounter.id = self._extract_id()
        self.Encounter = Encounter

if __name__ == '__main__':
    GenerateEncounter()