from odoo import fields, models, api

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Type", required=True)
    sequence = fields.Integer('Sequence')
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)