
from odoo.tests.common import TransactionCase
from odoo.tools import tagged

class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        my_company_id = cls.env['res.company'].search([], limit=1).id
        cls.property = cls.env['estate.property'].create({
            "name": "Big House",
            "expected_price": 500000.0,
            "company_id": [4, my_company_id]
        })
        offer_ids = cls.env['estate.property.offer'].create([{
            "price": 500000,
            "partner_id": [4, cls.env['res.partner'].search([], limit=1).id],
            "property_id": [4, cls.property.id],
        },
        {
            "price": 600000,
            "partner_id": [4, cls.env['res.partner'].search([], limit=1).id],
            "property_id": [4, cls.property.id],
        }])

    @tagged('test_property')
    def test_create_offer(self):
        cls.property.offer_ids[1].set_accepted()

