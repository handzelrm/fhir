import generatebase
import labvaluesets

import pandas as pd
import numpy as np
import random
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class GenerateFparLabs(generatebase.GenerateBase):

    def __init__(self):
        self.hiv = labvaluesets.LabValueSets('ValueSet','FPARHIVTests')
        self.ct_gc = labvaluesets.LabValueSets('ValueSet','FPARchlamydiaTrachomatisAndNeisseriaGonorrhoeaeCombinedTests')
        self.ct = labvaluesets.LabValueSets('ValueSet','FPARchlamydiaTrachomatisTests')
        self.gc = labvaluesets.LabValueSets('ValueSet','FPARneisseriaGonorrhoeaeTests')
        self.hpv = labvaluesets.LabValueSets('ValueSet','FPARhumanPapillomaVirusTests')
        self.pap = labvaluesets.LabValueSets('ValueSet','FPARpapSmearTests')
        self.preg = labvaluesets.LabValueSets('ValueSet','FPARpregnancyTests')

        self._generate_lab_df()

        self.lab_dict = {}
        self.lab_dict['hiv'] = self._generate_lab_dict(self.hiv)
        separate_or_combined = random.choice(['separate','combined'])

        if separate_or_combined == 'separate':
            self.lab_dict['ct'] = self._generate_lab_dict(self.ct)
            self.lab_dict['gc'] = self._generate_lab_dict(self.gc)
        elif separate_or_combined == 'combined':
            self.lab_dict['ct_gc'] = self._generate_lab_dict(self.ct_gc)
        else:
            raise ValueError('Issue with code')
        self.lab_dict['hpv'] = self._generate_lab_dict(self.hpv)
        self.lab_dict['pap'] = self._generate_lab_dict(self.pap)
        self.lab_dict['preg'] = self._generate_lab_dict(self.preg)

    def _generate_lab_df(self):
        """Generates a pandas dataframe of labs based on excel file."""
        lab_list = []
        loinc_list = []
        value_list = []
        df = pd.read_excel('../demographic_files/labs.xlsx')
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

    def _generate_lab_dict(self,lab):
        lab_loinc = random.choice(lab.LoincSet)
        lab_value_list = self.lab_df[self.lab_df.loinc==lab_loinc].value.values
        lab_name_list = self.lab_df[self.lab_df.loinc==lab_loinc].lab_name.values
        if len(lab_value_list)==0:
            lab_loinc, lab_value, lab_name = self._check_for_missing_labs(lab)
        else:
            lab_value = random.choice(lab_value_list)
            lab_name = random.choice(lab_name_list)

        lab_dict = {'type':'valuestring','loinc':lab_loinc,'display':lab_name,'unit':None,'value':lab_value}
        return lab_dict


if __name__ == '__main__':
    GenerateFparLabs()
