from datetime import datetime as dt
from datetime import timedelta as td


time1=[['09:00','10:30'],['12:00','13:00'],['16:05','18:00']]
time2=[['10:00','11:30'],['11:40','14:30'],['14:30','15:00'],['16:05','17:00']]
schedule_1=['09:00','20:00']
schedule_2=['10:00','18:30']
time_slot=30



def format_to_standard_time(string_formatted):
    """
        Format string form date to standard datetime format
    """
    format = '%H:%M'
    actual_time_data = dt.strptime(string_formatted, format)
    return actual_time_data

def subtract_two_times(t1,t2):
    """
        Subtract two string form dates to return gap and duration
    """
    duration = format_to_standard_time(t2) -format_to_standard_time(t1)
    return {'duration': duration, 'gap': [t1,t2]}

def get_schedule_margin_slots_duration(time_slot_list, schedule):
    """
        Check with schedule margins to get free gaps for a person
    """
    margin_gaps = []
    start_gap = subtract_two_times(schedule[0], time_slot_list[0][0])
    end_gap = subtract_two_times( time_slot_list[-1][1],schedule[1])

    if start_gap['duration'] > td(seconds=0):
        margin_gaps.append(start_gap)
    if end_gap['duration'] > td(seconds=0):
        margin_gaps.append(end_gap)
    return margin_gaps

def get_all_gaps_in_within(time_slot_list):
    """
        Check with meeting times to get free gaps for a person apart from schedule gaps
    """
    gap_slots = []
    for i in range(0, len(time_slot_list) - 1):
        gap = subtract_two_times(time_slot_list[i][1], time_slot_list[i+1][0])
        if gap['duration'] > td(seconds=0):
            gap_slots.append(gap)
    return gap_slots

def check_availability_in_time(gap_list, duration):
    """
        Check for eligible gaps from gaplist of free times
    """
    eligible = []
    for gap in gap_list:
        if gap['duration'] >= td(minutes=duration):
            eligible.append(gap)
    return eligible

def check_overlapped_time_gap(start,end):
    """
        Check if overlapped gap is eligible
    """
    gap_time = subtract_two_times(start, end)
    if gap_time['duration'] >= td(minutes=time_slot):
        return gap_time
        

def get_common_eligibility(e1, e2):
    """
        Common free time for both
    """
    available = []
    for eligible_slot1 in e1:
        for eligible_slot2 in e2:
            # Unformatted
            ustart1 = eligible_slot1['gap'][0] 
            uend1 = eligible_slot1['gap'][1] 
            ustart2 = eligible_slot2['gap'][0]
            uend2 = eligible_slot2['gap'][1]
            # formatted
            start1 = format_to_standard_time(ustart1)
            end1 = format_to_standard_time(uend1)
            start2 = format_to_standard_time(ustart2)
            end2 = format_to_standard_time(uend2)

            if (start2>=start1 and start2<end1):
                # slot 2 within slot 1 completely
                if (end2<end1):
                    gap_time = check_overlapped_time_gap(ustart2, uend2)
                    available.append(gap_time)

                # slot 2 overlaps slot 1 to the right
                else:
                    gap_time = check_overlapped_time_gap(ustart2, uend1)
                    available.append(gap_time)

            if (end2<=end1 and end2> start1):
                # slot 2 overlaps slot 1 to the left
                if start2<=start1:
                    gap_time = check_overlapped_time_gap(ustart1, uend2)
                    available.append(gap_time)
            
            # slot 1 within slot 2 completely
            if (start1>start2 and end1<end2):
                gap_time = check_overlapped_time_gap(ustart1, ustart2)
                available.append(gap_time)
            
    return available
    

def get_empty_slots(time1, time2, schedule_1, schedule_2, time_slot):
    gap1, gap2 = [], []

    # Get free times individually
    gap1 += (get_schedule_margin_slots_duration(time1, schedule_1)) 
    gap1 += (get_all_gaps_in_within(time1))
    gap2 += (get_schedule_margin_slots_duration(time2, schedule_2)) 
    gap2 += (get_all_gaps_in_within(time2))
    eligible1 = check_availability_in_time(gap1, time_slot)
    eligible2 = check_availability_in_time(gap2, time_slot)
    # Get common free times
    commonly_available = get_common_eligibility(eligible1, eligible2)
    time_slot_available = []
    # Get free slots
    for av_times in commonly_available:
        no_of_slots = (av_times['duration'] // td(minutes=time_slot))
        start_time_of_gap = av_times['gap'][0]
        for i in range(0, no_of_slots):
            end_time_of_gap_f = format_to_standard_time(start_time_of_gap) + td(minutes=time_slot)
            end_time_of_gap = '{:0>2d}:{:0>2d}'.format(end_time_of_gap_f.hour, end_time_of_gap_f.minute)
            time_slot_available.append({'duration': td(minutes=time_slot), 'gap': [start_time_of_gap, end_time_of_gap]})
            start_time_of_gap = end_time_of_gap
    slots = []       
    for each in time_slot_available:
        slots.append(each['gap']) 
    print(slots)
    return slots

get_empty_slots(time1, time2, schedule_1, schedule_2, time_slot)