from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import requests
import logging


_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    key = fields.Char(string="Key", config_parameter='gnh_auth.key')
    validity_until = fields.Datetime(string="Valid Until", config_parameter='gnh_auth.validity_until')
    valid_notify = fields.Integer(
        string="Notify Before (Days)",
        default=10,
        help="Number of days before expiration to trigger notifications.",
        config_parameter='gnh_auth.valid_notify'
    )

    
    @api.model
    def set_values(self):
        super().set_values()
        data = self.get_auth_key()
        print(" ///////// Data Function ---------->", data)

        if data:
            _logger.info("Fetched key from API: %s", data.get('key'))
            _logger.info("Fetched end_date from API: %s", data.get('end_date'))
            if 'result' in data and isinstance(data['result'], list) and data['result']:
                result_item = data['result'][0]
                print("Result Items ----->", result_item)
                if 'key' in result_item and 'end_date' in result_item:
                    self.env['ir.config_parameter'].sudo().get_param('gnh_auth.key', result_item['key'])
                    self.env['ir.config_parameter'].sudo().set_param('gnh_auth.validity_until', result_item['end_date'])
                    # _logger.info("Key and End Date: %s, %s", result_item['key'], result_item['end_date'])

                    # Assign values to self.key and self.validity_until
                    self.key = result_item['key']
                    self.validity_until = result_item['end_date']

                    print("self.key after assignment: ---> %s", self.key)
                    print("self.validity_until after assignment: ----> %s", self.validity_until)
                    # _logger.info("self.key after assignment: %s", self.key)
                    # _logger.info("self.validity_until after assignment: %s", self.validity_until)
                else:
                    # _logger.error("Expected keys 'key' and 'end_date' not found in 'result' item: %s", result_item)
                    raise ValidationError(_("Invalid Key. Please try again."))
                    # Handle the case where the expected keys are not present in the 'result' item
            else:
                # _logger.error("Expected key 'result' not found in response data or is empty: %s", data)
                raise ValidationError(_("Invalid data received from API."))
                
        # _logger.info(" $$$$$$$$ Data From Values: %s", data)
        self.env['ir.config_parameter'].set_param('gnh_auth.valid_notify', str(self.valid_notify))

    @api.constrains('valid_notify')
    def _check_valid_notify(self):
        for record in self:
            print("valid_notify - ", record.valid_notify)
            print("valid_notify - ", type(record.valid_notify))
            if record.valid_notify <= 4:
                raise ValidationError("Notify Before (Days) must be at least 4.")



    def get_auth_key(self):
        company = self.env['res.company'].sudo().browse(self.env.company.id)
        tcb_endpoint = company.tcb_website
        _logger.info("TCB Website: %s", tcb_endpoint)

        client_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        _logger.info("Client URL: %s", client_url)

        params = {'client_url': client_url}
        try:
            _logger.info("Sending request to: %s", f'{tcb_endpoint}/api/get_new_key')
            _logger.info("Request params: %s", params)
            response = requests.post(f'{tcb_endpoint}/api/get_new_key', json=params, timeout=10)
            _logger.info("Response status code: %s", response.status_code)
            _logger.info("Response content: %s", response.text)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.error("Failed to fetch the key from the external service: %s", str(e))
            if isinstance(e, requests.exceptions.ConnectionError):
                raise ValidationError(_("Unable to connect to the server. Please check the server URL and ensure it's accessible."))
            elif isinstance(e, requests.exceptions.Timeout):
                raise ValidationError(_("The request to the server timed out. Please try again later."))
            elif isinstance(e, requests.exceptions.HTTPError):
                if e.response.status_code == 404:
                    raise ValidationError(_("The requested endpoint was not found on the server. Please check the server configuration."))
                else:
                    raise ValidationError(_("An HTTP error occurred: %s") % str(e))
            else:
                raise ValidationError(_("An unexpected error occurred: %s") % str(e))

        try:
            data = response.json()
            _logger.info("Parsed JSON data: %s", data)
        except ValueError:
            _logger.error("Failed to parse JSON from response")
            raise ValidationError(_("The server returned an invalid response. Please check the server logs."))

        if isinstance(data, list) and data:
            result_item = data[0]
            if 'key' in result_item and 'end_date' in result_item:
                self.env['ir.config_parameter'].sudo().set_param('gnh_auth.key', result_item['key'])
                self.env['ir.config_parameter'].sudo().set_param('gnh_auth.validity_until', result_item['end_date'])
                self.key = result_item['key']
                self.validity_until = result_item['end_date']
                _logger.info("Key and validity set: %s, %s", self.key, self.validity_until)
                return result_item
            else:
                raise ValidationError(_("Invalid data structure received from API."))
        else:
            raise ValidationError(_("No valid data received from API."))

        

class ResCompany(models.Model):
    _inherit = 'res.company'

    tcb_website = fields.Char(string='TCB Website')







































            # Handle the case where the 'result' key is not present or the 'result' list is empty
            # # Ensure the data is not None or empty
            # if data.get('key') and data.get('end_date'):
            #     self.key = data.get('key')
            #     self.validity_until = data.get('end_date')

            #     print(" ////////// $$$$$ Key -> ", self.key)
            #     print(" ////////// $$$$$ validity_until ->", self.validity_until)
                
            #     _logger.info("self.key after assignment: %s", self.key)
            #     _logger.info("self.validity_until after assignment: %s", self.validity_until)

            #     self.env['ir.config_parameter'].sudo().set_param('gnh_auth.key', self.key)
            #     self.env['ir.config_parameter'].sudo().set_param('gnh_auth.validity_until', self.validity_until)

            #     if self.key != data.get('key'):
            #         raise ValidationError(_("Invalid Key. Please try again."))
            # else:
            #     _logger.error("Invalid data received from API: %s", data)
            #     raise ValidationError(_("Invalid data received from API."))












        # # Check if the 'result' key exists in the response data
        # if 'result' in data and isinstance(data['result'], list) and data['result']:
        #     # Extract the first item from the 'result' list
        #     result_item = data['result'][0]
        #     if 'key' in result_item and 'end_date' in result_item:
        #         # Set parameters in ir.config_parameter
        #         self.env['ir.config_parameter'].sudo().set_param('gnh_auth.key', result_item['key'])
        #         self.env['ir.config_parameter'].sudo().set_param('gnh_auth.validity_until', result_item['end_date'])
        #         _logger.info("Key and End Date: %s, %s", result_item['key'], result_item['end_date'])

        #         # Assign values to self.key and self.validity_until
        #         self.key = result_item['key']
        #         self.validity_until = result_item['end_date']

        #         _logger.info("self.key after assignment: %s", self.key)
        #         _logger.info("self.validity_until after assignment: %s", self.validity_until)
        #     else:
        #         _logger.error("Expected keys 'key' and 'end_date' not found in 'result' item: %s", result_item)
        #         # Handle the case where the expected keys are not present in the 'result' item
        # else:
        #     _logger.error("Expected key 'result' not found in response data or is empty: %s", data)
        #     # Handle the case where the 'result' key is not present or the 'result' list is empty








    # def get_auth_key(self):
    #    company = self.env['res.company'].sudo().browse(self.env.company.id)
    #    tcb_endpoint = company.tcb_website
    #    print("Tcb Website -- ", tcb_endpoint)

    #    client_url = self.env['ir.config_parameter'].sudo(
    #    ).get_param('web.base.url')
    #    print("GNH website---", client_url)
       
    #    params = {'client_url': client_url}

    #    response = requests.post(
    #             f'{tcb_endpoint}/api/get_new_key', json=params)

    #    print("Response ---", response)

    #    if response.status_code == 200:
    #         data = response.json()
    #         Key = self.env['ir.config_parameter'].sudo().set_param('gnh_auth.key', data.get('key'))
    #         enddate = self.env['ir.config_parameter'].sudo().set_param('gnh_auth.validity_until', data.get('end_date'))

    #         print(" Key //////// End Date =============$$$$$$", Key , enddate)
    #         self.key = data.get('key')
    #         self.validity_until = data.get('end_date')
    #         print(" ============= ==== //////Response ---------------------", data)
    #         print(" ============= ==== //////self.key ---------------------", self.key)
    #         print(" ============= ==== //////self.validity_until ---------------------", self.validity_until)
    #         return data


    #    if response.status_code == 200:
    #         data = response.json()
    #         self.key = data.get('key')
    #         self.validity_until = data.get('end_date')
    #         print(" ============= ==== //////Response ---------------------", data)
    #         print(" ============= ==== //////self.key ---------------------", self.key)
    #         print(" ============= ==== //////self.validity_until ---------------------", self.validity_until)
    #         return data

    #    elif response.status_code == 404:
    #         print("Response 404 error")

    #    elif response.status_code == 404:
    #         _logger.error("404 error from TCB endpoint")
    #    else:
    #         _logger.error("Error from TCB endpoint")
    #         return None
