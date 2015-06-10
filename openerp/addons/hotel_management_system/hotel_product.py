__author__ = 'khudrath'

from openerp.osv import fields, osv
import re


class hotel_product(osv.osv):
    _name = "hotel.product"
    _description = "product creation"


    def _get_total_stock(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        prod = self.browse(cr, uid, ids, context=context)
        trans_obj = self.pool.get('hotel.stock.transfer')
        res = {}
        for o in prod:
            ip = 0.0
            op = 0.0
            trans_op = trans_obj.search(cr,uid,[('loc_des_id.name','ilike','stock'),('product_id.id','=',o.id),('state','=','done')])
            trans_ip = trans_obj.search(cr,uid,[('loc_id.name','ilike','stock'),('product_id.id','=',o.id),('state','=','done')])
            op_list = trans_obj.read(cr,uid,trans_op,['qty'])
            ip_list = trans_obj.read(cr,uid,trans_ip,['qty'])
            if op_list:
                for i in op_list:
                    ip+=i['qty']
            if ip_list:
                for i in ip_list:
                    op+=i['qty']
            res[o.id] = ip-op
        return res


    def _get_alert_bol(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        prods = self.browse(cr, uid, ids, context=context)
        res = {}
        for prod in prods:
            avail = False
            if prod.stock_alert>prod.total_stock:
                avail=True
            res[prod.id] = avail
        return res

    def _get_alert(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        prods = self.browse(cr, uid, ids, context=context)
        res = {}
        for prod in prods:
            name =""
            if prod.stock_alert>prod.total_stock:
                name = "!!!"
            res[prod.id] = name
        return res


    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'default_code' : fields.char('Ref. Number', size=64, select=True),
        'barcode' : fields.char('Barcode', size=64, select=True),
        'unit': fields.float('Unit'),
        'product_unit': fields.many2one('hotel.product.unit', 'Unit of Measure ', required=True),
        'value': fields.float('Value'),
        'product_category': fields.many2one('hotel.product.category', 'Category', required=True),
        'stock_alert': fields.integer('Stock Alert'),
        'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the product without removing it."),
        'total_stock': fields.function(_get_total_stock, string='Current Stock', type='float', digits=(14,3)),
        'alert':fields.function(_get_alert, string='Alert', type='char'),
        'alert_bol': fields.function(_get_alert_bol, string='Alert', type='boolean'),

    }
    _defaults = {
        'active': lambda *a: 1,
    }
    _sql_constraints = [
        ('name_product_uniq', 'unique(name)', 'The name of the Product must be unique...!'),
    ]


    def name_get(self, cr, uid, ids, context=None):
        """
        Tuples with the text representation of requested objects for to-many relationships
        :param cr: database cursor
        :param uid: current login user ID
        :param ids: list of ids
        :param context: context arguments, like lang, time zone
        :return: combination of name, unit value & unit(format: "product name + space + unit value + unit)
        """
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name+" "+str(record.unit)+record.product_unit.name
            if record.default_code:
                name = record.default_code+" "+ name
            res.append((record.id, name))
        return res

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name:
            ids = self.search(cr, user, [('default_code','=',name)]+ args, limit=limit, context=context)
            if not ids:
                ids = self.search(cr, user, [('barcode','=',name)]+ args, limit=limit, context=context)
            if not ids:
                ids = set()
                ids.update(self.search(cr, user, args + [('default_code',operator,name)], limit=limit, context=context))
                if not limit or len(ids) < limit:
                    ids.update(self.search(cr, user, args + [('name',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
                ids = list(ids)
            if not ids:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    ids = self.search(cr, user, [('default_code','=', res.group(2))] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        fin = []
        if context.get('positive_only',False):
            for prod in self.browse(cr, user, ids, context=context):
                if prod.total_stock>0.0:
                    fin.append(prod.id)
        if fin:
            result = self.name_get(cr, user, fin, context=context)
        else:
            result = self.name_get(cr, user, ids, context=context)
        return result


    def unlink(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            raise osv.except_osv(('Warning!'), ("To delete a product un-check the active field on product form!!"))
        return True


hotel_product()
