from django.test import TestCase
from pretix_borderland.models.lottery_entry import LotteryEntry
from pretix_borderland.forms.lottery import RegisterForm
from pretix_borderland.views.lottery import Register
from unittest.mock import patch
from pretix_borderland.tasks import send_mail

#from .waiting_list import WaitingList
#MIGRATION_MODULES = DisableMigrations()

@patch('pretix_borderland.tasks.send_mail')
class RegisteringLoteryTestCases(TestCase):
    # These test cases are to check that the registration to the lottery is working
    # correctly. The test cases are:
    # 1. User that is not in the lottery joins successfully
    # 2. If the input data is not valid, the user cannot join the lottery until the data is valid
    # 3. User that is already in the lottery cannot join again
    # 4. User that is not in the lottery cannot join if the lottery is closed
    def setUp(self):
            self.john_doe = {
                "email": "john.doe@somewhere.com",
                "dob": "1989-09-09",
                "first_name": "John",
                "last_name": "Doe"
            }

    def test_user_joins_lottery_successfully(self, mock_send_mail):
        mock_send_mail.delay = lambda *args, **kwargs: None

        # test using the http client
        response = self.client.post("borderlandtest/year/register/", data=self.john_doe)
        self.assertEqual(response.status_code, 201)

        u = LotteryEntry.objects.get(email="john.doe@somewhere.com")
        self.assertIsNotNone(u)
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Doe")
        self.assertEqual(u.dob, "1989-09-09")


# class WaitingListTestCase(TestCase):
#     def setUp(self):
#         self.john_doe = {
#             "email": "john.doe@somewhere.com",
#             "dob": "1989-09-09",
#             "first_name": "John",
#             "last_name": "Doe"
#         }
#
#     def test_user_that_is_not_in_waiting_list_joins_successfully(self):
#         w = WaitingList()
#         r = w.form_valid(forms.JoinWaitingList(initial=self.john_doe))
#         self.assertEqual(r.status_code, 201)
#         u = models.WaitingList.objects.get(email="john.doe@somewhere.com")
#         self.assertIsNotNone(u)
