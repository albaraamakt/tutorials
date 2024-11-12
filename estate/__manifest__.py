{
    'name': 'Estate',

    'application': True,
    'category': 'Real Estate/Brokerage',

    'depends': ['base'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users.xml',
        'data/master_data.xml',
        'demo/demo_data.xml',
    ],

    'demo': [
        'data/demo_data.xml',
    ]
}
