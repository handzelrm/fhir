import generatebase
import generatepatient
import generatepractitioner
import generateencounter
import generateobservationdict

import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.observation as o

import datetime

class GenerateObservation(generatebase.GenerateBase):

    
    def __init__(self,observation_dict,dt=datetime.datetime.now(),Patient=None, Practitioner=None, Encounter=None):
        """Uses fhirclient.models to create and send vitals to server."""
        self.dt = dt

        if Patient == None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient

        if Practitioner == None:
            self.Practitioner = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner_recipient = Practitioner

        if Encounter == None:
            self.Encounter = generateencounter.GenerateEncounter(Patient=self.Patient, Location=None, Condition=None).Encounter
        else:
            self.Encounter = Encounter

        self.observation_dict = observation_dict

        if not isinstance(self.observation_dict,dict):
            raise ValueError('observation_dict needs to be a dictionary of observations')
        
        for obs,value in self.observation_dict.items():
            Observation = o.Observation()
            CodeableConcept = cc.CodeableConcept()
            Coding = c.Coding()
            Coding.system = 'http://loinc.org'
            Coding.code = value['loinc']
            Coding.display = value['display']

            CodeableConcept.coding = [Coding]
            Observation.code = CodeableConcept
            Observation.status = 'final'
            Observation.subject = self._create_FHIRReference(self.Patient)
            Observation.performer = [self._create_FHIRReference(self.Practitioner)]

        
            if value['type'] == 'quantity':
                Observation = self._add_quantity_value(Observation,obs)
            elif value['type'] == 'codeable':
                Observation = self._add_codeable_value(Observation,obs)
            else:
                raise ValueError('Measurement Type ValueError')

            Observation.effectiveDateTime = self._create_FHIRDate(self.dt)
                 
            Observation.context = self._create_FHIRReference(self.Encounter) 
               
            self.response = Observation.create(server=self.connect2server().server)
            Observation.id = self._extract_id()

if __name__ == '__main__':
    obs = generateobservationdict.GenerateObservationDict()
    GenerateObservation(obs.observation_dict,Patient=obs.Patient)