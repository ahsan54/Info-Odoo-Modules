from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class AddFuelWizard(models.TransientModel):
    _name = 'add.fuel'
    description = 'Add Fuel Wizard'

    liters = fields.Float(string='Liters', required = True)
    average_price = fields.Float(string='Price Per Liter', required = True)

    def action_add_fuel(self):
        print(self.env.context.get('active_ids'))
        result = self.env['fuel.tank'].browse(self.env.context.get('active_ids'))
        print(result.name)
        if self.liters > result.capacity or self.liters < 0:
            raise ValidationError("Out of Capacity Range")
        else:
            # print(self.liters)
            # print(result.liters)
            total = result.liters + self.liters
            if total > result.capacity:
                raise ValidationError(f'Tank remaining only {result.capacity - result.liters} liters')
            result.last_added_fuel_date = datetime.today()

            self.env['fuel.tank.lines'].create({
                'tank_last_added_fuel_date': result.last_added_fuel_date,
                'tank_average_price': self.average_price,
                'tank_liters': self.liters,
                'fuel_tank_id': result.id,
            })

    @api.constrains('liters')
    def _check_liters(self):
        for rec in self:
            if rec.liters == 0.00 or rec.liters == 0:
                raise ValidationError(f"liters can't be zero")

    @api.constrains('average_price')
    def _check_liters(self):
        for rec in self:
            if rec.average_price == 0.00 or rec.average_price == 0:
                raise ValidationError(f"Price per liter can't be zero")