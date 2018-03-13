# from fhirgenerator
import generatebase

import fhirclient.models.address as a
import fhirclient.models.codeableconcept as cc
import fhirclient.models.coding as c
import fhirclient.models.extension as e
import fhirclient.models.fhirdate as fd
import fhirclient.models.humanname as hn
import fhirclient.models.patient as p

import pandas as pd
import random
import datetime
import calendar
from scipy.stats import gamma
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class GeneratePatient(generatebase.GenerateBase):
    def __init__(self):
        """Creates name, gender, birthday, address, race, ethnicity and patient's server id"""
        name_first_dict,name_last_list,street_list,state_list,zipcode_df = self._generate_patient_data()
        self.gender = random.choice(['male']*4+['female']*94+['unknown']*2) #95% women
        if self.gender == 'unknown':
            self.name_first = random.choice(name_first_dict[random.choice(['male','female'])])
        else:
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
        df = pd.read_excel('../demographic_files/common_name_first.xlsx')
        name_first_dict['male'] = df.men.tolist()
        name_first_dict['female'] = df.women.tolist()

        name_last_list = []
        df = pd.read_excel('../demographic_files/common_name_last.xlsx')
        name_last_list = df.name_last.tolist()

        street_list = ['Second', 'Third', 'First', 'Fourth', 'Park', 'Fifth', 'Main', 'Sixth', 'Oak', 'Seventh', 'Pine', 'Maple', 'Cedar', 'Eighth', 'Elm', 'View', 'Washington', 'Ninth', 'Lake', 'Hill']
        df = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
        state_list = df[0][0].tolist().remove('Abbreviation')
        zipcode_df = pd.read_csv('../demographic_files/zipcodes.csv')

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
        # df = pd.read_html('http://hl7.org/fhir/ValueSet/v2-0005')[2]
        # df.columns = df.iloc[0,:]
        # df = df.iloc[1:,0:3]
        # self.race_description = random.choice(df.Description.tolist())
        # self.race_code = df[df.Description==self.race_description].Code.values[0]
        # self.race_system = df[df.Description==self.race_description].System.values[0]
        df_list = pd.read_html('http://hl7.org/fhir/us/core/stu1/ValueSet-omb-race-category.html')
        df_omb = df_list[1].iloc[1:,:2]
        df_omb.columns = ['code', 'display']
        df_omb['system'] = 'ombCategory'
        df_list = pd.read_html('http://hl7.org/fhir/us/core/stu1/ValueSet-detailed-race.html')
        df_detailed = df_list[2].iloc[-1:,:2]
        df_detailed.columns = ['code', 'display']
        df_detailed['system'] = 'detailed'
        df = df_omb.append(df_detailed)
        self.race_display = random.choice(df.display.tolist())
        self.race_code = df[df.display==self.race_display].code.values[0]
        self.race_system = df[df.display==self.race_display].system.values[0]

    def _get_ethnicity_coding(self):
        """Uses FHIR valueset v3 to obtain and randomly choose an ethnicity"""
        self.ethnicity_system = 'http://hl7.org/fhir/v3/Ethnicity'
        df = pd.read_html(self.ethnicity_system)[2]
        df.columns = df.iloc[0,:]
        df = df[df.Level=='1']
        df = df.iloc[0:,1:3]
        self.ethnicity_description = random.choice(df.Display.tolist())
        self.ethnicity_code = df[df.Display==self.ethnicity_description].Code.values[0]

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
        PatientCommunication = p.PatientCommunication()
        PatientCommunication.language = self._create_FHIRCodeableConcept('en-US','urn:ietf:bcp:47','English')
        # PatientCommunication.language = self._create_FHIRCodeableConcept('en-US','http://hl7.org/fhir/ValueSet/languages','English')
        PatientCommunication.preferred = True
        Patient.communication = [PatientCommunication]

        race = e.Extension()
        race.url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'
        # race.url = 'http://hl7.org/fhir/us/core/ValueSet/omb-race-category'

        us_core = e.Extension()
        # us_core.url = 'http://hl7.org/fhir/us/core/ValueSet/omb-race-category'
        # us_core.url = 'http://hl7.org/fhir/us/core/ValueSet/detailed-race'

        # us_core.url = 'ombCategory'
        # us_core.valueCoding = self._create_FHIRCoding(self.race_code,'urn:oid:2.16.840.1.113883.6.238',self.race_description)
        us_core.url = self.race_system
        us_core.valueCoding = self._create_FHIRCoding(self.race_code,'urn:oid:2.16.840.1.113883.6.238',self.race_display)



        # race_detailed = e.Extension()
        # race_detailed.url = 'detailed'
        # race_detailed.valueCoding = self._create_FHIRCoding(self.race_code,'urn:oid:2.16.840.1.113883.6.238',self.race_description)
        race_text = e.Extension()
        race_text.url = 'text'
        race_text.valueString = self.race_display
        race.extension = [us_core,race_text]

        ethnicity = e.Extension()
        ethnicity.url = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity'

        us_core = e.Extension()
        us_core.url = 'ombCategory'
        us_core.valueCoding = self._create_FHIRCoding(self.ethnicity_code,'urn:oid:2.16.840.1.113883.6.238',self.ethnicity_description)
        ethnicity_text = e.Extension()
        ethnicity_text.url = 'text'
        ethnicity_text.valueString = self.ethnicity_description
        ethnicity.extension = [us_core,ethnicity_text]

        Patient.extension = [race,ethnicity]

        # Currently the server valdiation throws a 500 error if race and ethnicity extentions are present
        self._validate(Patient)

        self.response = Patient.create(self.smart.server)
        Patient.id = self._extract_id()
        print(f'{Patient.__class__.__name__}:{self.name_last},{self.name_first}; id: {Patient.id}')
        # return Patient.id
        self.Patient = Patient

if __name__ == '__main__':
    GeneratePatient()
