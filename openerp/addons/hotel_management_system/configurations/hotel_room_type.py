__author__ = 'Pradeep'
from openerp.osv import fields, osv


class tarun_hotel_room_type(osv.Model):
    """
    This Model Represent The Room Type Creation
    """
    _name = "hotel.room.type"
    _description = "Room Type"

    _columns = {
        'name': fields.char('Room Type', size=128, required=True, select=True),
    }



tarun_hotel_room_type()
