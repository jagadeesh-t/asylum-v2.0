__author__ = 'Khudrath'

from openerp.osv import fields, osv


class hotel_room_bed(osv.osv):
    """
    This Model Represent The Room Type Creation
    """
    _name = "hotel.room.bed"
    _description = "Room & Bed"
    _columns = {
        'room_id': fields.many2one('hotel.room', 'Room Reference', required=True, ondelete='cascade', select=True),
        'name': fields.many2one('hotel.bed.type', 'Bed Type', required=True, select=True),
        'bed_qty': fields.integer('Quantity'),
    }

hotel_room_bed()