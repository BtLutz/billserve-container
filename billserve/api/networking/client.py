from billserve.api.networking.http import HttpClient
import xmltodict
import json
from billserve.api.networking.models.MagicDict import MagicDict


class GovinfoClient:
    http = HttpClient()

    @staticmethod
    def create_bill_from_url(url):
        """
        Creates a bill instance from a baby URL.
        :param url: THe URL of the bill you'd like to create
        :return: The created bill
        """
        from api.models import Bill
        response = GovinfoClient.http.get(url)
        bill_data_raw = xmltodict.parse(response.data)

        if 'billStatus' not in bill_data_raw or 'bill' not in bill_data_raw['billStatus']:
            raise KeyError('Malformed XML data found at {url}'.format(url=url))

        bill_data_raw = bill_data_raw['billStatus']['bill']

        bill_data = MagicDict(bill_data_raw, Bill.members, Bill.optional_members).cleaned()
        bill_data['url'] = url

        return Bill.objects.create_from_dict(bill_data)

    @staticmethod
    def create_bill_url(congress, bill_type, number):
        """
        Generates a govinfo bill URL with the required components.
        :param congress: The congress of the bill (115, 114, 113, etc.)
        :param bill_type: The type of the bill (S, HR, SJ, HRJ, etc.)
        :param number: The number of the bill in its congress (987, 314, etc.)
        :return: A URL that points towards the bill's location on GovInfo.
        """
        return \
            'https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{type}/BILLSTATUS-{congress}{type}{number}.xml' \
            .format(congress=congress, type=bill_type.lower(), number=number)

    @staticmethod
    def create_bill_url_list_from_origin(origin_url):
        response = json.loads(GovinfoClient.http.get(origin_url).data)
        return [result['link'] for result in response['files']]

