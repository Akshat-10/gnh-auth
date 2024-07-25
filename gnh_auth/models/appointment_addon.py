from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class AppointmentAddon(models.Model):
    _inherit = 'hms.appointment'

    @api.constrains('date')
    def _check_appointment_validity(self):
        validity_until_str = self.env['ir.config_parameter'].sudo().get_param('gnh_auth.validity_until')
        print("--------- validation_until_str", validity_until_str)
        print("--------- validity_until_str", type(validity_until_str))
        valid_notify_days_str = self.env['ir.config_parameter'].sudo().get_param('gnh_auth.valid_notify')
        print("--------- valid_notify_days", valid_notify_days_str)
        print("--------- valid_notify_days", type(valid_notify_days_str))

        if not validity_until_str:  
            return

        validity_until = datetime.strptime(validity_until_str, '%Y-%m-%d').date()

        # validity_until = datetime.strptime(validity_until_str, '%Y/%m/%d %H:%M:%S').date()
        today = datetime.today().date()
        print("validity_until : ", validity_until)
        for appointment in self:
            appointment_date = appointment.date.date()
            print("appointment date : ", appointment_date)
            if appointment_date < today:
                continue
            
            valid_notify = int(valid_notify_days_str)
            print("--------- valid_notify - ", valid_notify)
            print("--------- valid_notify - ", type(valid_notify))

            
            days_remaining = (validity_until - appointment_date).days
            print("days remaining : ", days_remaining)
            if 3 <= days_remaining <= valid_notify:
                message = "Please clear payments by ",validity_until, " to avoid uninterrupted services."
                print("message - ", message)
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Payment Reminder'),
                        'type': 'warning',
                        'message': _("Please clear payments by {} to avoid uninterrupted services.").format(validity_until),
                        'sticky': True,
                    }
                }
                print("notification : ", notification)
                return notification
            elif 0 < days_remaining < 3:
                message = "Your account will be closed soon."
                print("message - ", message)
                notification = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Account Closure Warning'),
                        'type': 'warning',
                        'message': _("Your account will be closed soon."),
                        'sticky': True,
                    }
                }
                return notification
            elif days_remaining <= 0:
                raise ValidationError(_("Your account has been suspended. Please contact the administrator."))
        




class Hospitalization(models.Model):
    _inherit = 'acs.hospitalization'


    @api.constrains('date')
    def _check_appointment_validity(self):
        validity_until_str = self.env['ir.config_parameter'].sudo().get_param('gnh_auth.validity_until')
        valid_notify_days_str = self.env['ir.config_parameter'].sudo().get_param('gnh_auth.valid_notify')

        if not validity_until_str:  
            return

        validity_until = fields.Date.from_string(validity_until_str)
        today = fields.Date.today()

        for hospitalization in self:
            hospitalization_date = hospitalization.hospitalization_date.date()
            if hospitalization_date < today:
                continue
            
            valid_notify = int(valid_notify_days_str)
            
            days_remaining = (validity_until - hospitalization_date).days
            if 3 <= days_remaining <= valid_notify:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Payment Reminder'),
                        'type': 'warning',
                        'message': _("Please clear payments by {} to avoid uninterrupted services.").format(validity_until),
                        'sticky': True,
                    }
                }
            elif 0 < days_remaining < 3:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Account Closure Warning'),
                        'type': 'warning',
                        'message': _("Your account will be closed soon."),
                        'sticky': True,
                    }
                }
            elif days_remaining <= 0:
                raise ValidationError(_("Your account has been suspended. Please contact the administrator."))


class AcsPatientProcedure(models.Model):
    _inherit = 'acs.patient.procedure'


    @api.constrains('date')
    def _check_appointment_validity(self):
        validity_until_str = self.env['ir.config_parameter'].sudo().get_param('gnh_auth.validity_until')
        valid_notify_days_str = self.env['ir.config_parameter'].sudo().get_param('gnh_auth.valid_notify')

        if not validity_until_str:  
            return

        validity_until = fields.Date.from_string(validity_until_str)
        today = fields.Date.today()

        for procedure in self:
            procedure_date = procedure.date.date()
            if procedure_date < today:
                continue
            
            valid_notify = int(valid_notify_days_str)
            
            days_remaining = (validity_until - procedure_date).days
            if 3 <= days_remaining <= valid_notify:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Payment Reminder'),
                        'type': 'warning',
                        'message': _("Please clear payments by {} to avoid uninterrupted services.").format(validity_until),
                        'sticky': True,
                    }
                }
            elif 0 < days_remaining < 3:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Account Closure Warning'),
                        'type': 'warning',
                        'message': _("Your account will be closed soon."),
                        'sticky': True,
                    }
                }
            elif days_remaining <= 0:
                raise ValidationError(_("Your account has been suspended. Please contact the administrator."))





                # return {
                #     'type': 'ir.actions.client',
                #     'tag': 'display_notification',
                #     'params': {
                #         'type': 'warning',
                #         'message': _("Please clear payments by {} to avoid uninterrupted services.").format(validity_until),
                #         'sticky': True,
                #     }
                # }
                # return {'warning': {'title': _("Payment Reminder"),
                #                     'message': _("Please clear payments by {} to avoid uninterrupted services.").format(validity_until)}}


                # return {
                #     'type': 'ir.actions.client',
                #     'tag': 'display_notification',
                #     'params': {
                #         'message': message,
                #         'type': 'warning',
                #         'sticky': True,
                #     }
                # }
                # return {'warning': {'title': _("Account Closure Warning"),
                #                     'message': _("Your account will be closed soon.")}}
            








#     @api.constrains('date')
#     def _check_appointment_validity(self):
#         for appointment in self:
#             validity_until_str = self.env['ir.config_parameter'].sudo().get_param('gnh_auth.validity_until')
#             print("--------- validation_until_str", validity_until_str)
#             print("--------- validity_until_str", type(validity_until_str))
            
#             if validity_until_str == False:
#                 return
#             else:
#                 validity_until = datetime.strptime(validity_until_str, '%Y-%m-%d %H:%M:%S')

#             print('-----------config_setting----------', validity_until)
#             print('-----------config_setting type----------', type(validity_until))
#             appointment_date = appointment.date
#             print("-----------appointment_date----------", appointment_date)
#             print("-----------appointment_date type----------", type(appointment_date))

#             ten_days_before_validity_until = validity_until - timedelta(days=10)
#             print("-----------ten_days_before_validity_until ----------", ten_days_before_validity_until)
#             print("-----------ten_days_before_validity_until type----------", type(ten_days_before_validity_until))

#             print("appointment_date < ten_days_before_validity_until", appointment_date , "<" , ten_days_before_validity_until)

#             if appointment_date < ten_days_before_validity_until:
#                 print("ten_days_before_validity_until #### - ", ten_days_before_validity_until)
#                 # message = "Please clear payments by ",validity_until, " to avoid uninterrupted services."
#                 # return {
#                 #     'type': 'ir.actions.client',
#                 #     'tag': 'display_notification',
#                 #     'params': {
#                 #         'message': message,
#                 #         'type': 'warning',
#                 #         'sticky': True,
#                 #     }
#                 # }
#                 raise ValidationError(_("Please clear payments by ",validity_until, " to avoid uninterrupted services."))
            
#             three_days_before_validity_until = validity_until - timedelta(days=3)
#             print("-----------three_days_before_validity_until ----------", three_days_before_validity_until)
#             print("-----------three_days_before_validity_until type----------", type(three_days_before_validity_until))


#             print("appointment_date < three_days_before_validity_until", appointment_date , "<" , three_days_before_validity_until)




#             if appointment_date < three_days_before_validity_until:
#                 print("three_days_before_validity_until - ", three_days_before_validity_until)

#                 message = "Your account will be closed soon."
#                 return {
#                     'type': 'ir.actions.client',
#                     'tag': 'display_notification',
#                     'params': {
#                         'message': message,
#                         'type': 'warning',
#                         'sticky': True,
#                     }
#                 }
#             #     raise RedirectWarning(_("Appointment date is more than 10 days before validity until date."))
            
#             if appointment.date > validity_until:
#                 raise ValidationError(_("Your account has been suspended. Please contact the administrator."))



    # select_option = fields.Selection([
    #     ('dob', 'Date of Birth'),
    #     ('yob', 'Year of Birth'),
    # ], string='Select')

    # year_of_birth = fields.Char(string='Year of Birth')
    
    # validity = fields.Integer(
    #     string='Validity (In Days)',
    #     store=True,
    # )

    # @api.onchange('year_of_birth')
    # def _onchange_year_of_birth(self):
    #     for appointment in self:
    #         if appointment.year_of_birth:
    #             try:
    #                 birth_year_int = int(appointment.year_of_birth)
    #                 current_year = fields.Date.today().year
    #                 age = current_year - birth_year_int
    #                 appointment.age = str(age) + " Years"
    #             except ValueError:
    #                 appointment.year_of_birth = False
    #                 appointment.age = False
    #         else:
    #             appointment.age = False
    
