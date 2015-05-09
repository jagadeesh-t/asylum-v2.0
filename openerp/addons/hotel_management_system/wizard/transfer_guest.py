__author__ = 'pradeep'
from openerp.osv import osv, fields
class transfer_guest(osv.TransientModel):
    _name = "transfer.guest"
    _description = "Transfer Guest"
    _columns = {
        'room_id': fields.many2one('hotel.room', 'Room Number', required=True),
    }
