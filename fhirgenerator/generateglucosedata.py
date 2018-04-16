import generatebase
import generatepatient
import generateobservation
import generateencounter
import generatemedication
import generatemedicationadministration
import rxnormclassmeds

import numpy as np
import datetime
from pytz import timezone
import random
import calendar
import argparse
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class GenerateGlucoseData(generatebase.GenerateBase):

    average_glucose = 120

    def __init__(self):

        self.glucose = self.average_glucose
        self._generate_glucose()
        self._generate_period()
        self._generate_a1c()
        self.a1c_dict = {}

        self.glucose_dict = {
        'glucose':{'system':'http://loinc.org', 'type':'quantity','code':'41653-7','display':'Glucose [Mass/​volume] in Capillary blood by Glucometer','unit':'mg/dL','value':self.glucose}
        }

        # for i in range(len(self.a1c_value)):
            # self.a1c_dict[f'a1c_{i}'] = {'system':'http://loinc.org', 'type':'quantity', 'code':'4548-4', 'display':'Hemoglobin A1c','unit':'%', 'value':self.a1c_value[i]}
        self.a1c_dict['a1c'] = {'system':'http://loinc.org', 'type':'quantity', 'code':'4548-4', 'display':'Hemoglobin A1c','unit':'%', 'value':self.a1c_value}

        long_acting = rxnormclassmeds.RxnormClassMeds('A10AE')
        drug = random.choice(list(long_acting.drug_dict))
        rx_code = long_acting.drug_dict[drug]['drug_id']
        form_code = long_acting.drug_dict[drug]['drug_doseforms'][0]['doseform_code']
        form_display = long_acting.drug_dict[drug]['drug_doseforms'][0]['doseform_name']
        self.long_acting_dict = {f'drug':{'rx_code':rx_code,'form_code':form_code,'form_display':form_display}}


    def _generate_glucose(self):
        # print(self.glucose)
        self.glucose += np.random.normal(0,5*10)
        self.glucose = int(abs(self.glucose))

    def _generate_a1c(self):
        # self.a1c_value = []
        # for i in range(random.randint(1,4)):
            # self.a1c_value.append(random.randint(6,13))
        self.a1c_value = random.randint(6,13)

    def _generate_period(self):
        # year = random.randint(2017,2018)
        # month = random.randint(1,12)

        # last_day = calendar.monthrange(year,month)[1]
        # day = random.randint(1,last_day)

        # hour = random.randint(0,23)
        # minute = random.randint(0,59)
        # second = random.randint(0,59)

        # admission = datetime.datetime(year=year,month=month,day=day,minute=minute,hour=hour,second=second)
        days = random.randint(0,14)
        hours = random.randint(0,23)
        minutes = random.randint(0,59)
        admission = datetime.datetime.now()-datetime.timedelta(days=days,hours=hours,minutes=minutes)
        self.Period =  self._create_FHIRPeriod(admission)

    def _loop_generator(self,qxh):
        self.Patient = generatepatient.GeneratePatient().Patient
        self.Encounter = generateencounter.GenerateEncounter(Period=self.Period, Patient=self.Patient).Encounter
        self.dt = self.Encounter.Period.start.date
        generateobservation.GenerateObservation(self.a1c_dict,dt=self.dt,Encounter=self.Encounter)
        while self.dt < datetime.datetime.now().astimezone(timezone('US/Eastern')):
            generateobservation.GenerateObservation(self.glucose_dict,dt=self.dt,Encounter=self.Encounter)
            self._generate_glucose()
            self.glucose_dict['glucose']['value'] = self.glucose
            self.dt += datetime.timedelta(hours=qxh)
        # self.Medication = generatemedication.GenerateMedication(self.long_acting_dict).Medication
        # self.MedicationAdministration = generatemedicationadministration.GenerateMedicationAdministration(Patient=self.Patient, Medication=self.Medication, Encounter=self.Encounter)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--qxh', help='How frequently to create glucose values (i.e. every x hours) and needs to be int.', default=6, type=int)
    args = parser.parse_args()
    glucose = GenerateGlucoseData()
    glucose._loop_generator(args.qxh)

if __name__ == '__main__':
    main()
