from datetime import datetime, timedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price >= 0)",
            "Expected price must positive!",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price >= 0)",
            "Price must be positive!",
        ),
    ]

    name = fields.Char("Title", required=True, default="Available House")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Date Availability",
        copy=False,
        default=fields.Date.today() + timedelta(days=90),
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        "Garden Orientation",
    )

    total_area = fields.Integer("Total Area", compute="_compute_total_area")
    best_price = fields.Integer("Best Offer", compute="_compute_best_price")

    property_type_id = fields.Many2one("estate.property.type", ondelete="restrict")
    buyer = fields.Many2one("res.partner", ondelete="restrict", copy=False)
    salesperson = fields.Many2one(
        "res.users", ondelete="restrict", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", ondelete="restrict")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        "State",
        required=True,
        default="new",
        copy=False,
        readonly=True,
    )

    def set_sold(self):
        if self.state == "canceled":
            raise UserError("This property is canceled and cannot be sold")

        if not self.offer_ids:
            raise UserError("This property has not recieved any offers.")
            
        if not any(status for status in self.offer_ids.mapped('status')):
            raise UserError("This property has no accepted offers.")

        self.state = "sold"
        return True

    def set_canceled(self):
        if self.state == "sold":
            raise UserError("This property is sold and cannot be canceled")
        self.state = "canceled"
        return True

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # @api.onchange("offer_ids")
    # def _onchange_offer_ids(self):
    #     if self.offer_ids:
    #         self.state = "offer_received"

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.1) == -1:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _delete_property(self):
        if self.state not in ('new', 'canceled'):
            raise UserError("Only new and canceled properties can be deleted")
