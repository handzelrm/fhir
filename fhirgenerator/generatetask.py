import generatebase
import generatepatient
import generatepractitioner
import generateencounter
import generatereferralrequest

import fhirclient.models.task as t

import datetime

class GenerateTask(generatebase.GenerateBase):

    def __init__(self, Patient=None, Practitioner_agent=None, Practitioner_recipient=None, Encounter=None, ReferralRequest=None,):

        if Patient is not None and Encounter is not None and ReferralRequest is not None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            if Encounter.Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Encounter.Patient.id must equal ReferralRequest.Patient.id')
            if Encounter.id != ReferralRequest.Encounter.id:
                raise ValueError('Encounter.id must equal ReferralRequest.Encounter.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest
        elif Patient is not None and Encounter is None and ReferralRequest is None:
            self.Patient = Patient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient).ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
        elif Patient is not None and Encounter is not None and ReferralRequest is None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest(Patient=self.Patient,Encounter=self.Encounter).ReferralRequest
        elif Patient is not None and Encounter is None and ReferralRequest is not None:
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            self.Patient = Patient
            self.ReferralRequest = ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
        elif Patient is None and Encounter is not None and ReferralRequest is None:
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.ReferralRequest = ReferralRequest(Patient=self.Patient,Encounter=self.Encounter).ReferralRequest
        elif Patient is None and Encounter is None and ReferralRequest is not None:
            self.ReferralRequest = ReferralRequest
            self.Patient = self.ReferralRequest.Patient
            self.Encounter = self.ReferralRequest.Encounter
        elif Patient is None and Encounter is None and ReferralRequest is None:
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest().ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Patient = self.ReferralRequest.Patient
        else:
            raise ValueError('Error with Patient, Encounter, and ReferralRequest values')

        if Practitioner_agent == None:
            self.Practitioner_agent = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner_agent = Practitioner_agent

        if Practitioner_recipient == None:
            self.Practitioner_recipient = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner_recipient = Practitioner_recipient

        Task = t.Task()
        Task.status = 'requested'
        Task.intent = 'order'

        Task.executionPeriod = self._create_FHIRPeriod(start=datetime.datetime.now())

        TaskRequester = t.TaskRequester()
        TaskRequester.agent = self._create_FHIRReference(self.Practitioner_agent)
        Task.requester = TaskRequester

        Task_Restriction = t.TaskRestriction()
        Task_Restriction.recipient = [self._create_FHIRReference(self.Practitioner_recipient)]
        Task.restriction = Task_Restriction

        Task.for_fhir = self._create_FHIRReference(self.Patient)
        Task.context = self._create_FHIRReference(self.Encounter)

        Task.basedOn = [self._create_FHIRReference(self.ReferralRequest)]
        
#         self._validate(Task)
        self.response = Task.create(self.connect2server().server)
        Task.id = self._extract_id()
        self.Task = Task
        self.Task.Patient = self.Patient
        self.Task.Practitioner_agent = self.Practitioner_agent
        self.Task.Practitioner_recipient = self.Practitioner_recipient
        self.Task.Encounter = self.Encounter
        self.Task.ReferralRequest = self.ReferralRequest


if __name__ == '__main__':
    GenerateTask()