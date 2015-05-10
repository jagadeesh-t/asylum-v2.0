__author__ = 'pradeep'
from openerp.osv import osv, fields
class transfer_guest(osv.TransientModel):
    _name = "transfer.guest"
    _description = "Transfer Guest"
    _columns = {
        'room_id': fields.many2one('hotel.room', 'Room Number', required=True),
    }

    def transfer_room(self, cr, uid, ids, context=None):
        for active_ids in context['active_ids']:
            for transfer_guest in self.browse(cr, uid, ids):
                self.pool.get("hotel.book.order").write(cr, uid, [active_ids], {'room_id':transfer_guest.room_id.id},context=None)
        return True