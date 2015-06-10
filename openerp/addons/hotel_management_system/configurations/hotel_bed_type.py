__author__ = 'Khudrath'
from openerp.osv import fields, osv


class hotel_bed_type(osv.osv):
    _name = "hotel.bed.type"
    _description = "hotel bed"

    def _used_stock(self, cr, uid, ids, fieldnames, args, context=None):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            bed_qty = 0
            list_ids = self.pool.get("hotel.room.bed").search(cr, uid, [('name', '=', obj.id)], context=None)
            for list_basic_qty in self.pool.get("hotel.room.bed").read(cr, uid, list_ids, ['bed_qty'], context=context):
                bed_qty += list_basic_qty['bed_qty']
            res[obj.id] = bed_qty
        return res

    def _available_stock(self, cr, uid, ids, fieldnames, args, context=None):
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            bed_qty = 0
            list_ids = self.pool.get("hotel.room.bed").search(cr, uid, [('name', '=', obj.id)], context=None)
            for list_basic_qty in self.pool.get("hotel.room.bed").read(cr, uid, list_ids, ['bed_qty'], context=context):
               bed_qty += list_basic_qty['bed_qty']
            res[obj.id] = (obj.total_stock - bed_qty)
        return res

    def _check_avi_total_stock(self, cr, uid, ids, context=None):
        for avi_bed in self.browse(cr, uid, ids):
            total_avi_bed = 0
            list_bed_types = self.pool.get("hotel.room.bed").search(cr, uid, [('name', '=', avi_bed.id)], context=None)
            for list_bed_type_value in self.pool.get("hotel.room.bed").\
                    read(cr, uid, list_bed_types, ['bed_qty'], context=context):
                total_avi_bed += list_bed_type_value['bed_qty']
        if avi_bed.total_stock >= total_avi_bed :
            return True
        else:
            return False

    def _constraints_capacity_nonzero(self, cr, uid, ids, context=None):
        result =True
        for current_rec in self.browse(cr, uid, ids):
            if current_rec.value <= 0:
                result = False
        return result

    _columns = {
        'name': fields.char('Type', size=128, required=True, select=True),
        'value': fields.integer('Capacity',
                                help="1 for Single, 2 for Double. " +
                                     "This will be used for counting available Spaces in a room"),
        'total_stock': fields.integer('Total Stock', help="Total Stock"),
        'available_stock': fields.function(_available_stock, type='integer', string='Available Stock', store=False),
        'used_stock': fields.function(_used_stock, type='integer', string='Used Stock', store=False),
    }
    _sql_constraints = [
        ('name_bed_type_uniq', 'unique(name)', 'The name of the Bed Type must be unique...!'),
    ]
    _constraints = [
        (_check_avi_total_stock, 'Error! Requested Number of Bed Are Not Decreaseble.', ['total_stock']),
        (_constraints_capacity_nonzero, 'Capacity must be greater than zero.', ['Capacity']),
    ]

hotel_bed_type()
