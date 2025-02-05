from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


class FuelTank(models.Model):
    _name = 'fuel.tank'
    _description = 'Fuel Tank Integration'

    # Tank Details
    name = fields.Char(string='Name', required=True)
    location = fields.Char(string='Location')
    date = fields.Date(string="Last Clean Date")

    # Fuel Details
    capacity = fields.Float(string='Capacity')
    liters = fields.Float(string='Liters', compute='_compute_total_liters')
    average_price = fields.Float(string='Average Price', compute='_compute_avg_amount')

    # Last filling Details
    last_filling_date = fields.Date(string='Last Filling Date', readonly=True)
    last_filling_amount = fields.Float(string='Last Filling Amount', compute='_compute_last_filling_price')
    last_filling_price = fields.Float(string='Last Filling Price', )

    # Consumption Details
    total_filling_fuel = fields.Float(string='Total Filling Fuel (%)', compute='_compute_total_filling_fuel')
    last_added_fuel_date = fields.Date(string='Last Added Fuel Date', readonly=True)

    line_ids = fields.One2many('fuel.tank.lines', 'fuel_tank_id', string='Data')

    @api.depends('line_ids')
    def _compute_total_liters(self):
        for rec in self:
            rec.liters = sum(line.tank_liters for line in rec.line_ids)

    @api.depends('line_ids')
    def _compute_avg_amount(self):
        for rec in self:
            total_price = sum(line.tank_liters * line.tank_average_price for line in rec.line_ids)
            total_liters = sum(line.tank_liters for line in rec.line_ids) or rec.liters
            rec.average_price = total_price / total_liters if total_liters else 0

    @api.depends('line_ids', 'capacity')
    def _compute_total_filling_fuel(self):
        for rec in self:
            rec.total_filling_fuel = (
                        sum(line.tank_liters for line in rec.line_ids) / rec.capacity * 100) if rec.capacity else 0

    @api.depends('line_ids')
    def _compute_last_filling_price(self):
        for rec in self:
            if rec.line_ids:
                last_line = rec.line_ids[-1]
                # rec.last_filling_price = last_line.tank_average_price
                rec.last_filling_amount = last_line.tank_liters * last_line.tank_average_price
            else:
                rec.last_filling_amount = None


    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if self.env['fuel.tank'].search([('name', '=', rec.name), ('id', '!=', rec.id)]):
                raise ValidationError(f"Name '{rec.name}' already exists.")

    @api.constrains('capacity')
    def _check_capacity(self):
        for rec in self:
            if rec.capacity <= 0:
                raise ValidationError("Capacity must be greater than zero.")


class FuelTankLines(models.Model):
    _name = 'fuel.tank.lines'

    fuel_tank_id = fields.Many2one('fuel.tank', string='Fuel Tank')
    tank_last_added_fuel_date = fields.Date(string='Date')
    tank_liters = fields.Float(string='Liters')
    tank_average_price = fields.Float(string='Price')
