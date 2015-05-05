__author__ = 'Khudrath'
from openerp.osv import fields, osv
import time

class hotel_room(osv.osv):
    _name = "hotel.room"
    _description = "hotel room"


    def _get_total_spaces(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        rooms = self.browse(cr, uid, ids, context=context)
        res = {}
        for room in rooms:
            total_space = 0
            if room.bed_lines:
                for line in room.bed_lines:
                    total_space+=(line.bed_qty * line.name.value)
            res[room.id] = total_space
        return res
    #
    # def _get_total_baby_spaces(self, cr, uid, ids, field_name, arg, context=None):
    #     """
    #     @return: Dictionary of values.
    #     """
    #     rooms = self.browse(cr, uid, ids, context=context)
    #     res = {}
    #     for room in rooms:
    #         total_space = 0
    #         if room.bed_lines:
    #             for line in room.bed_lines:
    #                 if line.name.value==0:
    #                     total_space+=line.bed_qty
    #         res[room.id] = total_space
    #     return res
    #
    # def _get_total_occupancy(self, cr, uid, ids, field_name, arg, context=None):
    #     """
    #     @return: Dictionary of values.
    #     """
    #     rooms = self.browse(cr, uid, ids, context=context)
    #     order_obj = self.pool.get('tarun.hotel.book.order')
    #     res = {}
    #     for room in rooms:
    #         count = 0
    #         order_lines = order_obj.search(cr,uid,[('room_id.id','=',room.id)], context=context)
    #         for lines in order_obj.browse(cr,uid,order_lines,context=context):
    #             time_now = time.strftime('%Y-%m-%d %H:%M:%S')
    #             if lines.state=="cin" and lines.check_in_date<time_now:
    #                 count+=1
    #         res[room.id] = count
    #     return res
    #
    # def _get_total_occupancy_rate(self, cr, uid, ids, field_name, arg, context=None):
    #     """
    #     @return: Dictionary of values.
    #     """
    #     rooms = self.browse(cr, uid, ids, context=context)
    #     res = {}
    #     for room in rooms:
    #         rate = 0.0
    #         try:
    #             rate = float(room.total_occupancy)/float(room.total_spaces)*100.00
    #         except:
    #             rate = 0.0
    #         res[room.id] = rate
    #     return res
    #
    # def _get_availability(self, cr, uid, ids, field_name, arg, context=None):
    #     """
    #     @return: Dictionary of values.
    #     """
    #     rooms = self.browse(cr, uid, ids, context=context)
    #     order_obj = self.pool.get('tarun.hotel.book.order')
    #     res = {}
    #     for room in rooms:
    #         avail = True
    #         total_space = 0
    #         occ_space = 0
    #         if room.bed_lines:
    #             for bed_line in room.bed_lines:
    #                 total_space+=(bed_line.bed_qty * bed_line.name.value)
    #         order_lines = order_obj.search(cr,uid,[('room_id.id','=',room.id)], context=context)
    #         for lines in order_obj.browse(cr,uid,order_lines,context=context):
    #             time_now = time.strftime('%Y-%m-%d %H:%M:%S')
    #             # date less than current time
    #             if lines.state=="cin" and lines.check_in_date<time_now:
    #                 if lines.guest_type.name in ["Family","Sick"]:
    #                     avail = False
    #                     break
    #                 else:
    #                     occ_space+=1
    #         if total_space-occ_space<1:
    #             avail=False
    #
    #         res[room.id] = avail
    #     return res
    #
    # def _get_male_availability(self, cr, uid, ids, field_name, arg, context=None):
    #     """
    #     @return: Dictionary of values.
    #     """
    #     rooms = self.browse(cr, uid, ids, context=context)
    #     order_obj = self.pool.get('tarun.hotel.book.order')
    #     res = {}
    #     for room in rooms:
    #         avail = True
    #         total_space = 0
    #         occ_space = 0
    #         if room.bed_lines:
    #             for bed_line in room.bed_lines:
    #                 total_space+=(bed_line.bed_qty * bed_line.name.value)
    #         order_lines = order_obj.search(cr,uid,[('room_id.id','=',room.id)], context=context)
    #         for lines in order_obj.browse(cr,uid,order_lines,context=context):
    #             time_now = time.strftime('%Y-%m-%d %H:%M:%S')
    #             # date less than current time
    #             if lines.state=="cin" and lines.check_in_date<time_now:
    #                 if lines.guest_type.name in ["Family","Sick","Single"] and lines.gender=="f":
    #                     avail = False
    #                     break
    #                 else:
    #                     occ_space+=1
    #         if total_space-occ_space<1:
    #             avail=False
    #
    #         res[room.id] = avail
    #     return res
    #
    #
    # def _get_family_availability(self, cr, uid, ids, field_name, arg, context=None):
    #     """
    #     @return: Dictionary of values.
    #     """
    #     rooms = self.browse(cr, uid, ids, context=context)
    #     order_obj = self.pool.get('tarun.hotel.book.order')
    #     res = {}
    #     for room in rooms:
    #         avail = False
    #         total_space = 0
    #         occ_space = 0
    #         if room.bed_lines:
    #             for bed_line in room.bed_lines:
    #                 total_space+=(bed_line.bed_qty * bed_line.name.value)
    #
    #
    #         order_lines = order_obj.search(cr,uid,[('room_id.id','=',room.id)], context=context)
    #         for lines in order_obj.browse(cr,uid,order_lines,context=context):
    #             time_now = time.strftime('%Y-%m-%d %H:%M:%S')
    #             # date less than current time
    #             if lines.state=="cin" and lines.check_in_date<time_now:
    #                 if lines.guest_type.name in ["Family"]:
    #                     avail = True
    #                     occ_space+=1
    #         if total_space-occ_space<1:
    #             avail=False
    #
    #         res[room.id] = avail
    #     return res
    #
    def _compute_lines(self, cr, uid, ids, name, args, context=None):
        result = {}
        order_obj=self.pool.get('hotel.book.order')
        for room in self.browse(cr, uid, ids, context=context):
            orders = []
            orders = order_obj.search(cr,uid, [['state', '=', 'cin'], ['room_id_view', 'ilike', room.name]], context=context)
            result[room.id] = orders
        return result



    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'type_id': fields.many2one('hotel.room.type', 'Room Type', required=True, select=True),
        'total_spaces': fields.function(_get_total_spaces, string='Total Capacity', type='integer'),
        # 'total_baby_spaces': fields.function(_get_total_baby_spaces, string='Baby Beds', type='integer'),
        'bed_lines': fields.one2many('hotel.room.bed', 'room_id', 'Beds'),
        # 'total_occupancy': fields.function(_get_total_occupancy, string='Total Occupancy', type='integer'),
        # 'occupancy_rate': fields.function(_get_total_occupancy_rate, string='Occupancy Rate', type='float'),
        # 'available': fields.function(_get_availability, string='Available', type='boolean', help="A Room will be show Available if it has no Sick or Family Type Guest and has space available"),
        # 'male_available': fields.function(_get_male_availability, string='Male Check', type='boolean'),
        # 'family_available': fields.function(_get_family_availability, string='Family Check', type='boolean'),
        # 'cur_order' : fields.function(_compute_lines, relation='hotel.book.order', type="many2many", string='Current Reservations'),
    }
    _sql_constraints = [
        ('name_room_uniq', 'unique(name)', 'The name of the Room must be unique...!'),
    ]

    # def name_get(self, cr, uid, ids, context=None):
    #     if context is None:
    #         context = {}
    #     if isinstance(ids, (int, long)):
    #         ids = [ids]
    #     res = []
    #     for record in self.browse(cr, uid, ids, context=context):
    #         av_space=0
    #         av_space = record.total_spaces-record.total_occupancy
    #         name = record.name+" ("+str(av_space)+")"
    #         res.append((record.id, name))
    #     return res


hotel_room()

