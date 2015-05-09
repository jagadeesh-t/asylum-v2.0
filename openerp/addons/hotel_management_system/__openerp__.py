# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
    'name': 'Hotel Management System',
    'version': '1.0',
    'author': 'Pradeep & Ali',
    'category': 'Hotel Management System',
    'website': 'http://www.thresholdsoft.com/',
    'summary': 'Hotel Management System',
    'description' : """
                    Hotel Management System
                    """,
    'depends': ['base'],
    'data': ['wizard/transfer_guest_view.xml',
             'wizard/add_bed_qty_view.xml',
             'wizard/reduce_bed_qty_view.xml',
             'hotel_menu.xml',
             'configurations/hotel_room_type_view.xml',
             'configurations/hotel_guest_type_view.xml',
             'configurations/hotel_bed_type_view.xml',
             'hotel_room_view.xml',
             'configurations/hotel_room_bed.xml',
             'hotel_book_order_view.xml',
             # 'hotel_book_order_view.xml',
             # # 'board_hotel_view.xml',
             # 'hotel_activity_type_view.xml',
             # # 'hotel_activity_calender_view.xml',
             # 'hotel_room_view.xml',
             # # 'wizard/change_bed_qty_view.xml',
             # 'hotel_products_category_view.xml',
             # 'hotel_product_view.xml',
             'configurations/hotel_product_category_view.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
