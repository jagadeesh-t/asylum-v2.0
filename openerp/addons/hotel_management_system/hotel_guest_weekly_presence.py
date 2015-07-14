import datetime
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time

class hotel_guest_weekly_presence(osv.TransientModel):
    _name = "hotel.guest.weekly.presence"
    _description = "guest weekly presence"


    def button_approve(self, cr, uid, ids, context=None):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S')
        time_cmp = time.strftime('%Y-%m-%d')
        for do in self.browse(cr, uid, ids, context=context):
            if do.guest_id.points_updated_date != time_cmp:
                ids=self.pool.get('hotel.guest.points').create(cr,uid,{'guest_id':do.guest_id.id,
                                                                         'name':do.name,
                                                                         'qty':525.00,
                                                                         'up_qty':525.00,
                                                                         'date':time_now,
                                                                         'user_id':uid,
                                                                         },context=context)
                self.pool.get('hotel.guest.partner').write(cr,uid,[do.guest_id.id],{'points_updated_date':time_now})
                return {
                    'name': 'Guest Points',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'hotel.guest.points',
                    'views': [(False,'tree')],
                    'type': 'ir.actions.act_window',
                    'target':'inline',
                }
        else:
            raise osv.except_osv(_('Guest already scanned'), _('You cannot scan the same guest twice in a day'))


    _columns = {
        'guest_id': fields.many2one('hotel.guest.partner', 'Guest Name', required=True),
        'name': fields.datetime('Points Update Date'),
    }
    _defaults = {
        'name': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }


hotel_guest_weekly_presence()