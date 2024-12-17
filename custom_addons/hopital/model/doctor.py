from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Doctor"
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True, copy=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    image = fields.Binary(string="Doctor Image")
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=True)
    active = fields.Boolean(string="Active", default=True)

    # Establish a relationship with the appointment model
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string="Appointments")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (Copy)", self.doctor_name)
        default['note'] = "Copied Record"
        return super(HospitalDoctor, self).copy(default)

    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current',
        }
room_count = fields.Integer(string='Room Count', compute='_compute_room_count')

@api.depends('appointment_ids.room_id')
def _compute_room_count(self):
    for rec in self:
        rec.room_count = len(set(rec.appointment_ids.mapped('room_id')))
