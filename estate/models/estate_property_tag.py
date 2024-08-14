from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _sql_constraints = [('unique_tag_name', 'UNIQUE(name)', 'Tag name must be unique!')]

    name = fields.Char("Tag", required=True)
    color = fields.Integer("Color")