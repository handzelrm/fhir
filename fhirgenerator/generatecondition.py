import generatebase
import generatepatient

import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.condition as cond

import random
import pandas as pd
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class GenerateCondition(generatebase.GenerateBase):

    def __init__(self, Patient=None):

        if Patient == None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient

        self._generate_icd_code()

        Condition = cond.Condition()
        Condition.clinicalStatus = 'active'
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.code = self.icd_code
        Coding.display = self.icd_description
        CodeableConcept.coding = [Coding]
        Condition.code = CodeableConcept


        # Patient_FHIRReference = fr.FHIRReference()
        # Patient_FHIRReference.reference = f'Patient/{self.Patient.id}'
        Condition.subject = self._create_FHIRReference(self.Patient)

        self._validate(Condition)
        self.response = Condition.create(server=self.connect2server().server)
        Condition.id = self._extract_id()
        self.Condition = Condition
        self.Condition.Patient = self.Patient

    def _generate_icd_code(self):
        df = pd.read_excel('../demographic_files/common_obgyn_visits_parsed.xlsx',sheet_name='for OPA')
        icd_list = []
        for row in df.iterrows():
            icd_list += row[1][0]*[row[1][1]]
        self.icd_code = random.choice(icd_list)
        self.icd_description = df[df.code==self.icd_code].description.values[0]


if __name__ == '__main__':
	GenerateCondition()
