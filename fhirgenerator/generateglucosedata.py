import generatebase
import generateobservation
import generateencounter

import numpy as np
import datetime
import random
import calendar

class GenerateGlucoseData(generatebase.GenerateBase):

    average_glucose = 120

    def __init__(self):

        self.glucose = self.average_glucose
        self._generate_value()
        self._generate_period()

        self.observation_dict = {}
        {'type':'quantity','loinc':'41653-7','display':'Glucose [Mass/​volume] in Capillary blood by Glucometer','unit':'mg/dL','value':self.glucose}

    def _generate_value(self):
        self.glucose += np.random.normal(0,5*10)
        self.glucose = int(abs(self.glucose))

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


if __name__ == '__main__':
    glucose_dict = GenerateGlucoseData()
    inpt_encounter = generateencounter.GenerateEncounter(Period=glucose_dict.Period)
    print(inpt_encounter.Period.start)
    # generateobservation.GenerateObservation(glucose_dict,)