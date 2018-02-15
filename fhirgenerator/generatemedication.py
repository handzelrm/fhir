import generatebase
import fhirclient.models.medication as med
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class GenerateMedication(generatebase.GenerateBase):

    def __init__(self):
        Medication = med.Medication()
        Medication.code = self._create_FHIRCodeableConcept('Placeholder for code')
        Medication.form = self._create_FHIRCodeableConcept('Placeholder for form')
        Medication.status = 'active'
        # Medication.ingredient = [self._create_FHIRCodeableConcept('Placeholder')]

        MedicationIngredient = med.MedicationIngredient()
        # # MedicationIngredient.isActive = True
        MedicationIngredient.itemCodeableConcept = self._create_FHIRCodeableConcept('test')

        # print(MedicationIngredient.item)
        # print(MedicationIngredient.as_json())
        # Medication.ingredient = [MedicationIngredient]
        print(Medication.as_json())

        # MedicationIngredient = med.MedicationIngredient()
        # MedicationIngredient.item = []

        print(MedicationIngredient.as_json())





# CodeableConcept = cc.CodeableConcept()
#         Coding = c.Coding()
#         Coding.code = 'en-US'
#         Coding.system = 'http://hl7.org/fhir/ValueSet/languages'
#         Coding.display = 'English'
#         CodeableConcept.coding = [Coding]

if __name__ == '__main__':
    GenerateMedication()
