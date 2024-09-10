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
        self.check_access_rights('write')
        print('Bro has access to update a record on this model')
        self.check_access_rule('write')
        print('Bro even has access to update this specific record.')
        print(" reached ".center(100, '='))
        move = self.env["account.move"].sudo().create(vals)
        # print("=================Overriding method working!=================")
        return super(Property, self).set_sold()
