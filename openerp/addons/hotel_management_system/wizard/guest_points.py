__author__ = 'pradeep'
from openerp.osv import osv, fields
class guest_points(osv.TransientModel):
    _name = "change.guest.points"
    _description = "Update Guest Points"
    _columns = {
        'points': fields.float('Points'),
    }


guest_points()