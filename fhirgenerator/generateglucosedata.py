import generatebase
import generateobservation
import generateencounter

import numpy as np
import datetime
import random
import calendar
import argparse

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
        'glucose':{'type':'quantity','loinc':'41653-7','display':'Glucose [Mass/​volume] in Capillary blood by Glucometer','unit':'mg/dL','value':self.glucose}
        }

        for i in range(len(self.a1c_value)):
            self.a1c_dict[f'a1c_{i}'] = {'type':'quantity', 'loinc':'4548-4', 'display':'Hemoglobin A1c','unit':'%', 'value':self.a1c_value[i]}


    def _generate_glucose(self):
        self.glucose += np.random.normal(0,5*10)
        self.glucose = int(abs(self.glucose))

    def _generate_a1c(self):
        self.a1c_value = []
        for i in range(random.randint(1,4)):
            self.a1c_value.append(random.randint(6,13))

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
        # print(admission)
        self.Period =  self._create_FHIRPeriod(admission)

    def _loop_generator(self,qxh):
        self.Encounter = generateencounter.GenerateEncounter(Period=self.Period).Encounter
        self.dt = self.Encounter.Period.start.date
        generateobservation.GenerateObservation(self.a1c_dict,dt=self.dt,Encounter=self.Encounter)
        while self.dt < datetime.datetime.now():
            generateobservation.GenerateObservation(self.glucose_dict,dt=self.dt,Encounter=self.Encounter)
            self.dt += datetime.timedelta(hours=qxh)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('qxh', help='How frequently to create glucose values (i.e. every x hours) and needs to be int.', type=int)
    args = parser.parse_args()
    glucose = GenerateGlucoseData()
    glucose._loop_generator(args.qxh)

if __name__ == '__main__':
    main()
