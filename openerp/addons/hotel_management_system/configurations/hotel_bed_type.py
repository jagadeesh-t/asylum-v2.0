__author__ = 'Khudrath'
from openerp.osv import fields, osv

class hotel_bed_type(osv.osv):
    _name = "hotel.bed.type"
    _description = "hotel bed"

    _columns = {
        'name': fields.char('Type', size=128, required=True, select=True),
        'value': fields.integer('Capacity',help="1 for Single, 2 for Double. This will be used for counting available Spaces in a room"),
        'total_stock': fields.integer('Total Stock', help="Total Stock"),
        'available_stock': fields.integer('Available Stock', help="Available Stock"),
        'used_stock': fields.integer('Used Stock', help="Used Stock"),
    }


hotel_bed_type()
