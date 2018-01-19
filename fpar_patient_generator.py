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
import fhirclient.models.valueset as v
from fhirclient import client
from fhirclient import server
from fhirclient import auth

import json
import pandas as pd
import numpy as np
import random
import requests
import calendar
import re
import datetime
import random
import calendar
import matplotlib.pyplot as plt
from scipy.stats import gamma
import os

class TestPatient:    
    def __init__(self):
        """Creates name, gender, birthday, address, race, ethnicity and patient's server id"""
        name_first_dict,name_last_list,street_list,state_list,zipcode_df = self._generate_patient_data()
        self.gender = random.choice(['male']+['female']*19) #95% women
        self.name_first = random.choice(name_first_dict[self.gender])
        self.name_last = random.choice(name_last_list)
        self.bday = self._generate_bday()
        self.address_number = random.randint(1,9999)
        self.address_street = random.choice(street_list)
        city_state_zip = random.randint(0,zipcode_df.shape[0])
        self.city = zipcode_df.loc[city_state_zip].City
        self.state = zipcode_df.loc[city_state_zip].State
        self.zipcode = str(zipcode_df.loc[city_state_zip].Zipcode)
        self._get_race_coding()
        self._get_ethnicity_coding()
        self.smart = self.connect2server()
        self.id = self._generate_patient_fhir_object()      
    
    def __str__(self):
        return f'Name:{self.name_last},{self.name_first}; id:{self.id}'
    
    @staticmethod
    def __repr__():
        return 'TestPatient()'
    
    @staticmethod
    def _generate_patient_data():
        """Picks random patient data from multiple sources"""
        name_first_dict = {}
        df = pd.read_excel('./fhir/common_name_first.xlsx')
        name_first_dict['male'] = df.men.tolist()
        name_first_dict['female'] = df.women.tolist()
        
        name_last_list = []
        df = pd.read_excel('./fhir/common_name_last.xlsx')
        name_last_list = df.name_last.tolist()
        
        street_list = ['Second', 'Third', 'First', 'Fourth', 'Park', 'Fifth', 'Main', 'Sixth', 'Oak', 'Seventh', 'Pine', 'Maple', 'Cedar', 'Eighth', 'Elm', 'View', 'Washington', 'Ninth', 'Lake', 'Hill']
        df = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
        state_list = df[0][0].tolist().remove('Abbreviation')
        zipcode_df = pd.read_csv('./fhir/zipcodes.csv')

        return name_first_dict,name_last_list,street_list,state_list,zipcode_df
    
    @staticmethod
    def _generate_age():
        """Generates a random age between 13 and 50 using a gamma distribution."""
        a = 28
        min_val = 13
        max_val = 50
        r = gamma.rvs(a,1)
        if int(r)<min_val or int(r)>max_val:
            r = generate_age()
        return int(r)
    
    def _generate_bday(self):
        """Generates a random birthday and uses _generate_age() to determine year."""
        age = self._generate_age()
        today = datetime.date.today()
        month = random.choice(range(1,13))
        year = today.year-age
        last_day = calendar.monthrange(year,month)[1]
        day = random.choice(range(1,last_day+1))
        bday = datetime.date(year,month,day)
        return bday
    
    def _get_race_coding(self):
        """Uses FHIR valueset v2 to obtain and randomly choose a race."""
        df = pd.read_html('http://hl7.org/fhir/ValueSet/v2-0005')[2]    
        df.columns = df.iloc[0,:]
        df = df.iloc[1:,0:3]
        self.race_description = random.choice(df.Description.tolist())
        self.race_code = df[df.Description==self.race_description].Code.values[0]
        self.race_system = df[df.Description==self.race_description].System.values[0]

    def _get_ethnicity_coding(self):
        """Uses FHIR valueset v3 to obtain and randomly choose an ethnicity"""
        self.ethnicity_system = 'http://hl7.org/fhir/v3/Ethnicity'
        df = pd.read_html(self.ethnicity_system)[2]
        df.columns = df.iloc[0,:]
        df = df[df.Level=='1']
        df = df.iloc[0:,1:3]
        self.ethnicity_description = random.choice(df.Display.tolist())
        self.ethnicity_code = df[df.Display==self.ethnicity_description].Code.values[0]
    
    @staticmethod
    def connect2server():
        """Hard coded to connect to HSPC v5 server."""
        settings = {
            'app_id': 'hand_testing',
            'scope':'user/*.write',
            'api_base': 'http://api-v5-stu3.hspconsortium.org/stu3/open/'
        }
        smart = client.FHIRClient(settings=settings)
        smart.prepare()
        return smart

    def _generate_patient_fhir_object(self):
        """Creates a test patient using fhirclient.models."""
        Patient = p.Patient()
        HumanName = hn.HumanName()
        HumanName.family = self.name_last
        HumanName.given = [self.name_first]
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
        
        race = e.Extension()
        race.url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'
        us_core = e.Extension()
        us_core.url = 'http://hl7.org/fhir/ValueSet/v2-0005'
        Coding = c.Coding()
        Coding.system = self.race_system
        Coding.code = self.race_code
        Coding.display = self.race_description
        us_core.valueCoding = Coding
        race.extension = [us_core]
        
        ethnicity = e.Extension()
        ethnicity.url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity'
        us_core = e.Extension()
        us_core.url = 'http://hl7.org/fhir/v3/Ethnicity'
        Coding = c.Coding()
        Coding.system = self.ethnicity_system
        Coding.code = self.ethnicity_code
        Coding.display = self.ethnicity_description
        us_core.valueCoding = Coding
        ethnicity.extension = [us_core]
        Patient.extension = [race,ethnicity]
        
        # Currently the server valdiation throws a 500 error if race and ethnicity extentions are present                           
#         validate = self.smart.server.post_json(path='Patient/$validate',resource_json=Patient.as_json())
#         if validate.status_code != 200:
#             raise ValueError('Validation Error')
        
        response = Patient.create(self.smart.server)
        re_id = re.compile(r'Patient/(\d+)/')
        patient_id = re_id.search(response['text']['div']).group(1)
        print(f'Name:{self.name_last},{self.name_first}; id:{patient_id}')
        return patient_id    
    
   class LabValueSet:        
    def __init__(self,ResourceType,StructureDefinition):
        """Creates object with resource type and list of LOINC codes"""
        self.ResourceType = ResourceType
        self.LoincSet = []
        self.loinc = None    
        self.jdata = self.json_request(self.ResourceType,StructureDefinition)
        self.dict_search()
        self.valueset = self.hard_valueset()
     
    def __str__(self):
        return f'ResourceType:{self.ResourceType}, LOINC ValueSet:{self.LoincSet}'
    
    @staticmethod
    def __repr__():
        return 'LabValueSet(ResourceType,StructureDefinition)'
    
        
    @staticmethod    
    def read_json(file):
        """Reads json file and returns json object"""
        with open(file,'r') as f:
            jdata = json.load(f)
        return jdata
    
    @staticmethod
    def json_request(ResourceType,StructureDefinition):
        """Searches HSPC server v5 to obtain StructuredDefinitions."""
        r = requests.get(f'https://api-v5-stu3.hspconsortium.org/stu3/open/{ResourceType}?_id={StructureDefinition}&_format=json')
        return r.json()
        
    def hard_valueset(self):
        """Hard coded to all_lab_values.xlsx document."""
        if self.loinc==None:
            return None
        df = pd.read_excel('./fhir/all_lab_values.xlsx')
        valueset_list = df[df.loinc==self.loinc].value.tolist()        
        return valueset_list
        
    def dict_search(self,data=None):
        """Recursive function that works in conjuction with list_search.  Hard coded for looking up LOINC codes."""
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
        """Recursive function that works in conjuction with dict_search."""
        if data == None:
            data = self.jdata
        for i,v in enumerate(data):
            if isinstance(v,dict):
                self.dict_search(v)
            elif isinstance(v,list):
                self.list_search(v)
  
class TestObservations: 
    year_range = range(2000,datetime.date.today().year+1)
    
    location_id = 3602
    location_status = 'active'
    location_name = 'UPMC Magee Clinic'
    location_line = ["Magee-Women's Hospital of UPMC, Halket Street"]
    location_city = 'Pittsburgh'
    location_postalCode = '15213'
    location_state = 'PA'
    location_latitude = 40.437123
    location_longitude = -79.960779
    
    practitioner_id = 2807
    practitioner_given = 'Robert'
    practitioner_family = 'Handzel'
    practitioner_qualification = 'MD'
    
    def __init__(self,patient):
        """Takes a TestPatient object and creates vitals, height, weight, smoking history, labs, and encounters."""
        self.patient = patient        
        self._generate_dt()    
        self.smoke_loinc, self.smoke_description = self._get_smoking_loinc()        
        
        self.hiv = LabValueSet('ValueSet','FPARHIVTests')
        self.ct_gc = LabValueSet('ValueSet','FPARchlamydiaTrachomatisAndNeisseriaGonorrhoeaeCombinedTests')
        self.ct = LabValueSet('ValueSet','FPARchlamydiaTrachomatisTests')
        self.gc = LabValueSet('ValueSet','FPARneisseriaGonorrhoeaeTests')
        self.hpv = LabValueSet('ValueSet','FPARhumanPapillomaVirusTests')
        self.pap = LabValueSet('ValueSet','FPARpapSmearTests')
        self.preg = LabValueSet('ValueSet','FPARpregnancyTests')
        self.income = LabValueSet('ValueSet','FPARannualHouseholdIncomeRanges')        
        
        self.sbp, self.dbp, self.hr = self._generate_vitals()
        self.height, self.weight = self._generate_height_weight(self.patient.gender)
        self._create_all_vitals()

        self._generate_lab_df()

        self._create_labs(self.hiv)
        separate_or_combined = random.choice(['separate','combined'])
        if separate_or_combined == 'separate':
            self._create_labs(self.ct)
            self._create_labs(self.gc)
        elif separate_or_combined == 'combined':
            self._create_labs(self.ct_gc)
        else:
            raise ValueError('Issue with code')
        self._create_labs(self.hpv)
        
    def __str__(self):
        return f'Name:{self.name_last},{self.name_first}; id:{self.id}'
    
    @staticmethod
    def __repr__():
        return 'TestObservations(TestPatient())'
    
    def _create_all_vitals(self):
        """Creates basic vitals, height, weight, and smoking status and posts to server."""
        self._create_vitals('sbp')
        self._create_vitals('dbp')
        self._create_vitals('hr')
        self._create_vitals('height')
        self._create_vitals('weight')
        self._create_vitals('smoke')
            
    @staticmethod
    def _generate_vitals():
        """Generates a set of vitals using a normal distribution times 10"""
        avg_sbp = 120
        avg_dbp  = 80
        diff = int(np.random.normal(0,1)*10)
        sbp = avg_sbp + diff
        dbp = avg_dbp + diff

        avg_hr = 80
        diff = int(np.random.normal(0,1)*10)
        hr = avg_hr + diff
        return sbp, dbp, hr
    
    @staticmethod
    def _generate_height_weight(sex):
        """Generates height and weight roughly inline with US stats."""
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
    
    @staticmethod
    def _get_smoking_loinc():
        """Uses a get request from LOINC to obtain a list of smoking statuses and returns a random one."""
        df = pd.read_html('https://s.details.loinc.org/LOINC/72166-2.html?sections=Comprehensive')[5]
        df.columns = df.iloc[3,:]
        df = df.iloc[4:,[3,5]]
        df.columns = ['description','loinc']
        smoke_description = random.choice(df.description.tolist())
        smoke_loinc = df[df.description==smoke_description].loinc.values[0]
        return smoke_loinc, smoke_description
  
    def _create_vitals(self, measurement):
        """Uses fhirclient.models to create and send vitals to server."""
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
        
        Observation = o.Observation()
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.system = 'http://loinc.org'
        Coding.code = loinc
        Coding.display = display

        CodeableConcept.coding = [Coding]
        Observation.code = CodeableConcept
        Observation.status = 'final'

        Patient_Reference = fr.FHIRReference()
        Patient_Reference.reference = f'Patient/{self.patient.id}'
        Observation.subject = Patient_Reference
    
        val = q.Quantity()
        val.value = value
        val.unit = unit
        Observation.valueQuantity = val

        fhir_dt = fd.FHIRDate()
        fhir_dt.date = self.dt
        Observation.effectiveDateTime = fhir_dt
        
        Encounter_Reference = fr.FHIRReference()
        Encounter_Reference.reference = f'Encounter/{self.encounter_id}'        
        Observation.context = Encounter_Reference      

        response = Observation.create(server=self.patient.smart.server)
        return response       

    def _generate_dt(self):
        """Recursive function to find a random datetime not past today's date"""
        self._create_encounter()

        today = datetime.datetime.now()
        year = random.choice(self.year_range)
        month = random.choice(range(1,13))
        last_day = calendar.monthrange(year,month)[1]
        day = random.choice(range(1,last_day+1))

        minute = random.choice(range(60))
        hour = random.choice(range(24))
        second = random.choice(range(60))

        dt = datetime.datetime(year,month,day,hour,minute,second)

        if today<dt:
            self._generate_dt()
        self.dt = dt
        
    def create_another_encounter(self):
        """Creates another encounter with new datetime, labs, and vitals"""
        self._generate_dt()
        
        change = int(np.random.normal(0,1)*5)
        self.sbp += change
        self.dbp += change
        change = int(np.random.normal(0,1)*5)
        self.hr += change
        
        change = int(np.random.normal(0,1)*0.5)
        self.height += change
        change = int(np.random.normal(0,1)*5)
        self.weight += change
        self._create_all_vitals()
        
    def _check_for_missing_labs(self,lab):
        """
        Checks to make sure that there are lab values available.
        
        :param lab: LabValueSet object.
        :returns: None
        """
        lab_loinc = random.choice(lab.LoincSet)
        lab_value_list = self.lab_df[self.lab_df.loinc==lab_loinc].value.values
        lab_name_list = self.lab_df[self.lab_df.loinc==lab_loinc].lab_name.values
        if len(lab_value_list)==0:
            lab_loinc, lab_value, lab_name = self._check_for_missing_labs(lab)
        else:
            lab_value = random.choice(lab_value_list)
            lab_name = random.choice(lab_name_list)
        return lab_loinc, lab_value, lab_name
    
    def _create_labs(self,lab):
        """
        Uses fhirclient.models to create and post lab Observation resource.
        
        :param lab: LabValueSet object.
        :returns: None
        """
        lab_loinc, lab_value, lab_name = self._check_for_missing_labs(lab)
        
        Observation = o.Observation()
        Observation.status = 'final'
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.code = lab_loinc
        Coding.system = 'http://loinc.org'
        Coding.display = lab_name
        CodeableConcept.coding = [Coding]
        CodeableConcept.text = lab_name
        Patient_FHIRReference = fr.FHIRReference()
        Patient_FHIRReference.reference = f'Patient/{self.patient.id}'
        Observation.subject = Patient_FHIRReference
        Observation.code = CodeableConcept
        Observation.valueString = lab_value

        Practitioner_FHIRReference = fr.FHIRReference()
        Practitioner_FHIRReference.reference = f'Practitioner/{self.practitioner_id}'
        Observation.performer = [Practitioner_FHIRReference]
        
        FHIRDate = fd.FHIRDate()
        FHIRDate.date = self.dt
        Observation.effectiveDateTime = FHIRDate
        
        Encounter_Reference = fr.FHIRReference()
        Encounter_Reference.reference = f'Encounter/{self.encounter_id}'        
        Observation.context = Encounter_Reference       
        response = Observation.create(self.patient.smart.server)
        
    def _generate_lab_df(self):
        """Generates a pandas dataframe of labs based on excel file."""
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
        
    def _create_encounter(self):
        """Uses fhirclient.models to create encounter resource"""
        Encounter = enc.Encounter()
        Coding = c.Coding()
        Coding.code = 'outpatient'
        Encounter.class_fhir = Coding

        Encounter.status = 'finished'

        EncounterLocation = enc.EncounterLocation()
        Location_FHIRReference = fr.FHIRReference()
        Location_FHIRReference.reference = f'Location/{self.location_id}'
        EncounterLocation.location = Location_FHIRReference
        Encounter.location = [EncounterLocation]

        Patient_FHIRReference = fr.FHIRReference()
        Patient_FHIRReference.reference = f'Patient/{self.patient.id}'
        Encounter.subject = Patient_FHIRReference

        response = Encounter.create(server=self.patient.smart.server)
        re_id = re.compile(r'Encounter/(\d+)/')
        self.encounter_id = re_id.search(response['text']['div']).group(1)        
    
    @classmethod
    def create_location(cls,smart):
        """
        Uses fhirclient.models to create and post location resource. Currently, using class variables.
        
        :param smart: fhirclient.client.FHIRClient object.
        :returns: practitioner id created by server 
        """
        Location = l.Location()
        LocationPosition = l.LocationPosition()
        Address = a.Address()
        Location.status = 'active'
        Location.name = cls.location_name
        Address.line = cls.location_line
        Address.city = cls.location_city
        Address.postalCode = cls.location_postalCode
        Address.state = cls.location_state
        Location.address = Address
        LocationPosition.latitude = cls.location_latitude
        LocationPosition.longitude = cls.location_longitude
        Location.position = LocationPosition
        response = Location.create(server=smart.server)
        re_id = re.compile(r'Location/(\d+)/')
        location_id = re_id.search(response['text']['div']).group(1)
        return location_id
    
    @classmethod
    def create_practitioner(cls,smart):
        """
        Uses fhirclient.models to create and post practitoner resource. Currently, using class variables.
        
        :param smart: fhirclient.client.FHIRClient object.
        :returns: practitioner id created by server        
        """
        Practitioner = pr.Practitioner()
        PractitionerQualification = pr.PractitionerQualification()
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.code = cls.practitioner_qualification
        Coding.system = 'https://www.hl7.org/fhir/v2/0360/2.7/index.html'
        CodeableConcept.coding = [Coding]
        PractitionerQualification.code = CodeableConcept
        Practitioner.qualification = [PractitionerQualification]
        name = hn.HumanName()
        name.given = [cls.practitioner_given]
        name.family = cls.practitioner_family
        Practitioner.name = [name]
        response = Practitioner.create(server=smart.server)
        re_id = re.compile(r'Practitioner/(\d+)/')
        practitioner_id = re_id.search(response['text']['div']).group(1)
        return practitioner_id        
             
if __name__ == '__main__':
    pt = TestPatient()
    obs = TestObservations(pt)
    obs.create_another_encounter()
