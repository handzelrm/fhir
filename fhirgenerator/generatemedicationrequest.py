import generatebase
import generatepatient

import fhirclient.models.medicationrequest as medreq
import fhirclient.models.patient as p

import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class GenerateMedicationRequest(generatebase.GenerateBase):
    def __init__(self,Patient=None):
        if Patient == None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient


        MedicationRequest = medreq.MedicationRequest()
        MedicationRequest.status = 'active'
        MedicationRequest.intent = 'order'
        MedicationRequest.medicationReference = 'medication'
        MedicationRequest.subject = self._create_FHIRReference(self.Patient)

        print(MedicationRequest.as_json())

    def test():
        pass


if __name__ == '__main__':

    GenerateMedicationRequest()
