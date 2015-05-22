# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
    'name': 'Hotel Management System',
    'version': '1.0',
    'author': 'Threshold',
    'category': 'Asylum',
    'website': 'http://www.thresholdsoft.com/',
    'summary': 'Hotel Management System',
    'description' : """
                    TSS Asylum Seeker instead of Hotel Management center
                    """,
    'depends': ['base'],
    'data': ['wizard/transfer_guest_view.xml',
             'wizard/add_bed_qty_view.xml',
             'wizard/reduce_bed_qty_view.xml',
             'wizard/customer_selection_view.xml',
             'wizard/guest_points_views.xml',
             'hotel_menu.xml',
             'configurations/hotel_room_type_view.xml',
             'configurations/hotel_guest_type_view.xml',
             'configurations/hotel_bed_type_view.xml',
             'hotel_room_view.xml',
             'configurations/hotel_room_bed.xml',
             'hotel_book_order_view.xml',
             'hotel_management_system_view.xml',
             # 'hotel_book_order_view.xml',
             # # 'board_hotel_view.xml',
             # 'hotel_activity_type_view.xml',
             # # 'hotel_activity_calender_view.xml',
             # 'hotel_room_view.xml',
             # # 'wizard/change_bed_qty_view.xml',
             # 'hotel_products_category_view.xml',
             # 'hotel_product_view.xml',
             'configurations/hotel_product_category_view.xml',
             'configurations/hotel_product_unit_view.xml',
             'configurations/hotel_occupancy_view.xml',
             'configurations/hotel_activity_view.xml',
             'hotel_product_view.xml',
             'hotel_purchase_view.xml',
             'hotel_stock_statistics_view.xml',
             'hotel_stock_view.xml',
             'hotel_seq_view.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
