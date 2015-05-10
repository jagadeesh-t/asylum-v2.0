__author__ = 'Khudrath'
from openerp.osv import fields, osv

class hotel_product_unit(osv.Model):
    """
    This Model Represent The Product Unit Creation
    """
    _name = "hotel.product.unit"
    _description = "product unit"

    _columns = {
        'name': fields.char('Product Unit', size=100, required=True, select=True),
    }

    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique (name)', "With this Product Unit, record already present..!")
    ]
hotel_product_unit()
