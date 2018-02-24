import generatebase

import fhirclient.models.address as a
import fhirclient.models.location as l
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class GenerateLocation(generatebase.GenerateBase):

    location_status = 'active'
    location_name = 'UPMC Magee Clinic'
    location_line = ["Magee-Women's Hospital of UPMC, Halket Street"]
    location_city = 'Pittsburgh'
    location_postalCode = '15213'
    location_state = 'PA'
    location_longitude = -79.960779
    location_latitude = 40.437123
    

    def __init__(self):
        """
        Uses fhirclient.models to create and post location resource. Currently, using class variables.

        :param smart: fhirclient.client.FHIRClient object.
        :returns: practitioner id created by server
        """
        Location = l.Location()
        LocationPosition = l.LocationPosition()
        Address = a.Address()
        Location.status = 'active'
        Location.name = self.location_name
        Address.line = self.location_line
        Address.city = self.location_city
        Address.postalCode = self.location_postalCode
        Address.state = self.location_state
        Location.address = Address
        LocationPosition.latitude = self.location_latitude
        LocationPosition.longitude = self.location_longitude
        Location.position = LocationPosition
        self._validate(Location)
        self.response = Location.create(server=self.connect2server().server)
        Location.id = self._extract_id()
        self.Location = Location


if __name__ == '__main__':
    GenerateLocation()
