__author__ = 'Khudrath'
from openerp.osv import fields, osv

class hotel_product_category(osv.Model):
    """
    This Model Represent The Product Category Creation
    """
    _name = "hotel.product.category"
    _description = "product category"

    _columns = {
        'name': fields.char('Product Category', size=100, required=True, select=True),
    }

    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique (name)', "With this Product category, record already present..!")
    ]




hotel_product_category()
