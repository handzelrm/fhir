import generatebase
import rxnormclassmeds
import fhirclient.models.medication as med
import random
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
            Medication.code = self._create_FHIRCodeableConcept(value['rx_code'], system='http://www.nlm.nih.gov/research/umls/rxnorm',display=value['form_display'])
            Medication.form = self._create_FHIRCodeableConcept(value['form_code'], display=value['form_display'],system='http://hl7.org/fhir/ValueSet/medication-form-codes')

            Medication.status = 'active'
            MedicationIngredient = med.MedicationIngredient()
            MedicationIngredient.isActive = True
            MedicationIngredient.itemCodeableConcept = self._create_FHIRCodeableConcept('test')

            self.response = Medication.create(server=self.connect2server().server)
            Medication.id = self._extract_id()

            self.Medication = Medication


if __name__ == '__main__':
    long_acting = rxnormclassmeds.RxnormClassMeds('A10AE')
    # print(long_acting.drug_dict)
    # print(long_acting.drug_dict.items())
    drug = random.choice(list(long_acting.drug_dict))
    # print(long_acting.drug_dict[drug])
    rx_code = long_acting.drug_dict[drug]['drug_id']
    form_code = long_acting.drug_dict[drug]['drug_doseforms'][0]['doseform_code']
    form_display = long_acting.drug_dict[drug]['drug_doseforms'][0]['doseform_name']

    # medication_dict = {'glargine':{'rx_code':'274783','form_code':'385219001','form_display':'Injection solution'}}
    medication_dict = {f'drug':{'rx_code':rx_code,'form_code':form_code,'form_display':form_display}}
    GenerateMedication(medication_dict)
