import generatebase
import generatepatient
import generatepractitioner
import generateencounter
import generateobservationdict
import generatefparlabs

import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.observation as o
import fhirclient.models.patient as p

import json
import datetime
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class GenerateObservation(generatebase.GenerateBase):

    def __init__(self,observation_dict,dt=datetime.datetime.now(),Patient=None, Practitioner=None, Encounter=None):
        """
        Creates, validates, and posts an Observation FHIR _generate_patient_fhir_object.

        :param observation_dict: dictionary of observations
        :param dt: datetime of observation. Default is now.
        :param Patient: Patient FHIR object.
        :param Practitioner: Practioner FHIR object.
        :returns: GenerateObservation object that has Observation as an attribute.
        """
        self.dt = dt

        if Patient is not None and Encounter is not None and Practitioner is not None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            if Encounter.Practitioner.id != Practitioner.id:
                raise ValueError('Encounter.Practitioner.id must equal Practitioner.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.Practitioner = Practitioner
        elif Patient is not None and Encounter is not None and Practitioner is None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must be the same as Encounter.Patient.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.Practitioner = Encounter.Practitioner
        elif Patient is not None and Encounter is None and Practitioner is not None:
            self.Patient = Patient
            self.Practitioner = Practitioner
            self.Encounter = generateencounter.GenerateEncounter(Patient=self.Patient,Practitioner=self.Practitioner).Encounter
        elif Patient is not None and Encounter is None and Practitioner is None:
            self.Patient = Patient
            self.Encounter = generateencounter.GenerateEncounter(Patient=self.Patient).Encounter
            self.Practitioner = self.Encounter.Practitioner
        elif Patient is None and Encounter is not None and Practitioner is None:
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner = self.Encounter.Practitioner
        elif Patient is None and Encounter is None and Practitioner is not None:
            self.Practitioner = Practitioner
            self.Encounter = generateencounter.GenerateEncounter(Practitioner=self.Practitioner).Encounter
            self.Patient = self.Encounter.Patient
        elif Patient is None and Encounter is not None and Practitioner is not None:
            if Encounter.Practitioner.id != Practitioner.id:
                raise ValueError('Encounter.Practitioner.id must equal Practitioner.id')
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner = Practitioner
        elif Patient is None and Encounter is None and Practitioner is None:
            self.Encounter = generateencounter.GenerateEncounter().Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner = self.Encounter.Practitioner
        else:
            raise ValueError('Error with Patient, Encounter, and Practitioner values.')

        self.observation_dict = observation_dict

        if not isinstance(self.observation_dict,dict):
            raise ValueError('observation_dict needs to be a dictionary of observations')

        for obs,value in self.observation_dict.items():
            self.obs = obs
            Observation = o.Observation()

            Observation.status = 'final'
            Observation.subject = self._create_FHIRReference(self.Patient)
            Observation.performer = [self._create_FHIRReference(self.Practitioner)]

            Observation = self._add_value(Observation,value)
            Observation.effectiveDateTime = self._create_FHIRDate(self.dt)
            Observation.context = self._create_FHIRReference(self.Encounter)

            self._validate(Observation)
            self.response = Observation.create(server=self.connect2server().server)
            Observation.id = self._extract_id()
            self.Observation = Observation
            print(self)

    def __str__(self):
        return f'{self.Observation.__class__.__name__}:{self.obs}; id: {self.Observation.id}'

    @staticmethod
    def __repr__():
        return 'GenerateObservation()'

if __name__ == '__main__':
    obs_dict = generateobservationdict.GenerateObservationDict()
    obs = GenerateObservation(obs_dict.observation_dict,Patient=obs_dict.Patient)
    labs = generatefparlabs.GenerateFparLabs()
    GenerateObservation(labs.lab_dict,Patient=obs.Patient,Practitioner=obs.Practitioner,Encounter=obs.Encounter)
