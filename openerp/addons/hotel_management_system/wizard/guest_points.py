__author__ = 'pradeep'
from openerp.osv import osv, fields
import time

class guest_points(osv.TransientModel):
    _name = "change.guest.points"
    _description = "Update Guest Points"
    _columns = {
        'points': fields.float('Points'),
    }

    def change_points(self, cr, uid, ids, context=None):
        record_id = context and context.get('active_id',False)
        assert record_id, _('Active Id not found')
        guest_obj = self.pool.get('hotel.guest.partner')
        points_obj = self.pool.get('hotel.guest.points')
        for wiz in self.browse(cr, uid, ids, context=context):
            guest = guest_obj.browse(cr, uid, record_id, context=context)
            if (guest.points < wiz.points) or (guest.points > wiz.points):
                bal = wiz.points - guest.points
                time_now = time.strftime('%Y-%m-%d %H:%M:%S')
                points_obj.create(cr,uid,{
                    'guest_id':guest.id,
                    'name':'Points Updated',
                    'qty':bal,
                    'date':time_now,
                    'user_id':uid,
                        },context=context)

        return {'type': 'ir.actions.act_window_close'}



guest_points()