from datetime import datetime, timedelta
from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_name = 'reference'

    reference = fields.Char(string='Reference', default='New')
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    room_id = fields.Many2one('hospital.room', string="Room")
    date_appointment = fields.Date(string="Date", required=True)
    start_time = fields.Datetime(string="Start Time", required=True)
    end_time = fields.Datetime(string="End Time", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        default='draft', tracking=True)
    note = fields.Text(string="Note")

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')

            # Ensure start_time is a datetime object
            if 'start_time' in vals and isinstance(vals['start_time'], str):
                vals['start_time'] = fields.Datetime.from_string(vals['start_time'])

            # Ensure end_time is set correctly
            if 'start_time' in vals:
                buffer_time = 15  # Example buffer time in minutes
                start_time = fields.Datetime.from_string(vals['start_time'])
                end_time = start_time + timedelta(minutes=buffer_time)
                vals['end_time'] = fields.Datetime.to_string(end_time)

        return super(HospitalAppointment, self).create(vals_list)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
