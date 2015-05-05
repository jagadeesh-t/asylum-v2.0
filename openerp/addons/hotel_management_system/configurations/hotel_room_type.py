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
    _sql_constraints = [
        ('name_room_type_uniq', 'unique(name)', 'The name of the Room Type must be unique...!'),
    ]



tarun_hotel_room_type()
