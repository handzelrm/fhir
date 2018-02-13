import generatebase
import generatepatient
import generatepractitioner
import generateencounter

import fhirclient.models.referralrequest as rr

import datetime

class GenerateReferralRequest(generatebase.GenerateBase):

    def __init__(self,Patient=None, Practitioner_agent=None, Practitioner_recipient=None, Encounter=None):
        """Uses fhirclient.models to create referral resource"""

        if Patient is not None and Encounter is not None and Practitioner_agent is not None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            if Encounter.Practitioner.id != Practitioner_agent.id:
                raise ValueError('Encounter.Practitioner.id must equal Practitioner.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.Practitioner_agent = Practitioner_agent
        elif Patient is not None and Encounter is not None and Practitioner_agent is None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must be the same as Encounter.Patient.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.Practitioner_agent = Encounter.Practitioner
        elif Patient is not None and Encounter is None and Practitioner_agent is not None:
            self.Patient = Patient
            self.Practitioner_agent = Practitioner_agent
            self.Encounter = generateencounter.GenerateEncounter(Patient=self.Patient,Practitioner=self.Practitioner_agent).Encounter
        elif Patient is not None and Encounter is None and Practitioner_agent is None:
            self.Patient = Patient
            self.Encounter = generateencounter.GenerateEncounter(Patient=self.Patient).Encounter
            self.Practitioner_agent = self.Encounter.Practitioner
        elif Patient is None and Encounter is not None and Practitioner_agent is None:
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner_agent = self.Encounter.Practitioner
        elif Patient is None and Encounter is None and Practitioner_agent is not None:
            self.Practitioner_agent = Practitioner_agent
            self.Encounter = generateencounter.GenerateEncounter(Practitioner=self.Practitioner_agent).Encounter
            self.Patient = self.Encounter.Patient
        elif Patient is None and Encounter is not None and Practitioner_agent is not None:
            if Encounter.Practitioner.id != Practitioner_agent.id:
                raise ValueError('Encounter.Practitioner.id must equal Practitioner.id')
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner_agent = Practitioner_agent
        elif Patient is None and Encounter is None and Practitioner_agent is None:
            self.Encounter = generateencounter.GenerateEncounter().Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner_agent = self.Encounter.Practitioner
        else:
            raise ValueError('Error with Patient, Encounter, and Practitioner values.')

        if Practitioner_recipient == None:
            self.Practitioner_recipient = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner_recipient = Practitioner_recipient

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

        # self._validate(ReferralRequest)
        self.response = ReferralRequest.create(server=self.connect2server().server)
        ReferralRequest.id = self._extract_id()
        self.ReferralRequest = ReferralRequest
        self.ReferralRequest.Patient = self.Patient
        self.ReferralRequest.Practitioner_agent = self.Practitioner_agent
        self.ReferralRequest.Practitioner_recipient = self.Practitioner_recipient
        self.ReferralRequest.Encounter = self.Encounter


if __name__ == '__main__':
    GenerateReferralRequest()