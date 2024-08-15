{
    'name': 'Estate',

    'application': True,
    'category': 'Tutorials/Estate',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer.xml',
        'views/res_users.xml',
        'views/estate_menus.xml',
    ]
}
