import generatebase
import generatepatient
import generatelocation
import generatecondition
import generatepractitioner

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

import datetime
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class GenerateEncounter(generatebase.GenerateBase):


    def __init__(self, Patient=None, Provider=None, Location=None, Condition=None, Period=None, status='in-progress', fhir_class='outpatient'):
        """Uses fhirclient.models to create encounter resource"""

        if Patient is not None and Condition is not None:
            if Patient.id != Condition.Patient.id:
                raise ValueError('Patient.id must equal Conditition.Patient.id.')
            self.Patient = Patient
            self.Condition = Condition
        elif Condition is None and Patient is None:
            self.Condition = generatecondition.GenerateCondition().Condition
            self.Patient = self.Condition.Patient
        elif Condition is not None and Patient is None:
            self.Condition = Condition
            self.Patient = self.Condition.Patient
        elif Condition is None and Patient is not None:
            self.Patient = Patient
            self.Condition = generatecondition.GenerateCondition(Patient=self.Patient).Condition
        else:
            raise ValueError('Error with Patient and Condition values')

        if Location == None:
            self.Location = generatelocation.GenerateLocation().Location
        else:
            self.Location = Location

        if Period == None:
            self.Period = self._create_FHIRPeriod()
        else:
            self.Period = Period

        if Provider == None:
            self.Practitioner = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner = Provider

        self.status = status
        self.fhir_class = fhir_class

        Encounter = enc.Encounter()
        Coding = c.Coding()
        Coding.code = self.fhir_class
        Encounter.class_fhir = Coding

        Encounter.status = self.status

        EncounterLocation = enc.EncounterLocation()
        EncounterLocation.location = self._create_FHIRReference(self.Location)
        Encounter.location = [EncounterLocation]

        Encounter.subject = self._create_FHIRReference(self.Patient)

        EncounterDiagnosis = enc.EncounterDiagnosis()
        EncounterDiagnosis.condition = self._create_FHIRReference(self.Condition)
        Encounter.diagnosis = [EncounterDiagnosis]

        EncounterParticipant = enc.EncounterParticipant()
        EncounterParticipant.individual = self._create_FHIRReference(self.Practitioner)
        Encounter.participant = [EncounterParticipant]

        Encounter.period = self.Period

        # self._validate(Encounter)
        self.response = Encounter.create(server=self.connect2server().server)
        Encounter.id = self._extract_id()

        self.Encounter = Encounter
        self.Encounter.Patient = self.Patient
        self.Encounter.Condition = self.Condition
        self.Encounter.Location = self.Location
        self.Encounter.Period = self.Period
        self.Encounter.Practitioner = self.Practitioner

if __name__ == '__main__':
    GenerateEncounter()
