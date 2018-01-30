import generatebase

class GenerateObservation(generatebase.GenerateBase):
    year_range = range(2017,datetime.date.today().year+1)
    
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
    
    practitioner_id_2 = 6315
    practitioner_given_2 = 'Steve'
    practitioner_family_2 = 'Hasley'
    practitioner_qualification_2 = 'MD'
    
    def __init__(self,patient):
        """Takes a TestPatient object and creates vitals, height, weight, smoking history, labs, and encounters."""
        self.patient = patient       
        
        self.condition_id_list = []
        for i in range(1,random.choice([2,3])):
            self._generate_icd_code()
            self._create_condition()
            self.condition_id_list.append(self.condition_id)
        self.condition_id = random.choice(self.condition_id_list)
        
        self._create_encounter()
        self._generate_dt()    
        self.smoke_loinc, self.smoke_description = self._get_smoking_loinc()
        self._generate_gravidity_and_parity(patient)
        
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
        
        self._get_household_income()
        self._get_pregnancy_status()
        
        
        self._update_observation_dict()
        
        self._create_all_observations()
        self._generate_lab_df()
        self._create_referral()
        self._create_new_task()

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
        self._create_labs(self.pap)
        self._create_labs(self.preg)
        
    def __str__(self):
        return f'Name:{self.name_last},{self.name_first}; id:{self.id}'
    
    @staticmethod
    def __repr__():
        return 'TestObservations(TestPatient())'
    
    def _update_observation_dict(self):
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
    
    def _create_all_observations(self):
        """Creates basic vitals, height, weight, and smoking status and posts to server."""
        for key in self.observation_dict:
            self._create_observation(key)
            
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
  
    def _create_observation(self, measurement):
        """Uses fhirclient.models to create and send vitals to server."""
        Observation = o.Observation()
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.system = 'http://loinc.org'
        Coding.code = self.observation_dict[measurement]['loinc']
        Coding.display = self.observation_dict[measurement]['display']

        CodeableConcept.coding = [Coding]
        Observation.code = CodeableConcept
        Observation.status = 'final'

        Patient_Reference = fr.FHIRReference()
        Patient_Reference.reference = f'Patient/{self.patient.id}'
        Observation.subject = Patient_Reference
    
        if self.observation_dict[measurement]['type'] == 'quantity':
            Observation = self._add_quantity_value(Observation,measurement)
        elif self.observation_dict[measurement]['type'] == 'codeable':
            Observation = self._add_codeable_value(Observation,measurement)
        else:
            raise ValueError('Measurement Type ValueError')

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
        else:
            self.dt = dt
        
    def create_another_encounter(self):
        """Creates another encounter with new datetime, labs, and vitals"""
        self._generate_dt()
        self._create_encounter()
                
        change = int(np.random.normal(0,1)*5)
        self.sbp += change
        self.dbp += change
        change = int(np.random.normal(0,1)*5)
        self.hr += change
        
        change = int(np.random.normal(0,1)*0.5)
        self.height += change
        change = int(np.random.normal(0,1)*5)
        self.weight += change
        self._update_observation_dict()
        self._create_all_observations()
        self._update_completed_task()
        
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
        Observation.subject = self._create_FHIRReference('Patient',self.patient.id)       
        Observation.code = CodeableConcept
        Observation.valueString = lab_value       
        Observation.performer = [self._create_FHIRReference('Practitioner',self.practitioner_id)]
        Observation.effectiveDateTime = self._create_FHIRDate(self.dt)          
        Observation.context = self._create_FHIRReference('Encounter',self.encounter_id)
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
        
    def _create_condition(self):
        Condition = cond.Condition()
        CodeableConcept = cc.CodeableConcept()
        Coding = c.Coding()
        Coding.code = self.icd_code
        Coding.display = self.icd_description
        CodeableConcept.coding = [Coding]
        Condition.code = CodeableConcept
        
        Patient_FHIRReference = fr.FHIRReference()
        Patient_FHIRReference.reference = f'Patient/{self.patient.id}'
        Condition.subject = Patient_FHIRReference
                
#         self._validate(Condition)
        response = Condition.create(server=self.patient.smart.server)
        self.condition_id = self._extract_id(response)
#         re_id = re.compile(r'Condition/(\d+)/')
#         self.condition_id = re_id.search(response['text']['div']).group(1)
        
    def _create_referral(self):
        """Uses fhirclient.models to create referral resource"""
        ReferralRequest = rr.ReferralRequest()
        ReferralRequestRequester = rr.ReferralRequestRequester()

        ReferralRequestRequester.agent = self._create_FHIRReference('Practitioner',self.practitioner_id)
        ReferralRequest.recipient = [self._create_FHIRReference('Practitioner',self.practitioner_id_2)]

        ReferralRequest.status = 'active'
        ReferralRequest.intent = 'order'

        ReferralRequest.occurrenceDateTime = self._create_FHIRDate(datetime.datetime.now()+datetime.timedelta(days=14))
        ReferralRequest.authoredOn = self._create_FHIRDate(datetime.datetime.now())
        ReferralRequest.context = self._create_FHIRReference('Encounter',self.encounter_id)
        ReferralRequest.subject = self._create_FHIRReference('Patient',self.patient.id)

        ReferralRequest.requester = ReferralRequestRequester
        ReferralRequest.as_json()

#         self._validate(ReferralRequest)
        response = ReferralRequest.create(server=pt.smart.server)
        ReferralRequest.id = self._extract_id(response)
        self.ReferralRequest = ReferralRequest
        
    def _create_new_task(self):
        Task = t.Task()
        Task.status = 'requested'
        Task.intent = 'order'

        Task.executionPeriod = self._create_FHIRPeriod(start=datetime.datetime.now())

        TaskRequester = t.TaskRequester()
        TaskRequester.agent = self._create_FHIRReference('Practitioner',self.practitioner_id)
        Task.requester = TaskRequester

        Task_Restriction = t.TaskRestriction()
        Task_Restriction.recipient = [self._create_FHIRReference('Practitioner',self.practitioner_id_2)]
        Task.restriction = Task_Restriction

        Task.for_fhir = self._create_FHIRReference('Patient',self.patient.id)
        Task.context = self._create_FHIRReference('Encounter',self.encounter_id)

        Task.basedOn = [self._create_FHIRReference('ReferralRequest',self.ReferralRequest.id)]
        
#         self._validate(Task)
        response = Task.create(self.patient.smart.server)
        Task.id = _extract_id(response)
        self.Task = Task
        
    def _update_completed_task(self):
        self.Task.status = 'completed'
        self.Task.executionPeriod = self._create_FHIRPeriod(end=datetime.datetime.now())
        self.Task.focus = self._create_FHIRReference('Encounter',self.encounter_id)
        self.Task.update(self.patient.smart.server)
    
            
    def _create_encounter(self):
        """Uses fhirclient.models to create encounter resource"""
        Encounter = enc.Encounter()
        Coding = c.Coding()
        Coding.code = 'outpatient'
        Encounter.class_fhir = Coding

        Encounter.status = 'finished'
        
        EncounterLocation = enc.EncounterLocation()
        EncounterLocation.location = self._create_FHIRReference('Location',self.location_id)        
        Encounter.location = [EncounterLocation]
      
        Encounter.subject = self._create_FHIRReference('Patient',self.patient.id)
        
        EncounterDiagnosis = enc.EncounterDiagnosis()
        EncounterDiagnosis.condition = self._create_FHIRReference('Condition',self.condition_id)        
        Encounter.diagnosis = [EncounterDiagnosis]
    
        self._validate(Encounter)
        response = Encounter.create(server=self.patient.smart.server)
        self.encounter_id = self._extract_id(response)
        
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
    
    def _generate_icd_code(self):
        df = pd.read_excel('./fhir/common_obgyn_visits_parsed.xlsx',sheetname='for OPA')
        icd_list = []
        for row in df.iterrows():
            icd_list += row[1][0]*[row[1][1]]
        self.icd_code = random.choice(icd_list)
        self.icd_description = df[df.code==self.icd_code].description.values[0]
    
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
        
    @staticmethod 
    def _create_FHIRReference(resource,id):
        FHIRReference = fr.FHIRReference()
        FHIRReference.reference = f'{resource}/{id}'
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
        if end is not None:
            Period.end = self._create_FHIRDate(end)
        return Period

    @staticmethod
    def _extract_id(response):
        regex = re.compile(r'"[a-z]+/(\d+)/',re.IGNORECASE)
        id = regex.search(response['issue'][0]['diagnostics']).group(1)
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
        validate = self.patient.smart.server.post_json(path=f'{resource.resource_type}/$validate',resource_json=resource.as_json())
        if validate.status_code != 200:
            raise ValueError(f'Validation Error: {resource.resouce_type}')
        
    
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
        name.given = [cls.practitioner_given_2]
        name.family = cls.practitioner_family_2
        Practitioner.name = [name]
        response = Practitioner.create(server=smart.server)
        re_id = re.compile(r'Practitioner/(\d+)/')
        practitioner_id = re_id.search(response['text']['div']).group(1)
        print(practitioner_id)
        return practitioner_id        