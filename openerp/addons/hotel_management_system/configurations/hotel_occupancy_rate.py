from openerp.osv import fields, osv
import time
from datetime import datetime
from datetime import timedelta  
from openerp.tools.translate import _


class hotel_occ(osv.osv):
    _name = "hotel.occ"
    _description = "Room Occupancy"

    def _get_total_spaces(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        occ = self.browse(cr, uid, ids, context=context)  
        room_obj = self.pool.get('hotel.room')
        room_ids = room_obj.search(cr,uid,[],context=context)
        rooms = room_obj.browse(cr, uid, room_ids, context=context)       
        res = {}
        for o in occ:
            total_space = 0
            for room in rooms: 
                if room.bed_lines:
                    for line in room.bed_lines:               
                        total_space+=(line.bed_qty * line.name.value)
            res[o.id] = total_space
        return res 
         
    def _get_total_baby_spaces(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        
        occ = self.browse(cr, uid, ids, context=context)  
        room_obj = self.pool.get('hotel.room')
        room_ids = room_obj.search(cr,uid,[],context=context)
        rooms = room_obj.browse(cr, uid, room_ids, context=context)       
        res = {}
        for o in occ:
            total_space = 0
            for room in rooms: 
                if room.bed_lines:
                    for line in room.bed_lines:               
                        if line.name.value==0:
                            total_space+=line.bed_qty
            res[o.id] = total_space
        return res 

    
    def _get_total_occupancy(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        occ = self.browse(cr, uid, ids, context=context)  
        room_obj = self.pool.get('hotel.room')
        room_ids = room_obj.search(cr,uid,[],context=context)
        rooms = room_obj.browse(cr, uid, room_ids, context=context) 
        order_obj = self.pool.get('hotel.book.order')
        res = {}
        for o in occ:
            count = 0
            for room in rooms: 
                order_lines = order_obj.search(cr,uid,[('room_id.id','=',room.id)], context=context)
                for lines in order_obj.browse(cr,uid,order_lines,context=context):
                    time_now = time.strftime('%Y-%m-%d %H:%M:%S')
                    if lines.state=="cin" and lines.check_in_date<time_now:
                        count+=1    
            res[o.id] = count
        return res  

    def _get_total_occupancy_rate(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        occ = self.browse(cr, uid, ids, context=context)  
        room_obj = self.pool.get('hotel.room')
        room_ids = room_obj.search(cr,uid,[],context=context)
        rooms = room_obj.browse(cr, uid, room_ids, context=context) 
        order_obj = self.pool.get('hotel.book.order')
        res ={}
        for occup in occ:
            tot = 0.0
            tot_occ = 0.0
            rate = 0.0
            for room in rooms: 
                order_lines = order_obj.search(cr,uid,[('room_id.id','=',room.id)], context=context)
                for lines in order_obj.browse(cr,uid,order_lines,context=context):
                    time_now = time.strftime('%Y-%m-%d %H:%M:%S')
                    if lines.state=="cin" and lines.check_in_date<time_now:
                        tot_occ+=1    
                if room.bed_lines:
                    for line in room.bed_lines:               
                        tot+=(line.bed_qty * line.name.value)
                
            if tot:
                rate = (tot_occ/tot)*100.00
            res[occup.id] = rate
        return res  
    
    
    
    def _get_total_occupancy_lost(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        occ = self.browse(cr, uid, ids, context=context)  
        room_obj = self.pool.get('hotel.room')
        room_ids = room_obj.search(cr, uid, [], context=context)
        rooms = room_obj.browse(cr, uid, room_ids, context=context) 
        res ={}
        for occup in occ:
            tot = 0.0
            tot_occ = 0.0
            rate = 0.0
            for room in rooms: 
                if not room.available:
                    tot_occ += room.total_spaces - room.total_occupancy  
                if room.bed_lines:
                    for line in room.bed_lines:               
                        tot += (line.bed_qty * line.name.value)

            print "tot_occ",tot_occ
            print "tot",tot

            if tot:
                rate = (tot_occ / tot) * 100.00
            res[occup.id] = rate
        return res  

    _columns = {
        'name': fields.char('Name', size=128, select=True),
        'total_spaces': fields.function(_get_total_spaces, string='Total Capacity', type='integer'),
        'total_baby_spaces': fields.function(_get_total_baby_spaces, string='Baby Beds', type='integer'),
        'total_occupancy': fields.function(_get_total_occupancy, string='Total Occupancy', type='integer'),
        'occupancy_rate': fields.function(_get_total_occupancy_rate, string='Occupancy Rate (%)', type='float'),
        'occupancy_lost': fields.function(_get_total_occupancy_lost, string='Occupancy Loss Rate (%)', type='float'),
       
    }
hotel_occ()