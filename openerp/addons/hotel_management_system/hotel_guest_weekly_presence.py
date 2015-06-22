
import datetime
from lxml import etree
import math
import pytz
import re
import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time






class hotel_guest_weekly_presence(osv.osv):
    _name = "hotel.guest.weekly.presence"
    _description = "guest weekly presence"


    def button_approve(self, cr, uid, ids, context=None):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S')
        for do in self.browse(cr, uid, ids, context=context):
            self.pool.get('hotel.guest.points').create(cr,uid,{'guest_id':do.guest_id.id,
                                                                     'name':do.name,
                                                                     'qty':do.qty*525.00,
                                                                     'date':time_now,
                                                                     'user_id':uid,
                                                                     },context=context)

        return self.write(cr,uid,ids,{'state': 'done'},context=context)


    def _generate_guest_attendance(self, cr, uid, ids, context=None):
        """
        @return: Dictionary of values.
        """
        guest_obj = self.pool.get('hotel.guest.partner')
        guests = guest_obj.search(cr,uid,[('available','=',True)])
        for guest in guest_obj.browse(cr, uid, guests):
            # default format is yyyy-mm-dd
            diff = (datetime.datetime.now() - datetime.datetime.strptime(guest.cin_date,'%Y-%m-%d')).days
            date_end = datetime.datetime.now().strftime('%Y-%m-%d')
            date_end2 = datetime.datetime.now().strftime('%Y-%d-%m')[5:10]
            date_start = guest.cin_date
            name = datetime.datetime.strptime(guest.cin_date,'%Y-%m-%d').strftime('%Y-%d-%m')[5:10] + ' to ' + date_end2

            if diff>7:
                date_start2 = datetime.datetime.now() - datetime.timedelta(days=7)
                name = date_start2.strftime('%Y-%d-%m')[5:10] + ' to ' + date_end2
                date_start = date_start2.strftime('%Y-%m-%d')
                diff = 7
            if diff > 0:
                self.create(cr,uid,{'name':name,
                                    'date_start':date_start,
                                    'date_end':date_end,
                                    'qty': diff,
                                    'guest_id': guest.id})
        return True


    def _approve_guest_attendance(self, cr, uid, ids, context=None):
        """
        @return: Dictionary of values.
        """
        to_app = self.search(cr,uid,[('state','=','draft')],context=context)
        return self.button_approve(cr,uid,to_app,context=context)



    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True, readonly=True, states={'draft': [('readonly', False)]}),
        'guest_id': fields.many2one('hotel.guest.partner', 'Guest Name', select=True, required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'date_start': fields.date('Date', help="Date From", required=True, select=True, readonly=True, states={'draft': [('readonly', False)]}),
        'date_end': fields.date('Date', help="Date Till", required=True, select=True, readonly=True, states={'draft': [('readonly', False)]}),
        'guest_rel_related': fields.related('guest_id', 'guest_ref', type='char', string='Guest Ref.', readonly=True, store=True),
        'qty': fields.integer('Total Days Present', readonly=True, states={'draft': [('readonly', False)]}),
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'state': fields.selection([
            ('draft', 'To Approve'),
            ('done', 'Approved'),
            ], 'Status', readonly=True, select=True),

    }

    _defaults = {
        'state':'draft',
        'user_id': lambda obj, cr, uid, context: uid,
    }

    _order = 'guest_rel_related asc'


    def create(self, cr, uid, vals, context=None):
        if 'qty' in vals:
            if vals['qty']>7 or vals['qty']<0:
                raise osv.except_osv(_('Error!'),
                _('Present Days is always less than 7 and greater than 0'))
        return super(hotel_guest_weekly_presence, self).create(cr, uid, vals, context=context)



    def write(self, cr, uid,ids, vals, context=None):
        if 'qty' in vals:
            if vals['qty']>7 or vals['qty']<0:
                raise osv.except_osv(_('Error!'),
                _('Present Days is always less than 7 and greater than 0'))
        return super(hotel_guest_weekly_presence, self).write(cr, uid,ids, vals, context=context)



hotel_guest_weekly_presence()