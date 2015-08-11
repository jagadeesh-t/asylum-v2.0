# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
    'name': 'Asylum Seeker Center',
    'version': '1.0',
    'author': 'Threshold',
    'category': 'Asylum',
    'website': 'http://www.thresholdsoft.com/',
    'summary': 'TSS Asylum Seeker Center',
    'description' : """
                    TSS Asylum Seeker
                    """,
    'depends': ['base', 'board', 'web_printscreen_zb', 'auto_backup'],
    'js' : [
        "static/src/js/view_form.js"
    ],
    'data': [
        'security/hotel_security.xml',
        'security/ir.model.access.csv',
        'hotel_menu.xml',
        'wizard/transfer_guest_view.xml',
        'wizard/add_bed_qty_view.xml',
        'wizard/reduce_bed_qty_view.xml',
        'wizard/customer_selection_view.xml',
        'wizard/guest_points_views.xml',

        'configurations/hotel_room_type_view.xml',
        'configurations/hotel_guest_type_view.xml',
        'configurations/hotel_bed_type_view.xml',
        'configurations/hotel_room_bed.xml',
        'configurations/hotel_product_category_view.xml',
        'configurations/hotel_product_unit_view.xml',
        'configurations/hotel_occupancy_view.xml',
        'configurations/hotel_activity_view.xml',

        'hotel_room_view.xml',
        'hotel_book_order_view.xml',
        'hotel_management_system_view.xml',
        'board_hotel.xml',
        'hotel_product_view.xml',
        'hotel_purchase_view.xml',
        'hotel_stock_statistics_view.xml',
        'hotel_stock_view.xml',
        'hotel_seq_view.xml',
        'hotel_guest_weekly_presence_view.xml',

        'data/hotel_stock_location_data.xml',
        'data/hotel_product_unit_data.xml',
        'data/master_data_loading.xml',
        'data/hotel_room_occupancy_data.xml',
        'Large_Label_report.xml',

        'register/hotel_stock_register_view.xml'

             ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
