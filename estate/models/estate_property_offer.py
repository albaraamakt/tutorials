from datetime import timedelta

from odoo import fields, models, api
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("positive_offer_price", "CHECK(price >= 0)", "Offer price must be positive!")
    ]

    price = fields.Integer("Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", ondelete="cascade", required=True)
    property_id = fields.Many2one("estate.property", ondelete="cascade", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    def set_accepted(self):
        self.status = "accepted"
        self.property_id.buyer = self.partner_id
        self.property_id.salesperson = self.env.user
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        return True

    def set_refused(self):
        self.status = "refused"
        return True

    # Deadline date computed field done
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = timedelta(days=record.validity) + record.create_date
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=7)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 1

    @api.model
    def create(self, vals):
        property_state = self.env['estate.property'].browse(vals['property_id']).state
        if property_state == 'sold':
            raise UserError('Property has already been sold.')

        self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        return super(PropertyOffer, self).create(vals)
