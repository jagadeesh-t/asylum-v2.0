__author__ = 'pradeep'
from openerp.osv import fields, osv
import time

class hotel_guest_point(osv.Model):
    _name = "hotel.guest.points"
    _description = "Hotel Guest Poiints"
    _columns = {
        'guest_id': fields.many2one('hotel.guest.partner', 'Guest Name', select=True),
        'name': fields.char('Name', size=128, required=True, select=True),
        # 'purchase_id': fields.many2one('tarun.hotel.purchase', 'Purchase Order', select=True),
        'qty': fields.float('Points'),
        'up_qty': fields.float('Updated Points'),
        'date': fields.datetime('Date', help="Date.", required=True, select=True, readonly=True),
        'user_id': fields.many2one('res.users', 'Approved By', readonly=True),
        'state': fields.selection([
            ('draft', 'To Approve'),
            ('done', 'Approved'),
            ], 'Status', readonly=True, select=True),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': lambda obj, cr, uid, context: uid,
    }

hotel_guest_point()
