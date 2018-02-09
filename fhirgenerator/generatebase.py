import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.fhirdate as fd
import fhirclient.models.fhirreference as fr
import fhirclient.models.period as period
import fhirclient.models.quantity as q
from fhirclient import client
from fhirclient import server
from fhirclient import auth
import json
import pandas as pd
import numpy as np
import random
import requests
import re
import datetime

class GenerateBase():

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
        
        if sex =='unknown':
            sex = random.choice(['male','female'])
    
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

    @staticmethod 
    def _create_FHIRReference(resource):
        FHIRReference = fr.FHIRReference()
        FHIRReference.reference = f'{resource.resource_type}/{resource.id}'
        return FHIRReference

    @staticmethod
    def _create_FHIRDate(date):
        FHIRDate = fd.FHIRDate()
        FHIRDate.date = date
        return FHIRDate
    
    def _create_FHIRPeriod(self,start=None,end=None):
        Period = period.Period()
        if start is not None:
            Period.start = self._create_FHIRDate(start)
        else:
            Period.start = self._create_FHIRDate(datetime.datetime.now())
        if end is not None:
            Period.end = self._create_FHIRDate(end)
        return Period

    # @staticmethod
    def _extract_id(self):
        # regex = re.compile(r'"[a-z]+/(\d+)/',re.IGNORECASE)
        regex = re.compile(r'\/(.*?)\/',re.IGNORECASE)
        id = regex.search(self.response['issue'][0]['diagnostics']).group(1)
        return id
    
    @staticmethod
    def _create_FHIRCodeableConcept(code,system,display):
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.code = code
        Coding.system = system
        Coding.display = display
        CodeableConcept.coding = [Coding]
        return CodeableConcept
    
    def _validate(self,resource):
        validate = self.connect2server().server.post_json(path=f'{resource.resource_type}/$validate',resource_json=resource.as_json())
        if validate.status_code != 200:
            raise ValueError(f'Validation Error: {resource.resouce_type}')

    @staticmethod
    def connect2server():
        """Hard coded to connect to HSPC v5 server."""
        settings = {
            'app_id': 'hand_testing',
            'scope':'user/*.write',
            # 'api_base': 'http://api-v5-stu3.hspconsortium.org/stu3/open/'
            # 'api_base': 'https://api-v5-stu3.hspconsortium.org/dmDBMI/open'
            # 'api_base': 'https://api-v5-stu3.hspconsortium.org/handzelFPAR/open'
            # 'api_base': 'https://api-v5-stu3.hspconsortium.org/handzel/open'
            'api_base': 'https://api-v5-stu3.hspconsortium.org/handzelTest/open'
        }
        smart = client.FHIRClient(settings=settings)
        smart.prepare()
        return smart

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

    @staticmethod
    def _generate_person():        

        name_first_dict = {}
        df = pd.read_excel('../demographic_files/common_name_first.xlsx')
        name_first_dict['male'] = df.men.tolist()
        name_first_dict['female'] = df.women.tolist()
        
        name_last_list = []
        df = pd.read_excel('../demographic_files/common_name_last.xlsx')
        name_last_list = df.name_last.tolist()

        gender = random.choice(['male','female'])
        name_first = random.choice(name_first_dict[gender])
        name_last = random.choice(name_last_list)

        return name_last, [name_first], gender

        
    def _add_quantity_value(self,Observation,measurement):
        """
        Adds a quantity value object to Observation.
        
        :param Observation: fhirclient.models.observation.Observation object
        :param measurement: measurement dictionary
        :returns: Observation object
        """       
        Quantity = q.Quantity()
        Quantity.value = self.observation_dict[measurement]['value']
        Quantity.unit = self.observation_dict[measurement]['unit']
        Observation.valueQuantity = Quantity
        return Observation
    
    def _add_codeable_value(self,Observation,measurement):
        """
        Adds a codeableconcept value object to Observation.
        
        :param Observation: fhirclient.models.observation.Observation object
        :param measurement: measurement dictionary
        :returns: Observation Object
        """
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.system = 'http://loinc.org'
        Coding.code = self.observation_dict[measurement]['value_loinc']
        Coding.display = self.observation_dict[measurement]['value_display']
        CodeableConcept.coding = [Coding]
        Observation.valueCodeableConcept = CodeableConcept
        return Observation

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
        
        if sex =='unknown':
            sex = random.choice(['male','female'])
    
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

    def _get_household_income(self):
        df = pd.read_html('https://r.details.loinc.org/LOINC/77244-2.html?sections=Comprehensive')[4]
        df = df.iloc[4:,[3,5]]
        df.columns = ['income_range','answer_id']
        self.income_range = random.choice(df.income_range.tolist())
        self.income_loinc = df[df.income_range == self.income_range].answer_id.values[0]
        
    def _get_pregnancy_status(self):
        """Currently hardcoded to give Not Pregnant"""
        df = pd.read_html('https://s.details.loinc.org/LOINC/82810-3.html')[5]
        df = df.iloc[4:,[3,5]]
        df.columns = ['pregnancy_display','pregnancy_id']
        df.iloc[2,0] = 'Unknown'
        self.pregnancy_display = df[df.pregnancy_display == 'Not pregnant'].pregnancy_display.values[0]
        #     pregnancy_display = random.choice(df.pregnancy_display.tolist())
        self.pregnancy_loinc = df[df.pregnancy_display == self.pregnancy_display].pregnancy_id.values[0]

    def _generate_gravidity_and_parity(self,patient):
        """Generates a gravidity and parity between 0 and 6"""
        if patient.gender == 'male':
            self.gravidity = 0
        else:
            self.gravidity = random.choice(range(7))
        if self.gravidity == 0:
            self.parity = 0
        else:
            self.parity = self.gravidity - random.choice(range(self.gravidity))

    def _get_fpar_random_value(self,item_name):
        df = pd.read_excel('../demographic_files/valueset.xlsx',sheet_name='Sheet1')
        df = df.fillna('N/A')
        item_value = df[df.item == item_name].valueset.tolist()
        return random.choice(item_value)

