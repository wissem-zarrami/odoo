from odoo import models, fields, api, exceptions
from datetime import datetime

class HospitalLabTest(models.Model):
    _name = 'hospital.lab.test'
    _description = 'Lab Test'

    name = fields.Char(string='Test Name', required=True)
    lab_request_id = fields.Many2one('hospital.lab.request', string='Lab Request', required=True, ondelete='cascade')
    result = fields.Text(string='Test Result')
    notes = fields.Text(string='Additional Notes')
    date_conducted = fields.Datetime(string='Date Conducted', default=fields.Datetime.now)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ], string='Status', default='pending')

    is_overdue = fields.Boolean(string='Is Overdue', compute='_compute_is_overdue', store=True)

    @api.depends('date_conducted')
    def _compute_is_overdue(self):
        for record in self:
            if record.state == 'pending' and record.date_conducted:
                record.is_overdue = record.date_conducted < datetime.now()
            else:
                record.is_overdue = False

    @api.constrains('date_conducted')
    def _check_date(self):
        for record in self:
            if record.date_conducted and record.date_conducted > fields.Datetime.now():
                raise exceptions.ValidationError("The date conducted cannot be in the future.")

    @api.constrains('result')
    def _check_result(self):
        for record in self:
            if not record.result:
                raise exceptions.ValidationError("Test result cannot be empty.")

    def action_mark_completed(self):
        self.ensure_one()
        if self.state == 'completed':
            raise exceptions.UserError("The test is already marked as completed.")
        self.state = 'completed'

    def action_mark_pending(self):
        self.ensure_one()
        if self.state == 'pending':
            raise exceptions.UserError("The test is already marked as pending.")
        self.state = 'pending'

    def action_view_lab_request(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lab Request',
            'res_model': 'hospital.lab.request',
            'view_mode': 'form',
            'res_id': self.lab_request_id.id,
            'target': 'current',
        }

    def action_print_report(self):
        self.ensure_one()
        return self.env.ref('hopital.report_lab_test').report_action(self)
