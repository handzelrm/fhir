from generateobservation import GenerateObservation
from generateobservationdict import GenerateObservationDict
from generatefparlabs import GenerateFparLabs
from generatetask import GenerateTask
import pandas as pd
import os
import time
import argparse


def generate_fpar_resources(timeit):
    t0 = time.time()
    obs_dict = GenerateObservationDict()
    obs_vitals = GenerateObservation(obs_dict.observation_dict,Patient=obs_dict.Patient)

    #cannot run while v5 server is down
    labs = GenerateFparLabs()
    obs_labs = GenerateObservation(labs.lab_dict,Patient=obs_vitals.Patient,Practitioner=obs_vitals.Practitioner,Encounter=obs_vitals.Encounter)

    task = GenerateTask(Patient=obs_vitals.Patient,Practitioner_agent=obs_vitals.Practitioner, Encounter=obs_vitals.Encounter)
    task.complete_task()
    
    name = f'{task.Patient.name[0].family},{task.Patient.name[0].given[0]}'
    pt_id = f'{task.Patient.id}'

    t1 = time.time()

    if time:
        print(f'{t1-t0:.2f} seconds')

    return name, pt_id

def loop_generator(num,output,timeit):
    name_list = []
    id_list = []
    for i in range(num):
        name, pt_id = generate_fpar_resources(timeit)
        name_list.append(name)
        id_list.append(pt_id)
    if output:
        pd.DataFrame({'name':name_list,'id':id_list}).to_excel('../fpar/patient_list.xlsx',index=False)
    

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('num', help="Number of fpar patients to create.", type=int)
    parser.add_argument('-o','--output', help='Output the result to an excel file', action='store_true')
    parser.add_argument('-t', '--timeit', help='Print the time it takes to run each patient.', action='store_true')
    args = parser.parse_args()

    loop_generator(args.num, args.output, args.timeit)

if __name__ == '__main__':
    main()
    
