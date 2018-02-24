import generatebase
import generatepatient
import generatepractitioner

import fhirclient.models.composition as comp

import datetime

class FparComposition(generatebase.GenerateBase):
    def __init__(self, Patient=None, Practitioner=None):
        if Patient is None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient
        if Practitioner is None:
            self.Practitioner = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner = Practitioner
        Composition = comp.Composition()
        Composition.date = self._create_FHIRDate(datetime.datetime.now())
        Composition.status = 'final'
        Composition.type = self._create_FHIRCodeableConcept('placeholder')
        Composition.subject = self._create_FHIRReference(self.Patient)
        Composition.author = [self._create_FHIRReference(self.Practitioner)]
        Composition.title = 'FPAR!'
        # Composition.as_json()
        Composition.create(server=self.connect2server().server)

if __name__ == '__main__':
    FparComposition()
