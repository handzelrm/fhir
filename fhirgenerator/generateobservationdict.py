import generatebase
import generatepatient


class GenerateObservationDict(generatebase.GenerateBase):

    def __init__(self, Patient=None):

        if Patient == None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient

        self.smoke_loinc, self.smoke_description = self._get_smoking_loinc()
        self._generate_gravidity_and_parity(self.Patient)
        self.sbp, self.dbp, self.hr = self._generate_vitals()
        self.height, self.weight = self._generate_height_weight(self.Patient.gender)
        self._get_household_income()
        self._get_pregnancy_status()

        self.observation_dict = {
            'sbp': {'type':'quantity','loinc':'8480-6','display':'Systolic Blood Pressure (mmHg)','unit':'mmHg','value':self.sbp},
            'dbp': {'type':'quantity','loinc':'8462-4','display':'Diastolic Blood Pressure (mmHg)','unit':'mmHg','value':self.dbp},
            'hr': {'type':'quantity','loinc':'8867-4','display':'Heart Rate (bpm)','unit':'bpm','value':self.hr},
            'height': {'type':'quantity','loinc':'8302-2','display':'Height (inches)','unit':'inches','value':self.height},
            'weight': {'type':'quantity','loinc':'29463-7','display':'Weight (pounds)','unit':'pounds','value':self.weight},
            'smoke': {'type':'quantity','loinc':self.smoke_loinc,'display':self.smoke_description,'unit':None,'value':None},
            'parity': {'type':'quantity','loinc':'11977-6','display':'Parity','unit':None,'value':self.parity},
            'gravidity': {'type':'quantity','loinc':'11977-6','display':f'{self.gravidity} Pregnancies','unit':'Pregnancies','value':self.gravidity},
            'income':{'type':'codeable','loinc':'77244-2','display':'Total combined household income range in last year','value_loinc':self.income_loinc,'value_display':self.income_range},
            'pregnancy':{'type':'codeable','loinc':'82810-3','display':'Pregnancy Status','value_loinc':self.pregnancy_loinc,'value_display':self.pregnancy_display}
            }


if __name__ == '__main__':
    GernerateObservationDict()






