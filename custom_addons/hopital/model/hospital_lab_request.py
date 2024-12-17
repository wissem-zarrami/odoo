from odoo import models, fields, api, exceptions

class HospitalLabRequest(models.Model):
    _name = 'hospital.lab.request'
    _description = 'Lab Request'

    name = fields.Char(string='Request Name', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    test_type = fields.Selection([
        ('blood', 'Blood Test'),
        ('xray', 'X-Ray'),
        ('mri', 'MRI'),
    ], string='Test Type', required=True)
    date_requested = fields.Datetime(string='Date Requested', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True)
    lab_test_ids = fields.One2many('hospital.lab.test', 'lab_request_id', string='Lab Tests')
    total_tests = fields.Integer(string='Total Tests', compute='_compute_total_tests', store=True)
    patient_name = fields.Char(string='Patient Name', related='patient_id.name', store=True)

    @api.depends('lab_test_ids')
    def _compute_total_tests(self):
        for record in self:
            record.total_tests = len(record.lab_test_ids)

    @api.constrains('date_requested')
    def _check_date_requested(self):
        for record in self:
            if record.date_requested and record.date_requested > fields.Datetime.now():
                raise exceptions.ValidationError("The request date cannot be in the future.")

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.lab.request') or ('New')
        return super(HospitalLabRequest, self).create(vals)

    def action_confirm(self):
        if not self.lab_test_ids:
            raise exceptions.UserError("Cannot confirm a request with no lab tests.")
        self.state = 'confirmed'
        self._send_notification('confirmed')

    def action_done(self):
        if not self.lab_test_ids.filtered(lambda x: x.state == 'completed'):
            raise exceptions.UserError("Cannot mark as done without completed lab tests.")
        self.state = 'done'
        # Removed notification functionality

    def action_print_report(self):
        self.ensure_one()
        report_name = 'hopital.report_lab_request'
        try:
            report = self.env.ref(report_name)
            if report._name == 'ir.actions.report':
                return report.report_action(self)
            else:
                raise exceptions.UserError(f'Report is not of type ir.actions.report: {report_name}')
        except Exception as e:
            raise exceptions.UserError(f'Error finding or using report: {str(e)}')


