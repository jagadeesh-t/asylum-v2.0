__author__ = 'Khudrath'
from openerp.osv import fields, osv

class hotel_activity(osv.Model):
    """
    This Model Represent The activity Creation
    """
    _name = "hotel.activity.type"
    _description = "activity type"

    _columns = {
        'name': fields.char('Activity', size=100, required=True, select=True),
    }

    _order = "name"
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Activity with this name already exist")
    ]




hotel_activity()
