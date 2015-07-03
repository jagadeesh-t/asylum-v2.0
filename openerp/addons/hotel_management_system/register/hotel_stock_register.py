__author__ = 'pradeep'
from openerp.osv import fields, osv

class hotel_stock_register(osv.Model):
    """
    This Model Represent The Stock Duration Creation
    """
    _name = "hotel.stock.register"
    _description = "Stock Registeer"

    _columns = {
        'to_date': fields.date('To Date', required=True,),
        'from_date': fields.date('From Date', required=True,),
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