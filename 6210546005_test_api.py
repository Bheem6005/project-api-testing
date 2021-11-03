import unittest
import requests

URL = "https://wcg-apis.herokuapp.com"


def create_reserve_params(citizen_id, site_name, vaccine_name):
    return f"/reservation?citizen_id={citizen_id}&site_name={site_name}&vaccine_name={vaccine_name}"


class ReservationApiTestCase(unittest.TestCase):
    """Unit test for the Reservation API of World Class Government APIs."""

    def setUp(self):
        requests.post(URL + f"/registration?citizen_id=4444444444444&name=Tetra&surname=Quad"
                            f"&birth_date=04/04/2001&occupation=human&address=home")

    def test_get_reservation_information(self):
        response = requests.get(URL + f"/reservation")
        self.assertEqual(200, response.status_code)

    def test_reserve_successfully(self):
        response = requests.post(URL + create_reserve_params("4444444444444", "OGYH Site", "Astra"))
        self.assertEqual("reservation success!", response.json()["feedback"])

    def test_reserve_citizen_id_less_than_13(self):
        response = requests.post(URL + create_reserve_params("444444444444", "OGYH Site", "Astra"))
        self.assertEqual("reservation failed: invalid citizen ID", response.json()["feedback"])

    def test_reserve_citizen_id_more_than_13(self):
        response = requests.post(URL + create_reserve_params("44444444444444", "OGYH Site", "Astra"))
        self.assertEqual("reservation failed: invalid citizen ID", response.json()["feedback"])

    def test_reserve_alphabet_citizen_id(self):
        response = requests.post(URL + create_reserve_params("fourinthirtee", "OGYH Site", "Astra"))
        self.assertEqual("reservation failed: invalid citizen ID", response.json()["feedback"])

    def test_reserve_symbol_citizen_id(self):
        response = requests.post(URL + create_reserve_params("@@@@@@@@@@@@@", "OGYH Site", "Astra"))
        self.assertEqual("reservation failed: invalid citizen ID", response.json()["feedback"])

    def test_reserve_non_registered_citizen_id(self):
        response = requests.post(URL + create_reserve_params("1234567894444", "OGYH Site", "Astra"))
        self.assertEqual("reservation failed: citizen ID is not registered", response.json()["feedback"])

    def test_reserve_blank_citizen_id(self):
        response = requests.post(URL + create_reserve_params("", "OGYH Site", "Astra"))
        self.assertEqual("reservation failed: missing some attribute", response.json()["feedback"])

    def test_reserve_blank_site_name(self):
        response = requests.post(URL + create_reserve_params("4444444444444", "", "Astra"))
        self.assertEqual("reservation failed: missing some attribute", response.json()["feedback"])

    def test_reserve_non_exist_vaccine_name(self):
        # When I create this test the feedback said "report failed: invalid vaccine name"
        # but I think it should be "reservation failed: invalid vaccine name"
        response = requests.post(URL + create_reserve_params("4444444444444", "OGYH Site", "SINoALICE"))
        self.assertEqual("reservation failed: invalid vaccine name", response.json()["feedback"])

    def test_reserve_blank_vaccine_name(self):
        response = requests.post(URL + create_reserve_params("4444444444444", "OGYH Site", ""))
        self.assertEqual("reservation failed: missing some attribute", response.json()["feedback"])

    def test_reserve_twice(self):
        requests.post(URL + create_reserve_params("4444444444444", "OGYH Site", "Astra"))
        response = requests.post(URL + create_reserve_params("4444444444444", "OGYH Site", "Astra"))
        self.assertEqual("reservation failed: there is already a reservation for this citizen",
                         response.json()["feedback"])

    def test_delete_reservation_successfully(self):
        requests.post(URL + create_reserve_params("4444444444444", "OGYH Site", "Astra"))

        response = requests.delete(URL + f'/reservation?citizen_id=4444444444444')
        self.assertEqual("cancel reservation successfully", response.json()["feedback"])

    def test_delete_non_existed_reservation(self):
        response = requests.delete(URL + f'/reservation?citizen_id=4444444444444')
        self.assertEqual("cancel reservation failed: there is no reservation for this citizen",
                         response.json()["feedback"])

    def test_delete_reservation_citizen_id_less_than_13(self):
        response = requests.delete(URL + f'/reservation?citizen_id=444444444444')
        self.assertEqual("cancel reservation failed: invalid citizen ID", response.json()["feedback"])

    def test_delete_reservation_citizen_id_more_than_13(self):
        response = requests.delete(URL + f'/reservation?citizen_id=44444444444444')
        self.assertEqual("cancel reservation failed: invalid citizen ID", response.json()["feedback"])

    def test_delete_reservation_alphabet_citizen_id(self):
        response = requests.delete(URL + f'/reservation?citizen_id=fourinthirtee')
        self.assertEqual("cancel reservation failed: invalid citizen ID", response.json()["feedback"])

    def test_delete_reservation_symbol_citizen_id(self):
        response = requests.delete(URL + f'/reservation?citizen_id=@@@@@@@@@@@@@')
        self.assertEqual("cancel reservation failed: invalid citizen ID", response.json()["feedback"])

    def test_delete_reservation_non_registered_citizen_id(self):
        # When I create this test the feedback said "reservation failed: citizen ID is not registered"
        # but I think it should be "cancel reservation failed: citizen ID is not registered"
        response = requests.delete(URL + f'/reservation?citizen_id=1234567894444')
        self.assertEqual("cancel reservation failed: citizen ID is not registered", response.json()["feedback"])

    def test_delete_reservation_blank_citizen_id(self):
        response = requests.delete(URL + f'/reservation?citizen_id=')
        self.assertEqual("cancel reservation failed: no citizen id is given", response.json()["feedback"])
