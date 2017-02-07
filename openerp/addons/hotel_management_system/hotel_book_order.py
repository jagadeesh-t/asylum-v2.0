import time
from openerp.osv import fields, osv

class hotel_book_order(osv.Model):

    def call_button(self, cr, uid, ids, context=None):
        for book_order in self.browse(cr, uid, ids):
            book_order.write({'state':'cout','check_out_date':time.strftime('%Y-%m-%d %H:%M:%S')})
        return True


    def _get_auto_room_id_view(self, cr, uid, ids, field_name, arg, context=None):
        all_orders=self.search(cr,uid,[],context=context)
        orders = self.browse(cr, uid, all_orders, context=context)
        res = {}
        for order in orders:
            name =""
            av_space = 0
            av_space = order.room_id.total_spaces-order.room_id.total_occupancy
            if order.state=="cin":
                name = order.room_id.name + " ( "+ str(av_space)+" ) "+ order.guest_type.name
                if order.guest_type.name == "Single":
                    if order.guest_id.gender:
                        if order.guest_id.gender == "m":
                            name+= " M"
                        else:
                            name+= " F"
            else:
                name = order.room_id.name + " ( "+ str(av_space)+" )"
            res[order.id] = name
        return res

    def _get_auto_name(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        all_orders=self.search(cr,uid,[],context=context)
        orders = self.browse(cr, uid, all_orders, context=context)
        res = {}
        for order in orders:
            name =""
	    print order.guest_id.name 
	    print order.guest_id.last_name
            print order.guest_id.guest_ref
            print order.id 
	    if  order.guest_id.name==None:
            	name =""
	    else:
		name = order.guest_id.name+" "+order.guest_id.last_name+" ["+order.guest_id.guest_ref+"]"
 	    print name
            res[order.id] = name
        return res

    def onchange_guest_ref(self, cr, uid, ids, guest_ref, context=None):
        if guest_ref:
            guest_id=self.pool.get("hotel.guest.partner").search(cr, uid, [('guest_ref', '=', guest_ref)], context=context)
            if guest_id:
                res = {'value': {}}
                guest_data=self.pool.get("hotel.guest.partner").browse(cr, uid, guest_id[0])
                res['value']['first_name'] = guest_data.name
                res['value']['last_name'] = guest_data.last_name
                res['value']['gender'] = guest_data.gender
                res['value']['country_id'] = guest_data.country_id.id
                return res
            else:
                return True
        else:
            return True


    _name = "hotel.book.order"
    _description = "Hotel Book Order"
    _order = "name"
    _columns = {
        'guest_ref': fields.char('Guest Ref.', size=128, required=True, select=True,states={'cin': [('readonly', False)]}),
        'name':fields.function(_get_auto_name, string='Name', type='char',store=True),
        'first_name': fields.char('First Name', size=128, required=True, select=True, readonly=True, states={'cin': [('readonly', False)]}),
        'last_name': fields.char('Last Name', size=128, required=True, select=True, readonly=True, states={'cin': [('readonly', False)]}),
        'gender': fields.selection([('m', 'Male'), ('f', 'Female')], 'Gender',required=True,states={'cin': [('readonly', False)]}),
        'guest_id': fields.many2one('hotel.guest.partner', 'Guest Name'),
        'guest_type': fields.many2one('hotel.guest.type', 'Guest Type',required=True),
        'country_id': fields.many2one('res.country', 'Country',),
        'room_id': fields.many2one('hotel.room', 'Room Number', required=True, ondelete='cascade',),
        'room_id_view':fields.function(_get_auto_room_id_view, string='Room Number', type='char',store=True),
        'check_in_date': fields.datetime('Check - In', help="Check-in Time.", required=True,),
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'state': fields.selection([
            ('cin', 'Check IN'),
            ('cout', 'Check OUT'),
            ], 'Status'),
        'check_out_date': fields.datetime('Check - Out', help="Check-out Time.", select=True),
    }
    _defaults = {
        'state':'cin',
        'user_id': lambda obj, cr, uid, context: uid,
        'check_in_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    def create(self, cr, user, vals, context=None):
        if vals.get('guest_ref'):
            guest_id=self.pool.get("hotel.guest.partner").search(cr, user, [('guest_ref', '=', vals.get('guest_ref'))], context=context)
            if guest_id:
                vals['guest_id']=guest_id[0]
                guest_create={
                    'guest_ref':vals['guest_ref'],
                    'name':vals['first_name'],
                    'last_name':vals['last_name'],
                    'gender':vals['gender'],
                    'country_id':vals['country_id']
                }
                self.pool.get("hotel.guest.partner").write(cr, user,[guest_id[0]],guest_create)
            else:
                guest_create={
                    'guest_ref':vals['guest_ref'],
                    'name':vals['first_name'],
                    'last_name':vals['last_name'],
                    'gender':vals['gender'],
                    'country_id':vals['country_id']
                }
                vals['guest_id']=self.pool.get("hotel.guest.partner").create(cr, user, guest_create, context)
        return super(hotel_book_order, self).create(cr, user, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        values={}
        if vals.get('guest_ref'):
            guest_id=self.pool.get("hotel.guest.partner").search(cr, uid, [('guest_ref', '=', vals.get('guest_ref'))], context=context)
            if guest_id:
               vals['guest_id']=guest_id[0]
            else:
                for record in  self.browse(cr, uid,ids):
                    if vals.get('guest_ref'):
                        guest_ref=vals.get('guest_ref')
                    else:
                        guest_ref=record.guest_ref
                    if vals.get('first_name'):
                        first_name=vals.get('first_name')
                    else:
                        first_name=record.first_name
                    if vals.get('guest_ref'):
                        gender=vals.get('gender')
                    else:
                        gender=record.gender
                    if vals.get('last_name'):
                        last_name=vals.get('last_name')
                    else:
                        last_name=record.last_name
                    if vals.get('country_id'):
                        country=vals.get('country_id')
                    else:
                        country=record.country_id

                    guest_create={
                        'guest_ref':guest_ref,
                        'name':first_name,
                        'last_name':last_name,
                        'gender':gender,
                        'country_id':country
                    }
                vals['guest_id']=self.pool.get("hotel.guest.partner").create(cr, uid, guest_create, context)

        if vals.get('first_name'):
            values['name'] =vals.get('first_name')
        if vals.get('last_name'):
            values['last_name'] =vals.get('last_name')
        if vals.get('gender'):
            values['gender']=vals.get('gender')
        if vals.get('country_id'):
            values['country_id ']=vals.get('country_id')

        if values:
            if vals.get('guest_ref'):
                self.pool.get("hotel.guest.partner").write(cr, uid, [vals['guest_id']],values)
            else:
                for record in  self.browse(cr, uid,ids):
                    self.pool.get("hotel.guest.partner").write(cr, uid, [record.guest_id.id],values)

        return super(hotel_book_order, self).write(cr, uid, ids, vals, context=context)
