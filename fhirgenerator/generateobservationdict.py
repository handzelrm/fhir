import generatebase
import generatepatient
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class GenerateObservationDict(generatebase.GenerateBase):

    def __init__(self, Patient=None):
        """
        Generates  self.observation_dict dictionary that will be used in the GenerateObservation module.

        :param Patient: Patient FHIR object.
        """
        if Patient == None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient

        self.smoke_code, self.smoke_description = self._get_smoking_loinc()
        self._generate_gravidity_and_parity(self.Patient)
        self.sbp, self.dbp, self.hr = self._generate_vitals()
        self.height, self.weight = self._generate_height_weight(self.Patient.gender)
        self._get_household_income()
        self._get_pregnancy_status()
        self.insurance = self._get_fpar_random_value('Insurance Coverage Type')
        self.payer = self._get_fpar_random_value('Payer for Visit')
        self.preg_reporting_method = self._get_fpar_random_value('Pregnancy Status Reporting Method')
        self.preg_intent = self._get_fpar_random_value('Pregnancy Intention')
        self.ever_had_sex = self._get_fpar_random_value('Ever Had Sex')
        self.sex_3_mo = self._get_fpar_random_value('Sex Last 3 Months')
        self.sex_12_mo = self._get_fpar_random_value('Sex Last 12 Months')
        self.contraceptive_intake = self._get_fpar_random_value('Contraceptive Method at Intake')
        self.contraceptive_exit = self._get_fpar_random_value('Contraceptive Method at Exit')
        # '428071000124103'

        self.observation_dict = {
            'sbp': {'system':'http://loinc.org','type':'quantity','code':'8480-6','display':'Systolic Blood Pressure (mmHg)','unit':'mmHg','value':self.sbp},
            'dbp': {'system':'http://loinc.org','type':'quantity','code':'8462-4','display':'Diastolic Blood Pressure (mmHg)','unit':'mmHg','value':self.dbp},
            'hr': {'system':'http://loinc.org','type':'quantity','code':'8867-4','display':'Heart Rate (bpm)','unit':'bpm','value':self.hr},
            'height': {'system':'http://loinc.org','type':'quantity','code':'8302-2','display':'Height (inches)','unit':'inches','value':self.height},
            'weight': {'system':'http://loinc.org','type':'quantity','code':'29463-7','display':'Weight (pounds)','unit':'pounds','value':self.weight},
            'smoke': {'system':'http://loinc.org','type':'codeable_x2','code':'72166-2','display':None,'valueCode':self.smoke_code,'valueSystem':'http://snomed.info/sct','valueDisplay':self.smoke_description}

            # 'parity': {'system':'http://loinc.org','type':'quantity','code':'11977-6','display':'Parity','unit':None,'value':self.parity},
            # 'gravidity': {'system':'http://loinc.org','type':'quantity','code':'11977-6','display':f'{self.gravidity} Pregnancies','unit':'Pregnancies','value':self.gravidity},
            # 'income':{'system':'http://loinc.org','type':'codeable','code':'77244-2','display':'Total combined household income range in last year','value_loinc':self.income_loinc,'value_display':self.income_range},
            # 'pregnancy':{'system':'http://loinc.org','type':'codeable','code':'82810-3','display':'Pregnancy Status','value_loinc':self.pregnancy_loinc,'value_display':self.pregnancy_display},
            # 'insurance': {'system':'http://loinc.org','type':'codeable','code':'52556-8','display':'Insurance Coverage','value_loinc':None, 'value_display':self.insurance},
            # 'payer': {'system':'http://loinc.org','type':'codeable','code':'76437-3','display':'Payer of Visit','value_loinc':None, 'value_display':self.payer},
            # 'preg_reporting_method': {'system':'http://loinc.org','type':'codeable','code':'86643-4','display':'Pregnancy Status Reporting Method','value_loinc':None, 'value_display':self.preg_reporting_method},
            # 'preg_intent': {'system':'http://loinc.org','type':'codeable','code':'86645-9','display':'Pregnancy Intention','value_loinc':None, 'value_display':self.preg_intent},
            # 'ever_had_sex': {'system':'http://loinc.org','type':'codeable','code':'86646-7','display':'Ever Had Sex','value_loinc':None, 'value_display':self.ever_had_sex},
            # 'sex_3_mo': {'system':'http://loinc.org','type':'codeable','code':'86647-5','display':'Sex Last 3 Months','value_loinc':None, 'value_display':self.sex_3_mo},
            # 'sex_12_mo': {'system':'http://loinc.org','type':'codeable','code':'86648-3','display':'Sex Last 12 Months','value_loinc':None, 'value_display':self.sex_12_mo},
            # 'contraceptive_intake': {'system':'http://loinc.org','type':'codeable','code':'86649-1','display':'Contraceptive Method at Intake','value_loinc':None, 'value_display':self.contraceptive_intake},
            # 'contraceptive_exit': {'system':'http://loinc.org','type':'codeable','code':'86651-7','display':'Contraceptive at Exit','value_loinc':None, 'value_display':self.contraceptive_exit}
            }
        # self.observation_dict['smoke']['code'] = '8517006'

        # if self.contraceptive_intake == None:
        #     self.reason_no_contraceptive_intake = self._get_fpar_random_value('Reason for no contraceptive method at intake')
        #     self.observation_dict['reason_no_contraceptive_intake'] = {'system':'http://loinc.org','type':'codeable','code':'86650-9','display':'Reason for no contraceptive method at intake','value_loinc':None, 'value_display':self.reason_no_contraceptive_intake}
        # if self.contraceptive_exit is None:
        #     self.reason_no_contraceptive_exit = self._get_fpar_random_value('Reason for no contraceptive method at exit')
        #     self.observation_dict['reason_no_contraceptive_exit'] = {'system':'http://loinc.org','type':'codeable','code':'86651-7','display':'Reason for no contraceptive method at exit','value_loinc':None, 'value_display':self.reason_no_contraceptive_exit}
        # else:
        #     self.how_contraceptive_exit = self._get_fpar_random_value('How Contraceptive Method Was Provided At Exit')
        #     self.observation_dict['how_contraceptive_exit'] = {'system':'http://loinc.org','type':'codeable','code':'86652-5','display':'How was contraceptive method provided at exit','value_loinc':None, 'value_display':self.how_contraceptive_exit}
        # print(self.observation_dict['smoke']['code'])
if __name__ == '__main__':
    GernerateObservationDict()
