import generatebase
import generatepatient
import generatepractitioner
import generateencounter

import fhirclient.models.referralrequest as rr

import datetime

class GenerateReferralRequest(generatebase.GenerateBase):

    def __init__(self,Patient=None, Practitioner_agent=None, Practitioner_recipient=None, Encounter=None):
        """Uses fhirclient.models to create referral resource"""

        if Patient is not None and Encounter is not None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Conditition.Patient.id.')
            self.Patient = Patient
            self.Encounter = Encounter
        elif Encounter is None and Patient is None:
            self.Encounter = generateencounter.GenerateEncounter().Encounter
            self.Patient = self.Encounter.Patient
        elif Encounter is not None and Patient is None:
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
        elif Encounter is None and Patient is not None:
            self.Patient = Patient
            self.Encounter = generateencounter.GenerateEncounter(Patient=self.Patient).Encounter
        else:
            raise ValueError('Error with Patient and Condition values')

        # if Patient == None:
        #     self.Patient = generatepatient.GeneratePatient().Patient
        # else:
        #     self.Patient = Patient

        if Practitioner_agent == None:
            self.Practitioner_agent = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner_agent = Practitioner_agent

        if Practitioner_recipient == None:
            self.Practitioner_recipient = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner_recipient = Practitioner_recipient

        # if Encounter == None:
        #     self.Encounter = generateencounter.GenerateEncounter(Patient=self.Patient, Location=None, Condition=None).Encounter
        # else:
        #     self.Encounter = Encounter


        ReferralRequest = rr.ReferralRequest()
        ReferralRequestRequester = rr.ReferralRequestRequester()

        ReferralRequestRequester.agent = self._create_FHIRReference(self.Practitioner_agent)
        ReferralRequest.recipient = [self._create_FHIRReference(self.Practitioner_recipient)]

        ReferralRequest.status = 'active'
        ReferralRequest.intent = 'order'

        ReferralRequest.occurrenceDateTime = self._create_FHIRDate(datetime.datetime.now()+datetime.timedelta(days=14))
        ReferralRequest.authoredOn = self._create_FHIRDate(datetime.datetime.now())
        ReferralRequest.context = self._create_FHIRReference(self.Encounter)
        ReferralRequest.subject = self._create_FHIRReference(self.Patient)

        ReferralRequest.requester = ReferralRequestRequester
        ReferralRequest.as_json()

#         self._validate(ReferralRequest)
        self.response = ReferralRequest.create(server=self.connect2server().server)
        ReferralRequest.id = self._extract_id()
        self.ReferralRequest = ReferralRequest
        self.ReferralRequest.Patient = self.Patient
        self.ReferralRequest.Practitioner_agent = self.Practitioner_agent
        self.ReferralRequest.Practitioner_recipient = self.Practitioner_recipient
        self.ReferralRequest.Encounter = self.Encounter

if __name__ == '__main__':
    GenerateReferralRequest()