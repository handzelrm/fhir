import generatebase
import generatepatient
import generatepractitioner
import generateencounter
import generatereferralrequest

import fhirclient.models.task as t

import datetime

class GenerateTask(generatebase.GenerateBase):

    def __init__(self, Patient=None, Practitioner_agent=None, Practitioner_recipient=None, Encounter=None, ReferralRequest=None,):

        if Patient is not None and Encounter is not None and ReferralRequest is not None and Practitioner_agent is not None and Practitioner_recipient is not None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            if Encounter.Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Encounter.Patient.id must equal ReferralRequest.Patient.id')
            if Encounter.id != ReferralRequest.Encounter.id:
                raise ValueError('Encounter.id must equal ReferralRequest.Encounter.id')
            if Practitioner_agent != ReferralRequest.Practitioner_agent:
                raise ValueError('Practitioner_agent must equal ReferralRequest.Practitioner_agent')
            if Practitioner_recipient != ReferralRequest.Practitioner_recipient:
                raise ValueError('Practitioner_recipient must equal ReferralRequest.Practitioner_recipient')
            self.Patient = Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient
        elif Patient is not None and Encounter is not None and ReferralRequest is not None and Practitioner_agent is not None and Practitioner_recipient is None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            if Encounter.Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Encounter.Patient.id must equal ReferralRequest.Patient.id')
            if Encounter.id != ReferralRequest.Encounter.id:
                raise ValueError('Encounter.id must equal ReferralRequest.Encounter.id')
            if Practitioner_agent != ReferralRequest.Practitioner_agent:
                raise ValueError('Practitioner_agent must equal ReferralRequest.Practitioner_agent')
            self.Patient = Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is not None and Encounter is not None and ReferralRequest is not None and Practitioner_agent is None and Practitioner_recipient is not None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            if Encounter.Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Encounter.Patient.id must equal ReferralRequest.Patient.id')
            if Encounter.id != ReferralRequest.Encounter.id:
                raise ValueError('Encounter.id must equal ReferralRequest.Encounter.id')
            if Practitioner_recipient != ReferralRequest.Practitioner_recipient:
                raise ValueError('Practitioner_recipient must equal ReferralRequest.Practitioner_recipient')
            self.Patient = Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest
            self.Practitioner_agent = self.ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient
        elif Patient is not None and Encounter is not None and ReferralRequest is not None and Practitioner_agent is None and Practitioner_recipient is None:
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
            self.Practitioner_agent = self.ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient

        elif Patient is not None and Encounter is None and ReferralRequest is None and Practitioner_agent is None and Practitioner_recipient is None:
            self.Patient = Patient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient).ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_agent = ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = ReferralRequest.Practitioner_recipient
        elif Patient is not None and Encounter is None and ReferralRequest is None and Practitioner_agent is not None and Practitioner_recipient is None:
            self.Patient = Patient
            self.Practitioner_agent = Practitioner_agent
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Practitioner_agent=self.Practitioner_agent).ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_recipient = ReferralRequest.Practitioner_recipient
        elif Patient is not None and Encounter is None and ReferralRequest is None and Practitioner_agent is None and Practitioner_recipient is not None:
            self.Patient = Patient
            self.Practitioner_recipient = Practitioner_recipient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Practitioner_recipient=self.Practitioner_recipient).ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_agent = self.ReferralRequest.Practitioner_agent
        elif Patient is not None and Encounter is None and ReferralRequest is None and Practitioner_agent is not None and Practitioner_recipient is not None:
            self.Patient = Patient
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Practitioner_agent=self.Practitioner_agent,Practitioner_recipient=self.Practitioner_recipient).ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter

        elif Patient is not None and Encounter is not None and ReferralRequest is None and Practitioner_agent is None and Practitioner_recipient is None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.Practitioner_agent = self.Encounter.Practitioner
            self.Practitioner_recipient = Practitioner_recipient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Encounter=self.Encounter,Practitioner_agent=self.Practitioner_agent,Practitioner_recipient=self.Practitioner_recipient).ReferralRequest
        elif Patient is not None and Encounter is not None and ReferralRequest is None and Practitioner_agent is not None and Practitioner_recipient is None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            if Practitioner_agent.id != Encounter.Practitioner.id:
                raise ValueError('Practitioner_agent.id must equal Encounter.Practioner.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.Practitioner_agent = Practitioner_agent
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Encounter=self.Encounter,Practitioner_agent=self.Practitioner_agent).ReferralRequest
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is not None and Encounter is not None and ReferralRequest is None and Practitioner_agent is None and Practitioner_recipient is not None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.Practitioner_agent = self.Encounter.Practitioner
            self.Practitioner_recipient = Practitioner_recipient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Encounter=self.Encounter,Practitioner_agent=self.Practitioner_agent,Practitioner_recipient=self.Practitioner_recipient).ReferralRequest
        elif Patient is not None and Encounter is not None and ReferralRequest is None and Practitioner_agent is not None and Practitioner_recipient is not None:
            if Patient.id != Encounter.Patient.id:
                raise ValueError('Patient.id must equal Encounter.Patient.id')
            if Practitioner_agent.id != Encounter.Practitioner.id:
                raise ValueError('Practitioner_agent.id must equal Encounter.Practioner.id')
            self.Patient = Patient
            self.Encounter = Encounter
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Encounter=self.Encounter,Practitioner_agent=self.Practitioner_agent).ReferralRequest

        elif Patient is not None and Encounter is None and ReferralRequest is not None and Practitioner_agent is None and Practitioner_recipient is None:
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            self.Patient = Patient
            self.ReferralRequest = ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_agent = self.ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is not None and Encounter is None and ReferralRequest is not None and Practitioner_agent is not None and Practitioner_recipient is None:
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            if ReferralRequest.Practitioner_agent.id != Practitioner_agent.id:
                raise ValueErrror('ReferralRequest.Practitioner_agent.id must equal Practitioner_agent.id')
            self.Patient = Patient
            self.Practitioner_agent = Practitioner_agent
            self.ReferralRequest = ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is not None and Encounter is None and ReferralRequest is not None and Practitioner_agent is None and Practitioner_recipient is not None:
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            if ReferralRequest.Practitioner_recipient.id != Practitioner_recipient.id:
                raise ValueErrror('ReferralRequest.Practitioner_recipient.id must equal Practitioner_recipient.id')
            self.Patient = Patient
            self.Practitioner_recipient = Practitioner_recipient
            self.ReferralRequest = ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_agent = self.ReferralRequest.Practitioner_agent
        elif Patient is not None and Encounter is None and ReferralRequest is not None and Practitioner_agent is not None and Practitioner_recipient is not None:
            if Patient.id != ReferralRequest.Patient.id:
                raise ValueError('Patient.id must equal ReferralRequest.Patient.id')
            if ReferralRequest.Practitioner_agent.id != Practitioner_agent.id:
                raise ValueErrror('ReferralRequest.Practitioner_agent.id must equal Practitioner_agent.id')
            if ReferralRequest.Practitioner_recipient.id != Practitioner_recipient.id:
                raise ValueErrror('ReferralRequest.Practitioner_recipient.id must equal Practitioner_recipient.id')
            self.Patient = Patient
            self.Practitioner_agent = Practitioner_agent
            self.ReferralRequest = ReferralRequest
            self.ReferralRequest = ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter

        elif Patient is None and Encounter is not None and ReferralRequest is None and Practitioner_agent is None and Practitioner_recipient is None:
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner_agent = self.Encounter.Practioner
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Encounter=self.Encounter,Practitioner_agent=self.Practitioner_agent).ReferralRequest
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is not None and ReferralRequest is None and Practitioner_agent is not None and Practitioner_recipient is None:
            if Practitioner_agent.id != Encounter.Practitioner.id:
                raise ValueError('Practitioner_agent.id must equal Encounter.Practioner.id')
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner_agent = self.Practitioner_agent
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Encounter=self.Encounter,Practitioner_agent=self.Practitioner_agent).ReferralRequest
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is not None and ReferralRequest is None and Practitioner_agent is None and Practitioner_recipient is not None:
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner_agent = self.Encounter.Practioner
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Encounter=self.Encounter,Practitioner_agent=self.Practitioner_agent).ReferralRequest
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is not None and ReferralRequest is None and Practitioner_agent is not None and Practitioner_recipient is not None:
            if Practitioner_agent.id != Encounter.Practitioner.id:
                raise ValueError('Practitioner_agent.id must equal Encounter.Practioner.id')
            self.Encounter = Encounter
            self.Patient = self.Encounter.Patient
            self.Practitioner_agent = Practitioner_agent
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Patient=self.Patient,Encounter=self.Encounter,Practitioner_agent=self.Practitioner_agent).ReferralRequest
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient

        elif Patient is None and Encounter is None and ReferralRequest is not None and Practitioner_agent is None and Practitioner_recipient is None:
            self.ReferralRequest = ReferralRequest
            self.Patient = self.ReferralRequest.Patient
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_agent = ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is None and ReferralRequest is not None and Practitioner_agent is not None and Practitioner_recipient is None:
            if ReferralRequest.Practitioner_agent.id != Practitioner_agent.id:
                raise ValueErrror('ReferralRequest.Practitioner_agent.id must equal Practitioner_agent.id')
            self.ReferralRequest = ReferralRequest
            self.Patient = self.ReferralRequest.Patient
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is None and ReferralRequest is not None and Practitioner_agent is None and Practitioner_recipient is not None:
            if ReferralRequest.Practitioner_recipient.id != Practitioner_recipient.id:
                raise ValueErrror('ReferralRequest.Practitioner_recipient.id must equal Practitioner_recipient.id')
            self.ReferralRequest = ReferralRequest
            self.Patient = self.ReferralRequest.Patient
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_agent = ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient
        elif Patient is None and Encounter is None and ReferralRequest is not None and Practitioner_agent is not None and Practitioner_recipient is not None:
            if ReferralRequest.Practitioner_agent.id != Practitioner_agent.id:
                raise ValueErrror('ReferralRequest.Practitioner_agent.id must equal Practitioner_agent.id')
            if ReferralRequest.Practitioner_recipient.id != Practitioner_recipient.id:
                raise ValueErrror('ReferralRequest.Practitioner_recipient.id must equal Practitioner_recipient.id')
            self.ReferralRequest = ReferralRequest
            self.Patient = self.ReferralRequest.Patient
            self.Encounter = self.ReferralRequest.Encounter
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient

        elif Patient is None and Encounter is not None and ReferralRequest is not None and Practitioner_agent is None and Practitioner_recipient is None:
            if Encounter.id != ReferralRequest.Encounter.id:
                raise ValueError('Encounter.id must equal ReferralRequest.Encounter.id')
            if Encounter.Practitioner.id != ReferralRequest.Practitioner_agent.id:
                raise ValueError('Encounter.Practioner.id must equal ReferralRequest.Practitioner_agent.id')
            self.Patient = Encounter.Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest
            self.Practitioner_agent = ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is not None and ReferralRequest is not None and Practitioner_agent is not None and Practitioner_recipient is None:
            if Encounter.id != ReferralRequest.Encounter.id:
                raise ValueError('Encounter.id must equal ReferralRequest.Encounter.id')
            if Encounter.Practitioner.id != ReferralRequest.Practitioner_agent.id:
                raise ValueError('Encounter.Practioner.id must equal ReferralRequest.Practitioner_agent.id')
            if Practitioner_agent.id != ReferralRequest.Practitioner_agent.id:
                raise ValueError('Practitioner_agent.id must equal ReferralRequest.Practitioner_agent.id')
            self.Patient = Encounter.Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is not None and ReferralRequest is not None and Practitioner_agent is None and Practitioner_recipient is not None:
            if Encounter.id != ReferralRequest.Encounter.id:
                raise ValueError('Encounter.id must equal ReferralRequest.Encounter.id')
            if Encounter.Practitioner.id != ReferralRequest.Practitioner_agent.id:
                raise ValueError('Encounter.Practioner.id must equal ReferralRequest.Practitioner_agent.id')
            if Practitioner_recipient.id != ReferralRequest.Practitioner_recipient.id:
                raise ValueError('Practitioner_recipient.id must equal ReferralRequest.Practitioner_recipient.id')
            self.Patient = Encounter.Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest
            self.Practitioner_agent = ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient
        elif Patient is None and Encounter is not None and ReferralRequest is not None and Practitioner_agent is not None and Practitioner_recipient is not None:
            if Encounter.id != ReferralRequest.Encounter.id:
                raise ValueError('Encounter.id must equal ReferralRequest.Encounter.id')
            if Encounter.Practitioner.id != ReferralRequest.Practitioner_agent.id:
                raise ValueError('Encounter.Practioner.id must equal ReferralRequest.Practitioner_agent.id')
            if Practitioner_agent.id != ReferralRequest.Practitioner_agent.id:
                raise ValueError('Practitioner_agent.id must equal ReferralRequest.Practitioner_agent.id')
            if Practitioner_recipient.id != ReferralRequest.Practitioner_recipient.id:
                raise ValueError('Practitioner_recipient.id must equal ReferralRequest.Practitioner_recipient.id')
            self.Patient = Encounter.Patient
            self.Encounter = Encounter
            self.ReferralRequest = ReferralRequest
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient

        elif Patient is None and Encounter is None and ReferralRequest is None and Practitioner_agent is None and Practitioner_recipient is None:
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest().ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Patient = self.ReferralRequest.Patient
            self.Practitioner_agent = self.ReferralRequest.Practitioner_agent
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is None and ReferralRequest is None and Practitioner_agent is not None and Practitioner_recipient is None:
            self.Practitioner_agent = Practitioner_agent
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Practitioner_agent=self.Practitioner_agent).ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Patient = self.ReferralRequest.Patient
            self.Practitioner_recipient = self.ReferralRequest.Practitioner_recipient
        elif Patient is None and Encounter is None and ReferralRequest is None and Practitioner_agent is None and Practitioner_recipient is not None:
            self.Practitioner_recipient = Practitioner_recipient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Practitioner_recipient=self.Practitioner_recipient).ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Patient = self.ReferralRequest.Patient
            self.Practitioner_agent = self.ReferralRequest.Practitioner_agent
        elif Patient is None and Encounter is None and ReferralRequest is None and Practitioner_agent is not None and Practitioner_recipient is not None:
            self.Practitioner_agent = Practitioner_agent
            self.Practitioner_recipient = Practitioner_recipient
            self.ReferralRequest = generatereferralrequest.GenerateReferralRequest(Practitioner_agent=self.Practitioner_agent,Practitioner_recipient=self.Practitioner_recipient).ReferralRequest
            self.Encounter = self.ReferralRequest.Encounter
            self.Patient = self.ReferralRequest.Patient

        else:
            raise ValueError('Error with Patient, Encounter, and ReferralRequest values')

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

    def complete_task(self):
        self.Task.status = 'completed'
        if self.Task.ReferralRequest.Encounter.class_fhir == 'outpatient':
            Encounter = generateencounter.GenerateEncounter()
            self.Task.focus = self._create_FHIRReference(Encounter)
        elif self.Task.ReferralRequest.Encounter.class_fhir == 'inptiaent':
            self.Task.focus = self._create_FHIRReference(self.Encounter)
        self.Task.executionPeriod = self._create_FHIRPeriod(end=datetime.datetime.now())
        print(self.Task.as_json())
        self.Task.update(server=self.connect2server().server)


if __name__ == '__main__':
    task = GenerateTask()
    task.complete_task()