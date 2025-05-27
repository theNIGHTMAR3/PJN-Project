#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:50:09 2024

@author: Jan Daciuk
"""
import time as ct
from datetime import time, datetime
import regex


class Task_Manager():
    def __init__(self):
        self.stops = ["Brzeźno Dom Zdrojowy",  # 0
                      "Dworzec Główny",  # 1
                      "Jasień PKM",  # 2
                      "Jaworzniaków",  # 3
                      "Jelitkowo",  # 4
                      "Kiełpino Górne",  # 5
                      "Lawendowe Wzgórze",  # 6
                      "Łostowice-Świętokrzyska",  # 7
                      "Miszewskiego",  # 8
                      "Nowy Port Oliwska",  # 9
                      "Oliwa",  # 10
                      "Oliwa PKP",  # 11
                      "Opera Bałtycka",  # 12
                      "Orunia Górna",  # 13
                      "Siedlicka",  # 14
                      "Sobótki",  # 15
                      "Stogi Plaża",  # 16
                      "Strzyża PKM",  # 17
                      "Ujeścisko",  # 18
                      "Wały Piastowskie",  # 19
                      "Wrzeszcz PKP",  # 20
                      "Zajezdnia",  # 21
                      "Zaspa"]  # 22
        self.stopsGen = ["Brzeźna Domu Zdrojowego",
                         "Dworca Głównego",
                         "Jasienia PKP",
                         "Jaworzniaków",
                         "Jelitkowa",
                         "Kiełpina Górnego",
                         "Lawendowego Wzgórza",
                         "Łostowic-Świętokrzyskiej",
                         "Miszewskiego",
                         "Nowego Portu Oliwskiej",
                         "Oliwy",
                         "Oliwy PKP",
                         "Opery Bałtyckiej",
                         "Oruni Górnej",
                         "Siedlickiej",
                         "Sobótki",
                         "Stogów Plaży",
                         "Strzyży PKM",
                         "Ujeściska",
                         "Wałów Piastowskich",
                         "Wrzeszcza PKP",
                         "Zajezdni",
                         "Zaspy"]
        self.lines = [2, 3, 4, 5, 6, 9, 11, 12, 127, 162, 168, 199, 262]
        self.routes = [[[6, 18, 1, 12, 22, 4], [4, 22, 12, 1, 18, 6]],  # 2
                       [[7, 1, 12, 0], [0, 12, 1, 7]],  # 3
                       [[6, 18, 12, 22, 4], [4, 22, 12, 18, 6]],  # 4
                       [[10, 17, 8, 0, 9], [9, 0, 8, 17, 10]],  # 5
                       [[7, 1, 12, 8, 17, 10, 4],
                        [4, 10, 17, 8, 12, 1, 7]],  # 6
                       [[16, 1, 12, 8, 17], [17, 8, 12, 1, 16]],  # 9
                       [[6, 18, 1, 12, 8, 17], [17, 8, 12, 1, 18, 6]],  # 11
                       [[18, 1, 12, 8, 17, 10, 22],
                        [22, 10, 17, 8, 12, 1, 10]],  # 12
                       [[2, 15, 11], [11, 15, 2]],  # 127
                       [[13, 7, 15, 20], [20, 15, 7, 13]],  # 162
                       [[20, 14, 5], [5, 14, 20]],  # 168
                       [[19, 1, 14, 20, 11], [11, 20, 14, 1, 19]],  # 199
                       [[3, 7, 15, 20], [20, 15, 7, 3]]]  # 262
        self.schedules = [[  # line 2
                           [  # 6 -> 4
                            ["4:38", "4:39", "5:02", "5:11", "5:26", "5:38"],
                            ["5:08", "5:09", "5:32", "5:41", "5:56", "6:08"],
                            ["5:38", "5:39", "6:02", "6:11", "6:26", "6:38"]],
                           [  # 4 -> 6
                            ["5:44", "5:56", "6:12", "6:18", "6:41", "6:42"],
                            ["6;14", "6:26", "6:42", "6:48", "7:11", "7:12"],
                            ["6:44", "6:56", "7;12", "7;18", "7:41", "7:42"]]],
                          [  # line 3
                           [  # 7 -> 0
                            ["21:49", "22:08", "22:19", "22:37"],
                            ["22:19", "22:40", "22:48", "23:05"],
                            ["22:49", "23:08", "23:16", "23:33"]],
                           [  # 0 -> 7
                            ["5:14", "5:31", "5:37", "5:59"],
                            ["11:04", "11:21", "11:27", "11:49"],
                            ["12:04", "12:21", "12:27", "12:49"]]],
                          [  # line 4
                           [  # 6 -> 4
                            ["9:19", "9:20", "9:51", "10:06", "10:18"],
                            ["9:59", "10:00", "10:31", "10:46", "10:58"],
                            ["10:39", "10:40", "11:11", "11:26", "11:38"]],
                           [  # 4 -> 6
                            ["10:50", "11:02", "11:18", "11:47", "11:48"],
                            ["11:30", "11:42", "11:58", "12:27", "12:28"],
                            ["12:10", "12:22", "12:38", "13:07", "13:08"]]],
                          [  # line 5
                           [  # 10 -> 9
                            ["12:14", "12:22", "12:34", "12:54", "13:04"],
                            ["12:34", "12:42", "12:54", "13:14", "13:24"],
                            ["12:54", "13:02", "13:14", "13:34", "13:44"]],
                           [  # 9 -> 10
                            ["14:05", "14:12", "14:31", "14:41", "14:49"],
                            ["14:25", "14:32", "14:51", "15:01", "15:09"],
                            ["14:45", "14:52", "15:11", "15:21", "15:29"]]],
                          [  # line 6
                           [  # 7 -> 4
                            ["15:02", "15:23", "15:32", "15:35", "15:45",
                             "15:54", "16:03"],
                            ["15:22", "15:43", "15:52", "15:55", "16:05",
                             "16:14", "16:23"],
                            ["15:42", "16:03", "16:12", "16:15", "16:25",
                             "16:34", "16:43"]],
                           [  # 4 -> 7
                            ["16:57", "17:09", "17:17", "17:29", "17:32",
                             "17:38", "18:00"],
                            ["17:17", "17:29", "17:37", "17:49", "17:52",
                             "17:58", "18:20"]]],
                          [  # line 9
                           [  # 16 -> 17
                            ["17:12", "17:37", "17:46", "17:49", "17:59"],
                            ["17:32", "17:57", "18:06", "18:09", "18:19"],
                            ["17:52", "18:17", "18:26", "18:29", "18:39"]],
                           [  # 17 -> 16
                            ["18:01", "18:12", "18:15", "18:21", "18:47"],
                            ["18:21", "18:32", "18:35", "18:41", "19:07"],
                            ["18:41", "18:52", "18:55", "19:01", "19:27"]]],
                          [  # line 11
                           [  # 6 -> 17
                            ["14:16", "14:17", "14:40", "14:49", "14:52",
                             "15:02"],
                            ["14:26", "14:27", "14:50", "14:59", "15:02",
                             "15:12"],
                            ["14:36", "14:37", "15:00", "15:09", "15:12",
                             "15:22"]],
                           [  # 17 -> 6
                            ["7:13", "7:24", "7:27", "7:33", "7:56",
                             "7:57"],
                            ["15:03", "15:14", "15:17", "15:23", "15:46",
                             "15:47"]]],
                          [  # line 12
                           [  # 18 -> 22
                            ["15:03", "15:30", "15:39", "15:42", "15:52",
                             "16:01", "16:15"],
                            ["15:23", "15:50", "15:59", "16:02", "16:12",
                             "16:21", "16:35"],
                            ["15:43", "16:10", "16;19", "16:22", "16:32",
                             "16:41", "16:55"]],
                           [  # 22 -> 18
                            ["10:06", "10:22", "10:30", "10:42", "10:45",
                             "10:51", "11:20"],
                            ["10:26", "10:42", "10:50", "11:02", "11:05",
                             "11:11", "11:40"],
                            ["10:46", "11:02", "11:10", "11:22", "11:25",
                             "11:31", "12:00"]]],
                          [  # 127
                           [  # 2 -> 11
                            ["9:12", "9:30", "9:58"],
                            ["9:42", "10:00", "10:29"],
                            ["10:12", "10:31", "11:00"]],
                           [  # 11 -> 2
                            ["13:00", "13:30", "13:48"],
                            ["13:20", "13:50", "14:08"],
                            ["13:40", "14:10", "14:28"]]],
                          [  # 162
                           [  # 13 -> 20
                            ["12:17", "12:21", "12:43", "12:50"],
                            ["12:37", "12:41", "13:03", "13:10"],
                            ["12:57", "13:01", "13:23", "13:30"]],
                           [  # 20 -> 13
                            ["13:17", "13:20", "13:38", "13:45"],
                            ["13:37", "13:40", "13:58", "14:05"],
                            ["13:57", "14:00", "14:18", "14:25"]]],
                          [  # line 168
                           [  # 20 -> 5
                            ["14:06", "14:44", "14:50"],
                            ["14:34", "15:12", "15:18"],
                            ["15:06", "15:44", "15:50"]],
                           [  # 5 -> 20
                            ["15:18", "15:23", "16:01"],
                            ["15:43", "15:49", "16:26"],
                            ["16:18", "16:24", "17:01"]]],
                          [  # line 199
                           [  # 19 -> 11
                            ["15:00", "15:02", "15:21", "15:28", "15:53"],
                            ["15:21", "15:23", "15:42", "15:48", "16:13"],
                            ["15:41", "15:43", "16:02", "16:08", "16:33"]],
                           [  # 11 -> 19
                            ["15:12", "15:40", "15:45", "16:08", "16:09"],
                            ["15:32", "16:00", "16:06", "16:28", "16:29"],
                            ["15:52", "16:20", "16:26", "16:48", "16:49"]]],
                          [  # line 262
                           [  # 3 -> 20
                            ["17:03", "17:11", "17:32", "17:39"],
                            ["17:23", "17:31", "17:52", "17:59"],
                            ["17:43", "17:51", "18:12", "18:19"]],
                           [  # 20 -> 3
                            ["16:07", "16:10", "16:29", "16:37"],
                            ["16:27", "16:30", "16:49", "16:57"],
                            ["16:47", "16:50", "17:09", "17;17"]]]]
        self.stop_in_lines = {}
        for pt_stop in range(len(self.stops)):
            self.stop_in_lines[pt_stop] = []
        for pt_line in range(len(self.lines)):
            # pt_line is the line index, not line number.
            for d in range(2):
                for st_n in range(len(self.routes[pt_line][d])):
                    x = [pt_line, d, st_n]
                    self.stop_in_lines[self.routes[pt_line][d][st_n]].append(x)
        self.stops_nom_dict = {}
        self.stops_gen_dict = {}
        for dict_case in [[self.stops, self.stops_nom_dict],
                          [self.stopsGen, self.stops_gen_dict]]:
            dcl, dcd = dict_case
            for stop_number, stop_name in enumerate(dcl):
                stop_name_seq = regex.split(r"\W", stop_name.lower())
                current_dict = dcd
                snsl = len(stop_name_seq)
                for snsn in range(snsl):
                    sns = stop_name_seq[snsn]
                    if sns not in current_dict:
                        current_dict[sns] = {}
                    current_dict = current_dict[sns]
                current_dict["#"] = stop_number

    def stop_name(self, stop_number):
        return self.stops[stop_number]

    def stop_number(self, stop_name):
        return self.stops.index(stop_name)

    def conn_from(self, from_stop, to_stop, dept_after_time):
        """
        Return a connection from from_stop to to_stop after dept_after_time.

        Parameters
        ----------
        from_stop : int
            Stop number (not name) of the departure.
        to_stop : int
            Stop number (not name) of the arrival.
        dept_after_time : str
            Departure should be after that time in hh:mm format.

        Returns
        -------
        list(int, int, str, str)
            A list containing:
                line number (not index),
                destination stop number,
                departure time,
                arrival time.

        """
        h1, m1 = dept_after_time.split(":")
        dat = time(hour=int(h1), minute=int(m1))
        res_list = []
        for lds in self.stop_in_lines[from_stop]:
            pt_line, d, st_n = lds  # pt_line is line index, not line number
            try:
                tsn = self.routes[pt_line][d].index(to_stop, st_n + 1)
                # There is a connection from from_stop to to_stop.
                # Check the schedule for the line.
                for cruise in self.schedules[pt_line][d]:
                    h2, m2 = cruise[st_n].split(":")
                    if time(hour=int(h2), minute=int(m2)) >= dat:
                        # There is a cruise with required departure time
                        cruise_details = [pt_line,  # line index
                                          self.routes[pt_line][d][-1],  # dest
                                          cruise[st_n],  # departure time
                                          cruise[tsn]]   # arrival time
                        res_list.append(cruise_details)
            except (IndexError, ValueError):
                tsn = -1
        if res_list != []:
            return min(res_list, key=lambda x: x[3])
        else:
            return []

    def conn_line_from(self, from_stop, to_stop, line_idx, dept_after_time):
        h1, m1 = dept_after_time.split(":")
        dat = time(hour=int(h1), minute=int(m1))
        res_list = []
        for d1 in range(2):  # direction
            if (from_stop in self.routes[line_idx][d1] and
                    to_stop in self.routes[line_idx][d1]):
                st_n = self.routes[line_idx][d1].index(from_stop)
                tsn = self.routes[line_idx][d1].index(to_stop)
                if tsn > st_n:
                    for cruise in self.schedules[line_idx][d1]:
                        h2, m2 = cruise[st_n].split(":")
                        if time(hour=int(h2), minute=int(m2)) >= dat:
                            cruise_dets = [line_idx,  # line index
                                           # destination stop number
                                           self.routes[line_idx][d1][-1],
                                           cruise[st_n],  # departure time
                                           cruise[tsn]]  # arrival time
                            res_list.append(cruise_dets)
        if res_list != []:
            return min(res_list, keys=lambda x: x[3])
        else:
            return []

    def conn_to(self, from_stop, to_stop, arr_before_time):
        h1, m1 = arr_before_time.split(":")
        dat = time(hour=int(h1), minute=int(m1))
        res_list = []
        for lds in self.stop_in_lines[to_stop]:
            pt_line, d, st_n = lds  # pt_line is line index, not line number
            try:
                tsn = self.routes[pt_line][d].index(to_stop, 0, st_n)
                # There is a connection from from_stop to to_stop.
                # Check the schedule for the line.
                for cruise in self.schedules[pt_line][d]:
                    h2, m2 = cruise[st_n].split(":")
                    if time(hour=int(h2), minute=int(m2)) <= dat:
                        # There is a cruise with the required arrival time
                        cruise_details = [pt_line,  # line index
                                          self.routes[pt_line][d][-1],  # dest
                                          cruise[tsn],    # departure time
                                          cruise[st_n]]   # arrival time
                        res_list.append(cruise_details)
            except (IndexError, ValueError):
                tsn = -1
        if res_list != []:
            return max(res_list, key=lambda x: x[2])
        else:
            return []

    def stop_name_nom_to_number(self, sequence, seq_index, seq_len):
        current_dict = self.stops_nom_dict
        while seq_index < seq_len:
            word = sequence[seq_index].lower()
            if word in current_dict:
                current_dict = current_dict[word]
            else:
                break
            seq_index += 1
        if '#' in current_dict:
            return [seq_index + 1, current_dict['#']]
        else:
            return [-1, -1]

    def stop_name_gen_to_number(self, sequence, seq_index, seq_len):
        current_dict = self.stops_gen_dict
        current_index = seq_index
        while current_index < seq_len:
            word = sequence[current_index].lower()
            if word in current_dict:
                current_dict = current_dict[word]
            else:
                break
            current_index += 1
        if '#' in current_dict:
            return [current_index, current_dict['#']]
        else:
            return [-1, -1]

    def time_to_time(self, sequence, seq_index, seq_len):
        if regex.match(r"\d{1,2}:\d{2}", sequence[seq_index]):
            x = sequence[seq_index].split(":")
            if x[0] < 23 and x[1] < 60:
                y = sequence[seq_index]
                return [seq_index + 1, y]

    def line_to_index(self, sequence, seq_index, seq_len):
        try:
            l_no = int(sequence[seq_index])
            return [seq_index + 1, self.lines.index(l_no)]
        except ValueError:
            return [-1, -1]

    def vehicle_type(self, line_number):
        """
        Return either a bus or a tramway depending on line number.

        Parameters
        ----------
        line_number : int
            Line number (not index).

        Returns
        -------
        str
            Vehicle type.

        """
        if line_number >= 100:
            return "autobus"
        else:
            return "tramwaj"

    def get_predef_dict(self):
        predef_dict = {"przystanekM": self.stop_name_nom_to_number,
                       "przystanekD": self.stop_name_gen_to_number,
                       "czas": self.time_to_time,
                       "numer": self.line_to_index}
        return predef_dict

    def get_defaults(self):
        defaults = {"linia": "dowolna", "czas": "teraz"}
        return defaults

    def exec_query(self, query_data):
        if query_data["type"] == "pyt_odj":
            from_stop = query_data["z_przystanku"]
            to_stop = query_data["do_przystanku"]
            if "czas" in query_data:
                czas = query_data["czas"]
            else:
                czas = "teraz"
            if czas == "teraz":
                now = datetime.now()
                dept_after_time = now.strftime("%H:%M")
            else:
                dept_after_time = czas
            if query_data["linia"] == "dowolna":
                res = self.conn_from(from_stop, to_stop, dept_after_time)
            else:
                line_idx = int(query_data["linia"])
                res = self.conn_line_from(from_stop, to_stop, line_idx,
                                          dept_after_time)
            if res != []:
                result = {"from_stop": self.stops[from_stop],
                          "to_stop": self.stops[to_stop],
                          "line": self.lines[res[0]],
                          "destination": self.stopsGen[res[1]],
                          "dept_time": res[2],
                          "arr_time": res[3]}
            else:
                result = {}
            return result

# Linie:
    # 168 Wrzeszcz PKP - Kiełpino Górne
    # 199 Wały Piastowskie - Oliwa PKP
    # 127 Jasień PKM - Oliwa PKP
    # 162 Orunia Górna - Wrzeszcz PKP
    # 262 Jaworzniaków - Wrzeszcz PKP
    # 2 Jelitkowo - Lawendowe Wzgórze
    # 3 Łostowice-Świętokrzyska - Brzeźno Dom Zdrojowy
    # 4 Lawendowe Wzgórze - Jelitkowo
    # 5 Oliwa - Nowy Port Oliwska
    # 6 Łostowice-Świętokrzyska - Jelitkowo
    # 9 Strzyża PKM - Stogi Plaża
    # 11 Strzyża PKM - Lawendowe Wzgorze, Lawendowe Wzgórze - Zajezdnia
    # 12 Ujeścisko - Zaspa
# Przystanki:
    # Siedlicka
    # Sobótki
    # Miszewskiego
    # Opera
    # Dworzec Główny


if __name__ == "__main__":
    tm = Task_Manager()
    from_stop = tm.stop_number(input("Check connection from stop: "))
    to_stop = tm.stop_number(input("  to stop: "))
    after_time = input("  departure after time: ")
    ln, dr, dt, at = tm.conn_from(from_stop, to_stop, after_time)
    print(f"Line {ln} dest {tm.stop_name(dr)} at {dt} ", end="")
    print(f"from {tm.stop_name(from_stop)} to {tm.stop_name(to_stop)} at {at}")
