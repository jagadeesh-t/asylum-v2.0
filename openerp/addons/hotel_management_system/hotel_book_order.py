import time
from openerp.osv import fields, osv

class hotel_book_order(osv.Model):

    def call_button(self, cr, uid, ids, context=None):
        for book_order in self.browse(cr, uid, ids):
            book_order.write({'state':'cout','check_out_date':time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    _name = "hotel.book.order"
    _description = "Hotel Book Order"
    _columns = {
        'guest_ref': fields.char('Guest Ref.', size=128, required=True,),
        'first_name': fields.char('First Name', size=128, required=True, ),
        'last_name': fields.char('Last Name', size=128, required=True,),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female')], 'Gender', ),
        'guest_type': fields.many2one('hotel.guest.type', 'Guest Type',required=True),
        'country_id': fields.many2one('res.country', 'Country',),
        'room_id': fields.many2one('hotel.room', 'Room Number', required=True, ondelete='cascade',),
        # 'room_id_view':fields.function(_get_auto_room_id_view, string='Room Number', type='char',store=True),
        'check_in_date': fields.datetime('Check - In', help="Check-in Time.", required=True,),
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'state': fields.selection([
            ('cin', 'Check IN'),
            ('cout', 'Check OUT'),
            ], 'Status'),
        'check_out_date': fields.datetime('Check - Out', help="Check-out Time.", select=True),
    }
    _defaults = {
        'state':'cin',
        'user_id': lambda obj, cr, uid, context: uid,
        'check_in_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }