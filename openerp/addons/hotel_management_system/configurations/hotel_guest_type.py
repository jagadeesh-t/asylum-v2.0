__author__ = 'pradeep'
from openerp.osv import fields, osv

class hotel_guest_type(osv.Model):
    """
    This Model Represent The Guest Type Creation
    """
    _name = "hotel.guest.type"
    _description = "Guest Type"

    _columns = {
        'name': fields.char('Guest Type', size=128, required=True, select=True),
    }



hotel_guest_type()
