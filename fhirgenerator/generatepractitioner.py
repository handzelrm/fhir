import generatebase

import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.humanname as hn
import fhirclient.models.practitioner as pr
import random
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class GeneratePractitioner(generatebase.GenerateBase):
    def __init__(self):
        """
        Uses fhirclient.models to create and post practitoner resource. Currently, using class variables.

        :param smart: fhirclient.client.FHIRClient object.
        :returns: practitioner id created by server
        """
        Practitioner = pr.Practitioner()
        PractitionerQualification = pr.PractitionerQualification()
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.code = random.choice(['MD','DO'])
        Coding.system = 'https://www.hl7.org/fhir/v2/0360/2.7/index.html'
        CodeableConcept.coding = [Coding]
        PractitionerQualification.code = CodeableConcept
        Practitioner.qualification = [PractitionerQualification]
        name = hn.HumanName()
        self.family, self.given, self.gender = self._generate_person()
        name.family = self.family
        name.given = self.given
        Practitioner.gender = self.gender
        Practitioner.name = [name]

        self._validate(Practitioner)
        self.response = Practitioner.create(self.connect2server().server)
        Practitioner.id = self._extract_id()
        self.Practitioner = Practitioner
        print(self)

    def __str__(self):
        return f'{self.Practitioner.__class__.__name__}:{self.family},{self.given[0]}; id: {self.Practitioner.id}'

    @staticmethod
    def __repr__():
        return 'GeneratePractitioner()'

if __name__ == '__main__':
	GeneratePractitioner()
