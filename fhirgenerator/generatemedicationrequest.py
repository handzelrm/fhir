import generatebase
import fhirclient.models.medicationrequest as medreq


class GenerateMedicationRequest(generatebase.GenerateBase):
    def __init__(self):
        MedicationRequest = medreq.MedicationRequest()
        print(MedicationRequest.as_json())
        # MedicationRequest.
        
        

if __name__ == '__main__':
    GenerateMedicationRequest()