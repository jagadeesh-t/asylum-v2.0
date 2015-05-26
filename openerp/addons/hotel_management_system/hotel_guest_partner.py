__author__ = 'pradeep'
from openerp.osv import fields, osv
from openerp import pooler, tools
from datetime import date
from datetime import datetime

class hotel_guest_partner(osv.Model):
    _name="hotel.guest.partner"
    _description="Guest"

    def _get_cur_points(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        prod = self.browse(cr, uid, ids, context=context)
        res = {}
        for o in prod:
            points = 0.0
            if o.points_hist:
                for lines in o.points_hist:
                    points+=lines.qty
                    points = points
                    self.pool.get('hotel.guest.points').write(cr,uid,[lines.id],{'up_qty':points})
            res[o.id] = points
        return res

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.last_name+" "+record.name+" ["+record.guest_ref+"]"
            res.append((record.id, name))
        return res

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    def onchange_state(self, cr, uid, ids, state_id, context=None):
        if state_id:
            country_id = self.pool.get('res.country.state').browse(cr, uid, state_id, context).country_id.id
            return {'value':{'country_id':country_id}}
        return {}

    def _compute_lines(self, cr, uid, ids, name, args, context=None):
        result = {}
        order_obj=self.pool.get('hotel.book.order')
        for guest in self.browse(cr, uid, ids, context=context):
            orders = []
            orders = order_obj.search(cr,uid, [['state', '=', 'cin'],['guest_ref', '=', guest.guest_ref]], context=context)
            result[guest.id] = orders
        return result

    def onchange_calculate_age(self, cr, uid, ids, born, context=None):
        if born != False:
            born=datetime.strptime(born, '%Y-%m-%d')
            today = datetime.today()
            try:
                birthday = born.replace(year=today.year)
            except ValueError: # raised when birth date is February 29 and the current year is not a leap year
                birthday = born.replace(year=today.year, month=born.month+1, day=1)
            if birthday > today:
                age= today.year - born.year - 1
                return {'value': {'age': age,}}
            else:
                age= today.year - born.year
                return {'value': {'age': age,}}
        else:
            return {'value': {'age': False,}}


    _columns={
        'guest_ref': fields.char('Guest Ref.', size=128, required=True, select=True),
        'name': fields.char('First Name', size=128, required=True, select=True),
        'last_name': fields.char('Last Name', size=128, required=True, select=True),
        'user_id': fields.many2one('res.users', 'User', help='The internal user that is in charge of communicating with this contact if any.'),
        'comment': fields.text('Notes'),
        'city': fields.char('City', size=128),
        'state_id': fields.many2one("res.country.state", 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
        'country': fields.related('country_id', type='many2one', relation='res.country', string='Country',
                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
        'email': fields.char('Email', size=240),
        'phone': fields.char('Phone', size=64),
        'fax': fields.char('Fax', size=64),
        'mobile': fields.char('Mobile', size=64),
        # image: all image fields are base64 encoded and PIL-supported
        'image': fields.binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'hotel.guest.partner': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of this contact. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'hotel.guest.partner': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of this contact. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        # 'has_image': fields.function(_has_image, type="boolean"),
        'company_id': fields.many2one('res.company', 'Company', select=1),
        'color': fields.integer('Color Index'),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female')], 'Gender',),
        'pref': fields.selection([('veg', 'Veg'), ('nveg', 'Non-Veg')], 'Diet',),
        'dob': fields.date('Date of Birth'),
        'cin_date': fields.date('Check-in Date'),
        'age': fields.integer('Age'),
        'book_hist' : fields.function(_compute_lines, relation='hotel.book.order', type="many2many", string='Booking History'),
        'available': fields.boolean('Available'),
        'points_hist': fields.one2many('hotel.guest.points', 'guest_id', 'Points'),
        'points': fields.function(_get_cur_points, string='Points', type='float', readonly=True),
    }
    _order = "name"
    _defaults = {
        'company_id': lambda self, cr, uid, ctx: self.pool.get('res.company')._company_default_get(cr, uid, 'tarun.hotel.guest.partner', context=ctx),
        'color': 0,
        'image': False,
        'user_id': lambda obj, cr, uid, context: uid,
	    'available': True,
    }
    _sql_constraints = [
        ('name_guest_uniq', 'unique(guest_ref)', 'The name of the Guest Reference must be unique...!'),
    ]

hotel_guest_partner()