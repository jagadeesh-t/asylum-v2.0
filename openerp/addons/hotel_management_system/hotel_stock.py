from openerp.osv import fields, osv
import time
import re
from datetime import datetime
from datetime import timedelta  
from openerp.tools.translate import _


class hotel_stock_location(osv.osv):
    _name = "hotel.stock.location"
    _description = "Stock Location"
    
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),  
        'description': fields.text('Description'),    
    }
hotel_stock_location()


class hotel_stock_transfer(osv.osv):
    _name = "hotel.stock.transfer"
    _description = "Stock Transfer"


    def button_done(self, cr, uid, ids, context=None):
        
        for do in self.browse(cr, uid, ids, context=context):
            time_now = time.strftime('%Y-%m-%d %H:%M:%S')
            return self.write(cr,uid,ids,{'state': 'done','date': time_now,},context=context)

    def button_cancel(self, cr, uid, ids, context=None):
        
        for do in self.browse(cr, uid, ids, context=context):
            time_now = time.strftime('%Y-%m-%d %H:%M:%S')
            return self.write(cr,uid,ids,{'state': 'cancel','date': time_now,},context=context)
        
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'qty': fields.float('Quantity', digits=(14,3)),
        'product_id': fields.many2one('hotel.product', 'Product', required=True),
        'loc_id': fields.many2one('hotel.stock.location', 'Source', required=True),
        'loc_des_id': fields.many2one('hotel.stock.location', 'Destination', required=True),
        'date': fields.datetime('Date', help="Date.", required=True, select=True, readonly=True, states={'draft': [('readonly', False)]}),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
            ], 'Status', readonly=True, select=True),    
        'user_id': fields.many2one('res.users', 'User', readonly=True),
    }

    
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': 'draft',
        'user_id': lambda obj, cr, uid, context: uid,
    }


hotel_stock_transfer()


class hotel_update_stock(osv.osv):
    _name = "hotel.update.stock"
    _description = "Stock Update"

    def action_view_new_inv(self, cr, uid, ids, context=None):

        print "--------------------------------------------------------------"
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        inv_ids =[]
        result = mod_obj.get_object_reference(cr, uid, 'hotel_management_system', 'action_hotel_update_stock')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        test_id = self.create(cr,uid,{'name':'Today Inv','date':time.strftime('%Y-%m-%d %H:%M:%S')})
        print test_id
        prod_ids= self.pool.get('hotel.product').search(cr,uid,[])
        for prod in self.pool.get('hotel.product').browse(cr, uid, prod_ids):
            self.pool.get('hotel.update.stock.lines').create(cr,uid,{'inv_id': test_id,
                                                                     'product_id': prod['id'],
                                                                     'product_category': prod['product_category']['id']})
        inv_ids.append(test_id)
        res = mod_obj.get_object_reference(cr, uid, 'hotel_management_system', 'hotel_update_stock_form')
        result['views'] = [(res and res[1] or False, 'form')]
        result['res_id'] = inv_ids and inv_ids[0] or False
        result['target'] = 'inline'
        return result
     


    def button_done(self, cr, uid, ids, context=None):
        
        for do in self.browse(cr, uid, ids, context=context):
            time_now = time.strftime('%Y-%m-%d %H:%M:%S')
            try:
                stock = self.pool.get('hotel.stock.location').search(cr,uid,[('name','ilike','stock')])
                purchase = self.pool.get('hotel.stock.location').search(cr,uid,[('name','ilike','purchase')])
                loc_id = purchase[0]
                loc_des_id = stock[0]
            except:                
                raise osv.except_osv(_('Location Error!'), _('Please create location name "Stock" and "Purchase"!'))
            for lines in do.inv_lines:
                if lines.qty and lines.qty>0.0:
                    self.pool.get('hotel.stock.transfer').create(cr,uid,{'name':do.name,
                                                                               'product_id':lines.product_id.id,
                                                                               'qty':lines.qty,
                                                                               'loc_id':loc_id,
                                                                               'loc_des_id':loc_des_id,
                                                                               'date':time_now,
                                                                               'user_id':uid,
                                                                               'state':'done'})
                    
            self.write(cr,uid,ids,{'state': 'done','date': time_now,},context=context)
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.get_object_reference(cr, uid, 'hotel_management_system', 'action_hotel_product')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        inv_ids = self.pool.get('hotel.product').search(cr,uid,[])
        result['domain'] = "[('id','in',["+','.join(map(str, inv_ids))+"])]"
        return result

    def button_cancel(self, cr, uid, ids, context=None):
        
        for do in self.browse(cr, uid, ids, context=context):
            time_now = time.strftime('%Y-%m-%d %H:%M:%S')
            return self.write(cr,uid,ids,{'state': 'cancel','date': time_now,},context=context)
        
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'date': fields.datetime('Date', help="Date.", required=True, select=True, readonly=True, states={'draft': [('readonly', False)]}),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
            ], 'Status', readonly=True, select=True),    
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'inv_lines': fields.one2many('hotel.update.stock.lines','inv_id', 'Stock Lines', readonly=True, states={'draft': [('readonly', False)]}),
    }

    
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': 'draft',
        'user_id': lambda obj, cr, uid, context: uid,
    }

hotel_update_stock()


class hotel_update_stock_lines(osv.osv):
    _name = "hotel.update.stock.lines"
    _description = "Stock Update Lines"
       
    _columns = {
        'inv_id': fields.many2one('hotel.update.stock', 'INV'),
        'product_id': fields.many2one('hotel.product', 'Product', required=True),
        'product_category': fields.many2one('hotel.product.category', 'Category'),
        'cur_qty': fields.related('product_id','total_stock',type='float', digits=(14,3),string='Current Stock',
            readonly=True, store=True),
        'qty': fields.float('Quantity', digits=(14,3)),
    }


hotel_update_stock_lines()


