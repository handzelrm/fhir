import generatebase
import generatepatient
import generatepractitioner
import generateencounter
import generatereferralrequest

import fhirclient.models.task as t

import datetime

class GenerateTask(generatebase.GenerateBase):

    def __init__(self, Patient=None, Practitioner_agent=None, Practitioner_recipient=None, Encounter=None, ReferralRequest=None,):

        if Patient == None:
            self.Patient = generatepatient.GeneratePatient().Patient
        else:
            self.Patient = Patient

        if Practitioner_agent == None:
            self.Practitioner_agent = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner_agent = Practitioner_agent

        if Practitioner_recipient == None:
            self.Practitioner_recipient = generatepractitioner.GeneratePractitioner().Practitioner
        else:
            self.Practitioner_recipient = Practitioner_recipient

        if Encounter == None:
            self.Encounter = generateencounter.GenerateEncounter(Patient=self.Patient, Location=None, Condition=None).Encounter
        else:
            self.Encounter = Encounter

        if ReferralRequest == None:
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient, Practitioner_agent=self.Practitioner_agent, Practitioner_recipient=self.Practitioner_recipient, Encounter = self.Encounter).ReferralRequest
        else:
            self.ReferralRequest = ReferralRequest

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

if __name__ == '__main__':
    GenerateTask()