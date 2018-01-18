import fhirclient.models.address as a
import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.encounter as enc
import fhirclient.models.extension as e
import fhirclient.models.fhirdate as fd
import fhirclient.models.fhirreference as fr
import fhirclient.models.humanname as hn
import fhirclient.models.location as l
import fhirclient.models.observation as o
import fhirclient.models.patient as p
import fhirclient.models.practitioner as pr
import fhirclient.models.quantity as q
# import fhirclient.models.reference as r
import fhirclient.models.valueset as v
from fhirclient import client
from fhirclient import server
from fhirclient import auth

import json
import pandas as pd
import numpy as np
import random
import requests
# from datetime import date,timedelta
import calendar
import re
import datetime
import random
import calendar
import matplotlib.pyplot as plt
from scipy.stats import gamma
import os

class patient():
    
    def __init__(self):   
        fname_dict,lname_list,street_list,state_list,zipcode_df = self._pt_generator()
        self.gender = random.choice(['male']+['female']*19) #95% women
        self.fname = random.choice(fname_dict[self.gender])
        self.lname = random.choice(lname_list)
        self.bday = self.generate_bday()
        self.address_number = random.randint(1,9999)
        self.address_street = random.choice(street_list)
        city_state_zip = random.randint(0,zipcode_df.shape[0])
        self.city = zipcode_df.loc[city_state_zip].City
        self.state = zipcode_df.loc[city_state_zip].State
        self.zipcode = str(zipcode_df.loc[city_state_zip].Zipcode)
        self.get_race_coding()
        self.get_ethnicity_coding()
        self.smart = self.connect2server()
        self.id = self.generate_fhir_object()      
    
    def __str__(self):
        return f'Name:{self.lname},{self.fname}; id:{self.id}'
    
    @staticmethod
    def __repr__():
        return 'patient()'
    
    @staticmethod
    def _pt_generator():
        """
        creates the data used in generator function
        """
        fname_dict = {}
        df = pd.read_excel('./fhir/common_fnames.xlsx')
        fname_dict['male'] = df.men.tolist()
        fname_dict['female'] = df.women.tolist()
        
        lname_list = []
        df = pd.read_excel('./fhir/common_lnames.xlsx')
        lname_list = df.lname.tolist()
        
        street_list = ['Second', 'Third', 'First', 'Fourth', 'Park', 'Fifth', 'Main', 'Sixth', 'Oak', 'Seventh', 'Pine', 'Maple', 'Cedar', 'Eighth', 'Elm', 'View', 'Washington', 'Ninth', 'Lake', 'Hill']
        df = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
        state_list = df[0][0].tolist().remove('Abbreviation')
        zipcode_df = pd.read_csv('./fhir/zipcodes.csv')

        return fname_dict,lname_list,street_list,state_list,zipcode_df
    
    @staticmethod
    def generate_age():
        a = 28
        min_val = 13
        max_val = 50
        r = gamma.rvs(a,1)
        if int(r)<min_val or int(r)>max_val:
            r = generate_age()
        return int(r)
    
    def generate_bday(self):
        """
        Uses a gamma distribution to determine age.
        The age is then subtracted from the current year.
        Random month and day are selected
        """
        age = self.generate_age()
        today = datetime.date.today()
        month = random.choice(range(1,13))
        year = today.year-age
        last_day = calendar.monthrange(year,month)[1]
        day = random.choice(range(1,last_day+1))
        bday = datetime.date(year,month,day)
        return bday
    
    def get_race_coding(self):
        df = pd.read_html('http://hl7.org/fhir/ValueSet/v2-0005')[2]    
        df.columns = df.iloc[0,:]
        df = df.iloc[1:,0:3]
        self.race_description = random.choice(df.Description.tolist())
        self.race_code = df[df.Description==self.race_description].Code.values[0]
        self.race_system = df[df.Description==self.race_description].System.values[0]

    
    def get_ethnicity_coding(self):
        self.ethnicity_system = 'http://hl7.org/fhir/v3/Ethnicity'
        df = pd.read_html(self.ethnicity_system)[2]
        df.columns = df.iloc[0,:]
        df = df[df.Level=='1']
        df = df.iloc[0:,1:3]
        self.ethnicity_description = random.choice(df.Display.tolist())
        self.ethnicity_code = df[df.Display==self.ethnicity_description].Code.values[0]
    
    @staticmethod
    def connect2server():
        """
        Currently hard coded to connect to fhirtest
        """
        settings = {
        'app_id': 'hand_testing',
        'scope':'user/*.write',
        'api_base': 'http://api-v5-stu3.hspconsortium.org/stu3/open/'
        }

        smart = client.FHIRClient(settings=settings)
        smart.prepare()
        return smart

    def generate_fhir_object(self):
        Patient = p.Patient()
        HumanName = hn.HumanName()
        HumanName.family = self.lname
        HumanName.given = [self.fname]
        Patient.name = [HumanName]
        Patient.gender = self.gender
        birthDay = fd.FHIRDate()
        birthDay.date = self.bday
        Patient.birthDate = birthDay
        Address = a.Address()
        Address.country = 'USA'
        Address.postalCode = self.zipcode
        Address.state = self.state
        Address.city = self.city
        Address.line = [f'{self.address_number} {self.address_street}']
        Address.use = 'home'
        Address.type = 'postal'
        Patient.active = True
        Patient.address = [Address]
        
#         race = e.Extension()
#         race.url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'
#         us_core = e.Extension()
#         us_core.url = 'http://hl7.org/fhir/ValueSet/v2-0005'
#         coding = c.Coding()
#         coding.system = self.race_system
#         coding.code = self.race_code
#         coding.display = self.race_description
#         us_core.valueCoding = coding
#         race.extension = [us_core]
        
#         ethnicity = e.Extension()
#         ethnicity.url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity'
#         us_core = e.Extension()
#         us_core.url = 'http://hl7.org/fhir/v3/Ethnicity'
#         coding = c.Coding()
#         coding.system = self.ethnicity_system
#         coding.code = self.ethnicity_code
#         coding.display = self.ethnicity_description
#         us_core.valueCoding = coding
#         ethnicity.extension = [us_core]
#         Patient.extension = [race,ethnicity]
                           
        validate = self.smart.server.post_json(path='Patient/$validate',resource_json=Patient.as_json())
        if validate.status_code != 200:
            raise ValueError('Validation Error')
        
        response = Patient.create(self.smart.server)
        re_id = re.compile(r'Patient/(\d+)/')
        id = re_id.search(response['text']['div']).group(1)
        print(f'Name:{self.lname},{self.fname}; id:{id}')
        return id
        
class lab_value_sets(object):
        
    def __init__(self,ResourceType,StructureDefinition):
        self.ResourceType = ResourceType
        self.LoincSet = []
        self.loinc = None
    
        self.jdata = self.json_request(self.ResourceType,StructureDefinition)
        self.dict_search()
        self.valueset = self.hard_valueset()
        
    @staticmethod    
    def read_json(file):
        with open(file,'r') as f:
            jdata = json.load(f)
        return jdata
    
    @staticmethod
    def json_request(ResourceType,StructureDefinition):
        """
        hspc server hard coded
        """
        r = requests.get(f'https://api-v5-stu3.hspconsortium.org/stu3/open/{ResourceType}?_id={StructureDefinition}&_format=json')
        return r.json()
        
    def hard_valueset(self):
        """
        hard coded to all_lab_values.xlsx document
        """
        if self.loinc==None:
            return None
        df = pd.read_excel('./fhir/all_lab_values.xlsx')
        valueset_list = df[df.loinc==self.loinc].value.tolist()        
        return valueset_list
        
    def dict_search(self,data=None):
        if data == None:
            data = self.jdata
        for k,v in data.items():
            
            #parsing loinc
            if k=='system' and v=='http://loinc.org': 
                try: 
                    isinstance(data['concept'],list)
                    for loinc_dict in data['concept']:
                        self.LoincSet.append(loinc_dict['code'])
                except KeyError:
                    self.loinc = data['code']
            elif k=='min' and int(v)==1:
                try:
                    print(f"id:{data['id']}")
                    pass
                except KeyError:
                    print(f"path:{data['path']}") 
                    pass
            if isinstance(v,dict):
                self.dict_search(v)
            elif isinstance(v,list):
                self.list_search(v)                

    def list_search(self,data):
        if data == None:
            data = self.jdata
        for i,v in enumerate(data):
            if isinstance(v,dict):
                self.dict_search(v)
            elif isinstance(v,list):
                self.list_search(v)
                
class observations():
        
    def __init__(self,server,pt,year_range,sex):
        self.server = server
        self.pt = pt
        self.generate_dt(year_range)
        self.sex = sex
        
        self.smoke_loinc, self.smoke_description = self.get_smoking_loinc()
        
        self.hiv = lab_value_sets('ValueSet','FPARHIVTests')
        self.ct_gc = lab_value_sets('ValueSet','FPARchlamydiaTrachomatisAndNeisseriaGonorrhoeaeCombinedTests')
        self.ct = lab_value_sets('ValueSet','FPARchlamydiaTrachomatisTests')
        self.gc = lab_value_sets('ValueSet','FPARneisseriaGonorrhoeaeTests')
        self.hpv = lab_value_sets('ValueSet','FPARhumanPapillomaVirusTests')
        self.pap = lab_value_sets('ValueSet','FPARpapSmearTests')
        self.preg = lab_value_sets('ValueSet','FPARpregnancyTests')
        self.income = lab_value_sets('ValueSet','FPARannualHouseholdIncomeRanges')
        
        self.create_all_vitals()

        self.practitioner_given = 'Robert'
        self.practitioner_family = 'Handzel'
        self.practitioner_id = '2807'
        self.generate_lab_df()

        self.create_labs(self.hiv)
        separate_or_combined = random.choice(['separate','combined'])
        if separate_or_combined == 'separate':
            self.create_labs(self.ct)
            self.create_labs(self.gc)
        elif separate_or_combined == 'combined':
            self.create_labs(self.ct_gc)
        else:
            raise ValueError('Issue with code')
        self.create_labs(self.hpv)
    
    def create_all_vitals(self):
        self.add_vitals()
        self.create_vitals('sbp')
        self.create_vitals('dbp')
        self.create_vitals('hr')
        self.create_vitals('height')
        self.create_vitals('weight')
        self.create_vitals('smoke')
    
    def add_vitals(self):
        try: 
            test = self.sbp
            test = self.dbp
            test = self.hr
            change = int(np.random.normal(0,1)*10)
            self.sbp += change
            self.dbp += change
            change = int(np.random.normal(0,1)*10)
            self.hr += change
        except AttributeError:
             self.sbp, self.dbp, self.hr = self.generate_vitals()
        try:
            test = self.height
            test = self.weight
            change = int(np.random.normal(0,1))
            self.height += change
            change = int(np.random.normal(0,1)*10)
            self.weight += change
        except AttributeError:
            self.height, self.weight = self.generate_height_weight(self.sex)
    
    @staticmethod
    def get_smoking_loinc():
        df = pd.read_html('https://s.details.loinc.org/LOINC/72166-2.html?sections=Comprehensive')[5]
        df.columns = df.iloc[3,:]
        df = df.iloc[4:,[3,5]]
        df.columns = ['description','loinc']
        smoke_description = random.choice(df.description.tolist())
        smoke_loinc = df[df.description==smoke_description].loinc.values[0]
        return smoke_loinc, smoke_description
  
    def create_vitals(self, measurement):
        
        if measurement == 'sbp':
            loinc = '8480-6'
            display = 'Systolic Blood Pressure (mmHg)'
            unit = 'mmHg'
            value = self.sbp
        elif measurement == 'dbp':
            loinc = '8462-4'
            display = 'Diastolic Blood Pressure (mmHg)'
            unit = 'mmHg'
            value = self.dbp
        elif measurement == 'hr':
            loinc = '8867-4'
            display = 'Heart Rate (bpm)'
            unit = 'bpm'
            value = self.hr
        elif measurement == 'height':
            loinc = '8302-2'
            display = 'Height (inches)'
            unit = 'inches'
            value = self.height
        elif measurement == 'weight':
            loinc = '29463-7'
            display = 'Weight (pounds)'
            unit = 'pounds'
            value = self.weight
        elif measurement == 'smoke':
            loinc = self.smoke_loinc
            display = self.smoke_description
            unit = None
            value = None
        else:
            raise ValueError('Measurement ValueError')
        
        vital = o.Observation()
        CodeableConcept = cc.CodeableConcept()
        coding = c.Coding()
        coding.system = 'http://loinc.org'
        coding.code = loinc
        coding.display = display

        CodeableConcept.coding = [coding]
        vital.code = CodeableConcept
        vital.status = 'final'

        pt_ref = fr.FHIRReference()
        pt_ref.reference = f'Patient/{self.pt}'
        vital.subject = pt_ref
    
        val = q.Quantity()
        val.value = value
        val.unit = unit
        vital.valueQuantity = val

        fhir_dt = fd.FHIRDate()
        fhir_dt.date = self.dt
        vital.effectiveDateTime = fhir_dt

        response = vital.create(server=self.server)

        return response
        
    @staticmethod
    def generate_vitals():   
        avg_sbp = 120
        avg_dbp  = 80

        diff = int(np.random.normal(0,1)*10)

        sbp = avg_sbp + diff
        dbp = avg_dbp + diff

        avg_hr = 80
        diff = int(np.random.normal(0,1)*10)
        hr = avg_hr + diff

        return sbp, dbp, hr
    
    def generate_dt(self,year_range):
        """
        recursive function to find a random datetime 
        """

        today = datetime.datetime.now()
        year = random.choice(year_range)
        month = random.choice(range(1,13))
        last_day = calendar.monthrange(year,month)[1]
        day = random.choice(range(1,last_day+1))

        minute = random.choice(range(60))
        hour = random.choice(range(24))
        second = random.choice(range(60))

        dt = datetime.datetime(year,month,day,hour,minute,second)

        if today<dt:
            generate_dt(year_range)

        self.dt = dt
    
    @staticmethod
    def generate_height_weight(sex):
        # https://www.cdc.gov/nchs/fastats/body-measurements.htm
        #could not find great reference for weight std
        avg_height_male = 69.2
        std_height_male = 4
        avg_height_female = 63.7
        std_height_female = 3.5
        
        avg_weight_male = 195.7
        std_weight_male = 30
        avg_weight_female = 168.5
        std_weight_female = 25
    
        if sex == 'male':
            height = np.random.normal(avg_height_male,std_height_male)
            weight = np.random.normal(avg_weight_male,std_weight_male)
        elif sex == 'female':
            height = np.random.normal(avg_height_female,std_height_female)
            weight = np.random.normal(avg_weight_female,std_weight_female)
        else:
            raise ValueError('sex error')
                        
        return height, weight
    
    def generate_Practitioner(self):
        Practitioner = pr.Practitioner()
        PractitionerQualification = pr.PractitionerQualification()
        CodeableConcept = cc.CodeableConcept()
        coding = c.Coding()
        coding.code = 'MD'
        coding.system = 'https://www.hl7.org/fhir/v2/0360/2.7/index.html'
        CodeableConcept.coding = [coding]
        PractitionerQualification.code = CodeableConcept
        Practitioner.qualification = [PractitionerQualification]
        name = hn.HumanName()
        name.given = [self.practitioner.given]
        name.family = self.practitioner.family
        Practitioner.name = [name]
        return provider

    
    def check_for_missing_labs(self,lab):
        lab_loinc = random.choice(lab.LoincSet)
        lab_value_list = self.lab_df[self.lab_df.loinc==lab_loinc].value.values
        lab_name_list = self.lab_df[self.lab_df.loinc==lab_loinc].lab_name.values
        if len(lab_value_list)==0:
            lab_loinc, lab_value, lab_name = self.check_for_missing_labs(lab)
        else:
            lab_value = random.choice(lab_value_list)
            lab_name = random.choice(lab_name_list)
        return lab_loinc, lab_value, lab_name
    
    def create_labs(self,lab):
        lab_loinc, lab_value, lab_name = self.check_for_missing_labs(lab)
        
        Observation = o.Observation()
        Observation.status = 'final'
        CodeableConcept = cc.CodeableConcept()
        coding = c.Coding()
        coding.code = lab_loinc
        coding.system = 'http://loinc.org'
        coding.display = lab_name
        CodeableConcept.coding = [coding]
        CodeableConcept.text = lab_name
        Patient_FHIRReference = fr.FHIRReference()
        Patient_FHIRReference.reference = f'Patient/{self.pt}'
        Observation.subject = Patient_FHIRReference
        Observation.code = CodeableConcept
        Observation.valueString = lab_value

        Practitioner_FHIRReference = fr.FHIRReference()
        Practitioner_FHIRReference.reference = f'Practitioner/{self.practitioner_id}'
        Observation.performer = [Practitioner_FHIRReference]
        
        FHIRDate = fd.FHIRDate()
        FHIRDate.date = self.dt
        Observation.effectiveDateTime = FHIRDate
        
        response = Observation.create(self.server)
        
    def generate_lab_df(self):
        lab_list = []
        loinc_list = []
        value_list = []
        df = pd.read_excel('./fhir/labs.xlsx')
        for row in df.iterrows():
            possible_values = row[1].value
            if possible_values is not np.nan:
                for value in possible_values.split('\n'):
                    lab_list.append(row[1].lab)
                    loinc_list.append(row[1].loinc)
                    value_list.append(value)
        df = pd.DataFrame({'lab_name':lab_list,'loinc':loinc_list,'value':value_list})
        df = df.replace('Not detected', 'Not Detected')
        df = df.replace('Nonreactive', 'Non-reactive')
        df = df.replace('Inconclusive', 'Indeterminate') #could not find better mapping
        df = df.replace('Equivocal', 'Indeterminate')
        
        self.lab_df = df

#currently will create a patient, print their id and name, create a set of lab/vital obvservations all with the same datetime, and create a second set of vitals with a second datetime
if __name__ == '__main__':
    pt = patient()
    obs = observations(pt.smart.server, pt.id, range(2000,2018),pt.gender)
    obs.generate_dt(range(2000,2018))
    obs.create_all_vitals()
