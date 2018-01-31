import generatebase
import labvaluesets


class GenerateFparLabs(generatebase.GenerateBase):

    def __init__(self):
        self.hiv = labvaluesets.LabValueSets('ValueSet','FPARHIVTests')
        self.ct_gc = labvaluesets.LabValueSets('ValueSet','FPARchlamydiaTrachomatisAndNeisseriaGonorrhoeaeCombinedTests')
        self.ct = labvaluesets.LabValueSets('ValueSet','FPARchlamydiaTrachomatisTests')
        self.gc = labvaluesets.LabValueSets('ValueSet','FPARneisseriaGonorrhoeaeTests')
        self.hpv = labvaluesets.LabValueSets('ValueSet','FPARhumanPapillomaVirusTests')
        self.pap = labvaluesets.LabValueSets('ValueSet','FPARpapSmearTests')
        self.preg = labvaluesets.LabValueSets('ValueSet','FPARpregnancyTests')
        self.income = labvaluesets.LabValueSets('ValueSet','FPARannualHouseholdIncomeRanges') 

        print(self.hiv.valueset)
        print(self.hiv.LoincSet)


        # self._create_labs(self.hiv)
        # separate_or_combined = random.choice(['separate','combined'])
        # if separate_or_combined == 'separate':
        #     self._create_labs(self.ct)
        #     self._create_labs(self.gc)
        # elif separate_or_combined == 'combined':
        #     self._create_labs(self.ct_gc)
        # else:
        #     raise ValueError('Issue with code')
        # self._create_labs(self.hpv)
        # self._create_labs(self.pap)
        # self._create_labs(self.preg)


if __name__ == '__main__':
    GenerateFparLabs()