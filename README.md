# fhir

## fhirgenerator
- the file generatebase contains class GenerateBase which is the base class for all of the other generate classes
- Other generate files create at least one FHIR resource. For instance, generatepatient.py contains class GeneratePatient which will create a Patient FHIR resource
- Each file if executed will call the class within the file at least once. Full testing has not yet been developed
- Each of the generate classes has logic to check for conflicting references. For example, generateobservation.GenerateObservation includes both Patient and Encounter. Encounter will have a reference to a Patient and a ValueError will be raised if Patient.id != Encounter.Patient.id

## demographics_files
A series of files used for creating a patient, labs, and condition