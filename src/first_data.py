import xml.etree.ElementTree as ET
from datetime import timedelta

from first_distance import FirstDistance
from first_pace import FirstPace
from first_race import FirstRaceType
from first_time import FirstTime


class FirstData(object):

    def __init__(self, xml_path):

        """
        Constructor

        :param xml_path: path to xml database
        :type xml_path: str
        :return: instance of FirstData
        :rtype: FirstData
        """

        self.race_types = []
        self.race_times = []
        self.segments = []
        self.segments_lookup = {}
        self.reference_race = None
        self.segments_paces = []
        self.plan_instructions = []

        root = ET.parse(source=xml_path).getroot()

        for child in root:

            if child.tag == 'name':
                self.name = child.text
            elif child.tag == 'note':
                self.note = child.text
            elif child.tag == 'rTT':
                self.__parse_races(races=child[0])
                self.__parse_rows(rows=child[1])
            elif child.tag == 'sT':
                self.__parse_segments(segment_def=child[0], ref_race=child[1],
                                      pace_unit=child[2], segment_paces=child[3])
            elif child.tag == 'wIs':
                self.__parse_plan_instructions(plan_instructions=child)

    def __str__(self):

        return self.name

    def __parse_races(self, races):

        for race in races:
            name = race[0].text
            dist = float(race[1][0].text)
            unit = race[1][1].text
            self.race_types.append(FirstRaceType(name=name, distance=dist, unit=unit))

    def __parse_rows(self, rows):

        for row in rows:
            times = []
            for col in row[0]:
                seconds = int(col[0].text)
                minutes = int(col[1].text)
                hours = int(col[2].text)
                times.append(FirstTime(seconds=seconds, minutes=minutes, hours=hours))

            self.race_times.append(times)

    def __parse_segments(self, segment_def, ref_race, pace_unit, segment_paces):

        where_am_i = 'FirstData.__parse_segments'
        index = 0
        for segment in segment_def:
            name = segment[0].text
            segment_type = segment[1].text
            distance = None
            duration = None
            ref_pace_name = None
            if segment_type == 'DISTANCE':
                distance = FirstDistance(distance=float(segment[2][0].text), unit=segment[2][1].text)
            elif segment_type == 'TIME':
                duration = FirstTime(seconds=int(segment[2][0].text),
                                     minutes=int(segment[2][1].text),
                                     hours=int(segment[2][2].text))
                ref_pace_name = segment[3].text
            else:  # PACE
                ref_pace_name = segment[2].text

            self.segments.append(FirstSegment(name=name, distance=distance,
                                              duration=duration, ref_pace_name=ref_pace_name))
            self.segments_lookup[name] = index
            index += 1

        self.reference_race = ref_race.text
        dist_unit = pace_unit.text.split()[-1]

        for line in segment_paces:
            paces_list = []
            first = True
            index = 0
            for value in line.text.split():
                if first:
                    paces_list.append(FirstTime.from_string(value))
                    first = False
                else:
                    # why incrementing index makes ref_segment.get_type undefined?
                    time_string = '0:' + value
                    ref_segment = self.segments[index]
                    if ref_segment.get_type() == 'distance':
                        cur_time = FirstTime.from_string(time_string)
                        cur_dist = ref_segment.distance
                        paces_list.append(FirstPace.from_time_distance(time=cur_time, distance=cur_dist,
                                                                       unit=dist_unit))
                    elif ref_segment.get_type() == 'pace':
                        paces_list.append(FirstPace.from_string(time_string + ' ' + pace_unit.text))
                    else:
                        raise ValueError(where_am_i + ' - Duration segments have already a reference pace')

                    index = index + 1

            self.segments_paces.append(paces_list)

    def __parse_plan_instructions(self, plan_instructions):

        for plan_inst in plan_instructions:
            one_plan = PlanInstructions(name=plan_inst[0].text, race_name=plan_inst[1].text)
            for line in plan_inst[2]:
                one_plan.add_instruction(line.text)
            self.plan_instructions.append(one_plan)

    def equivalent_time(self, time_from, race_index_from, race_index_to):

        """
        Find equivalent time for another race. E.G. if you ran 5K in 0:20:13, set your half marathon target
        time to 1:34:15.
        
        :param time_from: 
        :type time_from: FirstTime
        :param race_index_from: 
        :type race_index_from: int
        :param race_index_to: 
        :type race_index_to: int
        :return: equivalent time
        :rtype: FirstTime
        """

        where_am_i = 'FirstData.equivalent_time'
        if not isinstance(time_from, FirstTime):
            raise TypeError(where_am_i + ' - time_from must be an instance of FirstTime')
        if not isinstance(race_index_from, int):
            raise TypeError(where_am_i + ' - race_index_from must be an int')
        if not isinstance(race_index_to, int):
            raise TypeError(where_am_i + ' - race_index_to must be an int')
        num_races = len(self.race_types)
        if race_index_from < 0 or race_index_from >= num_races:
            raise ValueError(where_am_i + ' - race index must be between 0 and %1d' % (num_races-1))
        if race_index_to < 0 or race_index_to >= num_races:
            raise ValueError(where_am_i + ' - race index must be between 0 and %1d' % (num_races-1))
        ten_minutes = timedelta(minutes=10)
        low_time = self.race_times[0][race_index_from] - ten_minutes
        if time_from < low_time:
            raise ValueError(where_am_i + ' - time is shorter than the lowest database time')

        for row in self.race_times:
            if time_from <= row[race_index_from]:
                return row[race_index_to]

        raise ValueError(where_am_i + ' - time is longer than the highest database time')

    # noinspection PyTypeChecker
    def race_type_index_by_name(self, name):

        """
        Return the index in the database to the race type name

        :param name: type name
        :type name: str
        :return: the type index in the database
        :rtype: int
        """
        where_am_i = 'FirstSegment.race_type_index_by_name'
        if not isinstance(name, basestring):
            raise TypeError(where_am_i + ' - name is expected to be a string')
        for index in range(len(self.race_types)):
            if self.race_types[index].name == name:
                return index

        raise ValueError(where_am_i + ' - Race type %1s not found' % name)

    # noinspection PyTypeChecker
    def get_race_type_by_name(self, name):

        """
        Return the race type from the database with this race type name

        :param name: type name
        :type name: str
        :return: the type in the database
        :rtype: FirstRaceType
        """
        where_am_i = 'FirstSegment.get_race_type_by_name'
        if not isinstance(name, basestring):
            raise TypeError(where_am_i + ' - name is expected to be a string')
        for race_type in self.race_types:
            if race_type.name == name:
                return race_type

        raise ValueError(where_am_i + ' - Race type %1s not found' % name)

    def segment_index_by_name(self, name):

        """
        Performance method - return the segment index in the pace table
        
        :param name: segment name as appears in the instructions
        :type name: str
        :return: the index
        :rtype int
        """

        return self.segments_lookup[name]

    def segment_by_name(self, name):

        """
        Performance method - return the segment definition
        
        :param name: segment name as appears in the instructions
        :type name: str
        :return: the segment definition
        :rtype: FirstSegment
        """

        return self.segments[self.segment_index_by_name(name)]

    def pace_index_by_race_time(self, race_time, race_name):

        """
        Performance method - return the row index in the pace table
        
        :param race_time: race target time
        :type race_time: FirstTime
        :param race_name: the race name
        :type race_name: str
        :return: the index based on the time
        :rtype: int
        """
        where_am_i = 'FirstData.Paces.pace_index_by_race_time'
        from_race_index = self.race_type_index_by_name(race_name)
        to_race_index = self.race_type_index_by_name(self.reference_race)
        ref_time = self.equivalent_time(time_from=race_time,
                                        race_index_from=from_race_index, race_index_to=to_race_index)

        for index in range(len(self.segments_paces)):
            if self.segments_paces[index][0] >= ref_time:
                return index

        raise ValueError(where_am_i + ' - row not found with given time')


class FirstSegment(object):

    # noinspection PyTypeChecker
    def __init__(self, name, distance=None, duration=None, ref_pace_name=None):

        """
        Constructor

        :param name: segment name
        :type name: str
        :param distance: segment distance
        :type distance: FirstDistance
        :param duration: segment time duration
        :type duration: FirstTime
        :param ref_pace_name: reference pace name
        :type ref_pace_name: str
        :return instance of FirstSegment
        :rtype: FirstSegment
        """
        where_am_i = 'FirstSegment.__init__'
        if not isinstance(name, basestring):
            raise TypeError(where_am_i + ' - name must be a string')
        if distance is not None and not isinstance(distance, FirstDistance):
            raise TypeError(where_am_i + ' - distance must be an instance of FirstDistance')
        if duration is not None and not isinstance(duration, FirstTime):
            raise TypeError(where_am_i + ' - duration must be an instance of FirstTime')
        if ref_pace_name is not None and not isinstance(ref_pace_name, basestring):
            raise TypeError(where_am_i + ' - ref_pace_name must be a string')

        self.name = name
        self.distance = distance
        self.duration = duration
        self.ref_pace_name = ref_pace_name

    def get_type(self):

        """
        Get segment type

        :return: distance, time, or pace
        :rtype: str
        """
        if self.distance is not None:
            return 'distance'
        elif self.duration is not None:
            return 'time'
        else:
            return 'pace'

    def __str__(self):

        out_string = self.name + '  ' + self.get_type()
        if self.distance is not None:
            out_string += '  ' + str(self.distance)
        if self.duration is not None:
            out_string += '  ' + str(self.duration)
        if self.ref_pace_name is not None:
            out_string += '  ' + self.ref_pace_name

        return out_string


class PlanInstructions(object):

    def __init__(self, name, race_name):

        """
        Constructor
        
        :param name: plan name
        :type name: str
        :param race_name: reference race name
        :type race_name: str
        return: instance of PlanInstructions
        :rtype: PlanInstructions
        """
        self.name = name
        self.race_name = race_name
        self.instructions = []

    def add_instruction(self, line):

        """

        :param line: workout instructions
        :type line: str
        """
        self.instructions.append(line)
