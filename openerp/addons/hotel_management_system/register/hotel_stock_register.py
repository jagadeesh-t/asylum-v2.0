__author__ = 'pradeep'
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class hotel_stock_register(osv.Model):
    """
    This Model Represent The Stock Duration Creation
    """
    def onchange_stock_statistics(self, cr, uid, ids, to_date,from_date, context=None ):
        res = {}
        total_points=0.0
        if to_date != False and from_date != False:
            line=[]
            cr.execute('select hpl.product_id,sum(hpl.qty) as qty,sum(hpl.qty*hpl.pts_unit) as pts from hotel_purchase hp inner join hotel_purchase_lines hpl on hp.id = inv_id where hp.state  = \'done\'  and date(date) >= %s and date(date)<= %s group by hpl.product_id',(to_date, from_date,))
            for t in cr.dictfetchall():
                line.append([0, False, {'product_category': t['product_id'], 'pts': t['pts'], 'qty': t['qty']}])
                total_points=total_points+float(t['pts'])
            res['inv_lines']= line
            res['total_points']= total_points
            return {'value': res}
        # else:
        #     warning = {
        #             'title': _('Warning!'),
        #             'message': _('The selected unit of measure is not compatible with the unit of measure of the product.')
        #         }
        #     return {'warning': warning}

    _name = "hotel.stock.register"
    _description = "Stock Registeer"

    _columns = {
        'to_date': fields.date('To Date', required=True,),
        'from_date': fields.date('From Date', required=True,),
        'total_points':fields.float('Total Points',digits=(14, 3)),
        'inv_lines': fields.one2many('hotel.stock.statistics.register', 'inv_id', 'Purchase Order Lines',),
        }

hotel_stock_register()

class hotel_stock_line_register(osv.Model):
    """
    This Model Represent The Stock Details Creation
    """
    _name = "hotel.stock.statistics.register"
    _description = "Stock Statistics Registeer "

    _columns = {
        'inv_id': fields.many2one('hotel.stock.register', 'INV'),
        'product_category': fields.many2one('hotel.product', 'Category',),
        'pts': fields.float('Total Points',digits=(14, 3)),
        'qty': fields.float('Quantity', digits=(14, 3)),
        }

hotel_stock_line_register()