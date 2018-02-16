import generatebase
import fhirclient.models.medication as med
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class GenerateMedication(generatebase.GenerateBase):

    def __init__(self,medication_dict):
        """
        Creates FHIR Medication resources from a dictionary.

        :param medication_dict: dictionary of medications that are looped through
        """
        self.medication_dict = medication_dict

        for obs,value in self.medication_dict.items():

            Medication = med.Medication()
            Medication.code = self._create_FHIRCodeableConcept(value['rx_code'], system='http://www.nlm.nih.gov/research/umls/rxnorm')
            Medication.form = self._create_FHIRCodeableConcept(value['form_code'], display=value['form_code'],system='http://hl7.org/fhir/ValueSet/medication-form-codes')

            Medication.status = 'active'
            MedicationIngredient = med.MedicationIngredient()
            MedicationIngredient.isActive = True
            MedicationIngredient.itemCodeableConcept = self._create_FHIRCodeableConcept('test')

            self.response = Medication.create(server=self.connect2server().server)
            Medication.id = self._extract_id()

            self.Medication = Medication


if __name__ == '__main__':
    medication_dict = {'glargine':{'rx_code':'274783','form_code':'385219001','form_display':'Injection solution'}}
    GenerateMedication(medication_dict)
