import generatebase
import fhirclient.models.organization as org
import fhirclient.models.address as a
import fhirclient.models.contactpoint as cp
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class GenerateOrganization(generatebase.GenerateBase):

    organization_name = 'UPMC Magee Clinic'
    organization_phone = '(123) 456-7890'
    organization_line = ["Magee-Women's Hospital of UPMC, Halket Street"]
    organization_city = 'Pittsburgh'
    organization_postalCode = '15213'
    organization_state = 'PA'
    # organization_longitude = -79.960779
    # organization_latitude = 40.437123

    def __init__(self):
        Organization = org.Organization()
        Organization.active = True
        Organization.name = self.organization_name
        Address = a.Address()
        Address.line = self.organization_line
        Address.city = self.organization_city
        Address.postalCode = self.organization_postalCode
        Address.state = self.organization_state
        Organization.address = [Address]
        ContactPoint = cp.ContactPoint()
        ContactPoint.system = 'phone'
        ContactPoint.value = self.organization_phone
        Organization.telecom = [ContactPoint]
        self._validate(Organization)
        self.response = Organization.create(self.connect2server().server)
        Organization.id = self._extract_id()
        self.Organization = Organization
        print(f'{Organization.__class__.__name__}:{self.organization_name}; id: {Organization.id}')

if __name__ == '__main__':
    GenerateOrganization()
