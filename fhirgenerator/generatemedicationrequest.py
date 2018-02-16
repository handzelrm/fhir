import generatebase
import generatepatient
import generatemedication

import fhirclient.models.medicationrequest as medreq
import fhirclient.models.patient as p

import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class GenerateMedicationRequest(generatebase.GenerateBase):
    def __init__(self,Patient=None, Medication=None):
        if Patient is None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient

        if Medication is None:
            self.Medication = generatemedication.GenerateMedication().Medication
        else:
            self.Medication = Medication

        MedicationRequest = medreq.MedicationRequest()
        MedicationRequest.status = 'active'
        MedicationRequest.intent = 'order'
        MedicationRequest.medicationReference = self._create_FHIRReference(self.Medication)
        MedicationRequest.subject = self._create_FHIRReference(self.Patient)

        self.response = MedicationRequest.create(server=self.connect2server().server)
        MedicationRequest.id = self._extract_id()

        self.MedicationRequest = MedicationRequest


    def test():
        pass


if __name__ == '__main__':
    Medication = generatemedication.GenerateMedication()
    GenerateMedicationRequest()
