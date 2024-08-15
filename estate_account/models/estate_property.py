from odoo import fields, models, api, Command


class Property(models.Model):
    _inherit = "estate.property"

    def set_sold(self):
        vals = {
            "partner_id": self.buyer.id,
            "move_type": "out_invoice",
            "invoice_line_ids": [
                Command.create(
                    {
                        "name": self.name,
                        "quantity": 1.00,
                        "price_unit": self.selling_price * 0.06,
                    }
                ),
                Command.create(
                    {
                        "name": "Administrative fees",
                        "quantity": 1.00,
                        "price_unit": 100.00,
                    }
                ),
            ],
        }
        move = self.env["account.move"].create(vals)
        # print("=================Overriding method working!=================")
        return super(Property, self).set_sold()
