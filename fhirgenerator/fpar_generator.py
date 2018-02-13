from generateobservation import GenerateObservation
from generateobservationdict import GenerateObservationDict
from generatefparlabs import GenerateFparLabs
from generatetask import GenerateTask
import pandas as pd
import os
import time

def main():
    t0 = time.time()
    obs_dict = GenerateObservationDict()
    obs_vitals = GenerateObservation(obs_dict.observation_dict,Patient=obs_dict.Patient)

    #cannot run while v5 server is down
    labs = GenerateFparLabs()
    obs_labs = GenerateObservation(labs.lab_dict,Patient=obs_vitals.Patient,Practitioner=obs_vitals.Practitioner,Encounter=obs_vitals.Encounter)

    task = GenerateTask(Patient=obs_vitals.Patient,Practitioner_agent=obs_vitals.Practitioner, Encounter=obs_vitals.Encounter)
    task.complete_task()
    

    # if os.path.exists('./patient_list.xlsx'):
    #     df = pd.read_excel('./patient_list')
    # else:
    #     df = pd.DataFrame(columns=['name','id'])
    
    # with open('./patient_list','a') as f:
    #     f.write(f'{task.Patient.id}')
    name = f'{task.Patient.name[0].family},{task.Patient.name[0].given[0]}'
    pt_id = f'{task.Patient.id}'

    t1 = time.time()
    print(f'{t1-t0:.2f} seconds')

    return name, pt_id

if __name__ == '__main__':
    name_list = []
    id_list = []
    for i in range(100):
        name, pt_id = main()
        name_list.append(name)
        id_list.append(pt_id)
    pd.DataFrame({'name':name_list,'id':id_list}).to_excel('../fpar/patient_list.xlsx',index=False)
