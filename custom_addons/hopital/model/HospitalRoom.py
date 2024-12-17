from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalRoom(models.Model):
    _name = 'hospital.room'
    _description = 'Hospital Room'

    name = fields.Char(string='Room Name', required=True)
    room_type = fields.Selection([
        ('consultation', 'Consultation Room'),
        ('surgery', 'Surgery Room'),
        ('recovery', 'Recovery Room'),
    ], string='Room Type', required=True)
    equipment = fields.Char(string='Available Equipment')
    capacity = fields.Integer(string='Capacity', default=1)
    appointment_ids = fields.One2many('hospital.appointment', 'room_id', string='Appointments')

    @api.constrains('appointment_ids')
    def _check_overlapping_appointments(self):
        for room in self:
            appointments = room.appointment_ids.sorted(key='start_time')
            for i in range(len(appointments) - 1):
                current_appointment = appointments[i]
                next_appointment = appointments[i + 1]
                if current_appointment.end_time > next_appointment.start_time:
                    raise ValidationError("Overlapping appointments detected in room %s." % room.name)

class HospitalAppointment(models.Model):
    _inherit = 'hospital.appointment'

    room_id = fields.Many2one('hospital.room', string='Room', required=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)

    @api.constrains('start_time', 'end_time', 'room_id')
    def _check_appointment_times(self):
        for rec in self:
            if rec.start_time >= rec.end_time:
                raise ValidationError("End time must be after start time.")
            overlapping_appointments = self.env['hospital.appointment'].search([
                ('room_id', '=', rec.room_id.id),
                ('id', '!=', rec.id),
                ('start_time', '<', rec.end_time),
                ('end_time', '>', rec.start_time)
            ])
            if overlapping_appointments:
                raise ValidationError("This room is already booked during the selected time.")

    @api.model
    def create(self, vals):
        if 'start_time' in vals:
            start_time = fields.Datetime.from_string(vals['start_time'])
            buffer_time = 15  # 15 minutes buffer
            end_time = start_time + timedelta(minutes=buffer_time)
            vals['end_time'] = fields.Datetime.to_string(end_time)
        return super(HospitalAppointment, self).create(vals)
