from typing import List, Dict
from datetime import timedelta

import xmltodict as xmltodict

from first_distance import FirstDistance
from first_pace import FirstPace
from first_race import FirstRaceType
from first_time import FirstTime


class FirstSegment(object):

    # noinspection PyTypeChecker
    def __init__(self, name: str, distance: FirstDistance =None, duration: FirstTime =None, ref_pace_name: str =None):

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

        self.name = name
        self.distance = distance
        self.duration = duration
        self.ref_pace_name = ref_pace_name

    def get_type(self) -> str:

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

    def __str__(self) -> str:

        out_string = self.name + '  ' + self.get_type()
        if self.distance is not None:
            out_string += '  ' + str(self.distance)
        if self.duration is not None:
            out_string += '  ' + str(self.duration)
        if self.ref_pace_name is not None:
            out_string += '  ' + self.ref_pace_name

        return out_string


class PlanInstructions(object):

    def __init__(self, name: str, race_name: str):

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

    def add_instruction(self, line: str) -> None:

        """

        :param line: workout instructions
        :type line: str
        """
        self.instructions.append(line)


class FirstData(object):

    def __init__(self, xml_path: str):

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

        with open(xml_path, 'r') as fd:
            data_dict = xmltodict.parse(fd.read())['FIRSTdatabase']
            fd.close()

            self.name = data_dict['name']
            self.note = data_dict['note']
            self.__get_rtt(rtt=data_dict['rTT'])
            self.__get_segments(st=data_dict['sT'])
            self.__get_instructions(wis=data_dict['wIs'])

    def __str__(self) -> str:

        return self.name

    def __get_rtt(self, rtt: Dict) -> None:

        self.__get_races(races=rtt['races'])
        self.__get_times(rows=rtt['rows'])

    def __get_races(self, races: Dict) -> None:

        for race in races['race']:
            name = race['name']
            info = race['distance']
            self.race_types.append(FirstRaceType(name=name, distance=float(info['distance']), unit=info['unit']))

    def __get_times(self, rows: Dict) -> None:

        for row in rows['row']:
            times = []
            for col in row['times']['time']:
                times.append(FirstTime(seconds=int(col['seconds']),
                                       minutes=int(col['minutes']), hours=int(col['hours'])))

            self.race_times.append(times)

    def __get_segments(self, st: Dict) -> None:

        index = 0
        segments = st['segments']
        for segment in segments['segment']:
            name = segment['name']
            segment_type = segment['type']

            if segment_type == 'DISTANCE':
                dist_dict = segment['distance']
                distance = FirstDistance(distance=float(dist_dict['distance']), unit=dist_dict['unit'])
                self.segments.append(FirstSegment(name=name, distance=distance))
            elif segment_type == 'TIME':
                time_dict = segment['time']
                duration = FirstTime(seconds=int(time_dict['seconds']),
                                     minutes=int(time_dict['minutes']),
                                     hours=int(time_dict['hours']))
                self.segments.append(FirstSegment(name=name, duration=duration, ref_pace_name=segment['refPaceName']))
            else:  # PACE
                self.segments.append(FirstSegment(name=name, ref_pace_name=segment['refPaceName']))

            self.segments_lookup[name] = index

            index += 1

        self.reference_race = st['refRace']
        pace_unit = st['paceUnit']
        dist_unit = pace_unit.split()[-1]

        for line in st['lines']['string']:
            paces_list = []
            first = True
            index = 0
            for value in line.split():
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
                        paces_list.append(FirstPace.from_string(time_string + ' ' + pace_unit))
                    else:
                        raise ValueError('Duration segments have already a reference pace')

                    index = index + 1

            self.segments_paces.append(paces_list)

    def __get_instructions(self, wis: Dict) -> None:

        for plan_instructions in wis['planInstructions']:
            one_plan = PlanInstructions(name=plan_instructions['name'], race_name=plan_instructions['raceName'])
            for line in plan_instructions['instructions']['string']:
                one_plan.add_instruction(line=line)
            self.plan_instructions.append(one_plan)

    def equivalent_time(self, time_from: FirstTime, race_index_from: int, race_index_to: int) -> FirstTime:

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

        num_races = len(self.race_types)
        if race_index_from < 0 or race_index_from >= num_races:
            raise ValueError('Race index must be between 0 and %1d' % (num_races-1))
        if race_index_to < 0 or race_index_to >= num_races:
            raise ValueError('Race index must be between 0 and %1d' % (num_races-1))
        ten_minutes = timedelta(minutes=10)
        low_time = self.race_times[0][race_index_from] - ten_minutes
        if time_from < low_time:
            raise ValueError('Time is shorter than the lowest database time')

        for row in self.race_times:
            if time_from <= row[race_index_from]:
                return row[race_index_to]

        raise ValueError('Time is longer than the highest database time')

    # noinspection PyTypeChecker
    def race_type_index_by_name(self, name: str) -> int:

        """
        Return the index in the database to the race type name

        :param name: type name
        :type name: str
        :return: the type index in the database
        :rtype: int
        """
        for index in range(len(self.race_types)):
            if self.race_types[index].name == name:
                return index

        raise ValueError('Race type {} not found'.format(name))

    # noinspection PyTypeChecker
    def get_race_type_by_name(self, name: str) -> FirstRaceType:

        """
        Return the race type from the database with this race type name

        :param name: type name
        :type name: str
        :return: the type in the database
        :rtype: FirstRaceType
        """
        for race_type in self.race_types:
            if race_type.name == name:
                return race_type

        raise ValueError('Race type {} not found'.format(name))

    def segment_index_by_name(self, name: str) -> int:

        """
        Performance method - return the segment index in the pace table
        
        :param name: segment name as appears in the instructions
        :type name: str
        :return: the index
        :rtype int
        """

        return self.segments_lookup[name]

    def segment_by_name(self, name: str) -> FirstSegment:

        """
        Performance method - return the segment definition
        
        :param name: segment name as appears in the instructions
        :type name: str
        :return: the segment definition
        :rtype: FirstSegment
        """

        return self.segments[self.segment_index_by_name(name=name)]

    def pace_index_by_race_time(self, race_time: FirstTime, race_name: str) -> int:

        """
        Performance method - return the row index in the pace table
        
        :param race_time: race target time
        :type race_time: FirstTime
        :param race_name: the race name
        :type race_name: str
        :return: the index based on the time
        :rtype: int
        """
        from_race_index = self.race_type_index_by_name(name=race_name)
        to_race_index = self.race_type_index_by_name(name=self.reference_race)
        ref_time = self.equivalent_time(time_from=race_time,
                                        race_index_from=from_race_index, race_index_to=to_race_index)

        for index in range(len(self.segments_paces)):
            if self.segments_paces[index][0] >= ref_time:
                return index

        raise ValueError('Row not found with given time')
