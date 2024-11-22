
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.company = cls.env['res.company'].create({"name": "my_company"})
        cls.partner = cls.env['res.partner'].create({"name": "partner"})
        cls.property = cls.env['estate.property'].create({
            "name": "Big House",
            "expected_price": 500000.0,
            "company_id": cls.company.id
        })
        cls.offers = cls.env['estate.property.offer'].create([{
            "price": 500000,
            "partner_id": cls.partner.id,
            "property_id": cls.property.id
        },
        {
            "price": 600000,
            "partner_id": cls.partner.id,
            "property_id": cls.property.id
        }])

    def test_create_offer(self):
        self.offers[0].set_accepted()
        self.property.set_sold()

        self.assertRecordValues(self.offers[0], [{"status": "accepted"}])
        self.assertRecordValues(self.property, [{"state": "sold"}])
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                "partner_id": self.partner.id,
                "property_id": self.property.id,
            })

    def test_selling_sold_property(self):
        self.assertRecordValues(self.offers, [
            {
                "price": 500000,
                "partner_id": self.partner.id,
                "property_id": self.property.id,
            },
            {
                "price": 600000,
                "partner_id": self.partner.id,
                "property_id": self.property.id,
            },
        ])
        with self.assertRaises(UserError):
            self.property.set_sold()

