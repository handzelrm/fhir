import generatebase
import generatepatient
import generateencounter
import generatemedication
import fhirclient.models.medicationadministration as ma
import fhirclient.models.dosage as dos
import datetime

class GenerateMedicationAdministration(generatebase.GenerateBase):


    def __init__(self, Patient=None, Medication=None, Encounter=None):
        if Medication is None:
            raise ValueError('Need Medication')
        else:
            self.Medication = Medication

        if Patient is None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient

        if Encounter is None:
            self.Encounter = generateencounter.GenerateEncounter().Encounter
        else:
            self.Encounter = Encounter

        MedicationAdministration = ma.MedicationAdministration()
        MedicationAdministration.status = 'completed'
        MedicationAdministration.medicationReference = self._create_FHIRReference(self.Medication)
        MedicationAdministration.subject = self._create_FHIRReference(self.Patient)
        MedicationAdministration.effectiveDateTime = self._create_FHIRDate(datetime.datetime.now())
        MedicationAdministration.context = self._create_FHIRReference(self.Encounter)
        MedicationAdministrationDosage = ma.MedicationAdministrationDosage()
        MedicationAdministrationDosage.dose = 10
        MedicationAdministrationDosage.text = 'testing'
        # MedicationAdministrationDosage
        # MedicationAdministrationDosage
        # Dosage = dos.Dosage()
        # Dosage.text = 'Test Drug'
        # Dosage.doseQuantity = 10
        # MedicationAdministration.dosage = Dosage
        MedicationAdministration.as_json()

        self._validate(MedicationAdministration)
        self.response = MedicationAdministration.create(self.connect2server().server)
        MedicationAdministration.id = self._extract_id()
        self.MedicationAdministration = MedicationAdministration
        self.MedicationAdministration.Patient = self.Patient
        self.MedicationAdministration.Encounter = self.Encounter
        print(self)

    def __str__(self):
        return f'{self.MedicationAdministration.__class__.__name__}; id: {self.MedicationAdministration.id}'

    @staticmethod
    def __repr__():
        return 'GenerateMedicationAdministration()'

if __name__ == '__main__':
    GenerateMedicationAdministration(Medication={'glargine':{'rx_code':'274783','form_code':'385219001','form_display':'Injection solution'}})
