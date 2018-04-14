import requests
import argparse

class RxnormClassMeds():
    def __init__(self, classid):
        self.classid = classid
        r = requests.get(f'https://rxnav.nlm.nih.gov/REST/rxclass/classMembers.json?classId={classid}&relaSource=ATC')
        drugs = r.json()['drugMemberGroup']['drugMember']

        self.drug_dict = {}
        for drug in drugs:
            drug_name = drug['minConcept']['name']
            drug_id = drug['minConcept']['rxcui']
            r = requests.get(f'https://rxnav.nlm.nih.gov/REST/rxcui/{drug_id}/related.json?tty=DFG')
            try:
                drug_doseform = r.json()['relatedGroup']['conceptGroup'][0]['conceptProperties']
                has_doseform = True
            except KeyError:
                has_doseform = False
            if has_doseform:
                drug_doseform_list = []
                for doseform in drug_doseform:
                    drug_doseform_list.append({'doseform_name':doseform['name'], 'doseform_code':doseform['umlscui']})
                self.drug_dict[f'{drug_name}'] = {'drug_id':drug_id, 'drug_doseforms':drug_doseform_list}
        # print(self.drug_dict)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--classid', help='Class id for rxnorm.', type=str)
    args = parser.parse_args()
    if args.classid is None:
        RxnormClassMeds(classid='A10AE')
    else:
        RxnormClassMeds(classid=args.classid)

if __name__ == '__main__':
    main()
