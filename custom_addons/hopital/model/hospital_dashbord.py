from odoo import models, fields, api

class HospitalDashboard(models.Model):
    _name = 'hospital.dashboard'
    _description = 'Hospital Dashboard'

    name = fields.Char(string='Name', default='Hospital Dashboard')
    total_doctors = fields.Integer(string='Total Doctors', compute='_compute_total_doctors', store=True)
    total_patients = fields.Integer(string='Total Patients', compute='_compute_total_patients', store=True)
    total_appointments = fields.Integer(string='Total Appointments', compute='_compute_total_appointments', store=True)
    bed_occupancy_rate = fields.Float(string='Bed Occupancy Rate (%)', compute='_compute_bed_occupancy_rate', store=True)
    department_distribution = fields.Char(string='Department Distribution')
    appointment_graph = fields.Char(string='Appointment Graph')
    patient_flow_funnel = fields.Char(string='Patient Flow Funnel')
    bed_availability_map = fields.Char(string='Bed Availability Map')
    current_emergency_cases = fields.Integer(string='Current Emergency Cases', compute='_compute_current_emergency_cases', store=True)
    average_er_wait_time = fields.Float(string='Avg ER Wait Time (mins)', compute='_compute_average_er_wait_time', store=True)

    @api.depends('total_doctors')
    def _compute_total_doctors(self):
        for record in self:
            # Assigning a fixed number of doctors
            record.total_doctors = 50  # Example fixed value

    @api.depends('total_patients')
    def _compute_total_patients(self):
        for record in self:
            # Assigning a fixed number of patients
            record.total_patients = 200  # Example fixed value

    @api.depends('total_appointments')
    def _compute_total_appointments(self):
        for record in self:
            # Assigning a fixed number of appointments
            record.total_appointments = 1200  # Example fixed value

    @api.depends('bed_occupancy_rate')
    def _compute_bed_occupancy_rate(self):
        for record in self:
            # Assigning a fixed bed occupancy rate
            total_beds = 100  # Example total number of beds
            occupied_beds = 60  # Example number of occupied beds
            record.bed_occupancy_rate = (occupied_beds / total_beds) * 100 if total_beds else 0

    @api.depends('current_emergency_cases')
    def _compute_current_emergency_cases(self):
        for record in self:
            # Assigning a fixed number of emergency cases
            record.current_emergency_cases = 15  # Example fixed value

    @api.depends('average_er_wait_time')
    def _compute_average_er_wait_time(self):
        for record in self:
            # Assigning a fixed average wait time
            record.average_er_wait_time = 45  # Example fixed value (in minutes)
