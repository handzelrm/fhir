from generateobservation import GenerateObservation
from generateobservationdict import GenerateObservationDict
from generatefparlabs import GenerateFparLabs
from generatetask import GenerateTask

def main():
    obs_dict = GenerateObservationDict()
    print(obs_dict.Patient)
    print(obs_dict.Patient.id)
    obs_vitals = GenerateObservation(obs_dict.observation_dict,Patient=obs_dict.Patient)
    print(obs_vitals.Patient)
    print(obs_vitals.Patient.id)
    print(obs_vitals.Practitioner)
    print(obs_vitals.Practitioner.id)

    #cannot run while v5 server is down
    # labs = GenerateFparLabs()
    # obs_labs = GenerateObservation(labs.lab_dict,Patient=obs_vitals.Patient,Practitioner=obs_vitals.Practitioner,Encounter=obs_vitals.Encounter)

    task = GenerateTask(Patient=obs_vitals.Patient,Practitioner_agent=obs_vitals.Practitioner, Encounter=obs_vitals.Encounter)
    task.complete_task()

if __name__ == '__main__':
    main()