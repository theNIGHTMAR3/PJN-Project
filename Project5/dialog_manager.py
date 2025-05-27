#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 11 19:33:10 2024

@author: jandac
"""
import regex
import json
from dialog_editor import Phrases
from task_manager import Task_Manager


Tm = Task_Manager()
Ph = Phrases(Tm.get_predef_dict().keys())


def tokenize(sentence):
    ts = regex.split(r"\W+", sentence)
    if ts[-1] == "":
        ts.pop()
    return ts


def recognize_phrase_tail(ph, node, sentence, start_index):
    local_result = {}
    next_index = start_index + 1
    if ph.is_phrase_def(node):
        # This should never happen
        raise BaseException("Error in dialogue: Link to a phrase definition!")
    elif ph.is_phrase_ref(node):
        ref_node = ph.get_definition_node(ph.get_node_text(node))
        local_result = recognize_whole_phrase(ph, ref_node, sentence,
                                              start_index)
        if local_result[0]:
            # Subphrase recognized
            next_index = local_result[1]
            local_result = local_result[2]
        else:
            return [False]
    elif ph.is_end(node):
        return [True, next_index, {}]
    elif ph.is_predef(node):
        method = Tm.get_predef_dict()[ph.get_node_text(node)]
        local_result = method(sentence, start_index, len(sentence))
        if local_result[0] != -1:
            next_index = local_result[0]
            # Integrate the result
            local_result = {"!": local_result[1]}
        else:
            return [False]
    else:
        # This is a word node
        if ph.get_node_text(node).lower() != sentence[start_index].lower():
            return [False]
    # If we got here, we have recognized the current node
    # Recognize the rest of the phrase
    if next_index < len(sentence):
        for next_node in ph.get_links(node):
            if ph.is_end(next_node):
                continue  # Be greedy
            res = recognize_phrase_tail(ph, next_node, sentence, next_index)
            if res[0]:
                # Integrate the results
                next_index = res[1]
                for k1 in res[2].keys():
                    local_result[k1] = res[2][k1]
                return [True, next_index, local_result]
    for next_node in ph.get_links(node):
        if ph.is_end(next_node):
            return [True, next_index, local_result]
    return [False]


def recognize_whole_phrase(ph, phrase_node, sentence, start_index=0):
    if start_index >= len(sentence):
        return [False]
    result = {}
    if ph.is_phrase_def(phrase_node):
        for next_node in ph.get_links(phrase_node):
            if ph.is_end(next_node):
                continue  # Be greedy
            res = recognize_phrase_tail(ph, next_node, sentence, start_index)
            if res[0]:
                next_index = res[1]
                if ph.get_node_sem(phrase_node) != "":
                    result[ph.get_node_sem(phrase_node)] = res[2]
                else:
                    result = res[2]
                return [True, next_index, result]
        for next_node in ph.get_links(phrase_node):
            if ph.is_end(next_node):
                return [True, start_index, result]
    return [False]


class Dialog_Manager():
    def __init__(self, defaults):
        self.dialog_state = {}
        self.defaults = defaults
        self.dialog_state["last query"] = {}
        self.dialog_state["previous query"] = {}
        self.dialog_state["last result"] = {}
        self.dialog_state["aux query"] = {}
        self.initial_phrases = [
            Ph.get_definition_node("pyt_odj"),
            Ph.get_definition_node("pyt_dojazd_cel"),
            Ph.get_definition_node("pyt_nastepny")
            ]
        self.verbosity_level = 0
        self.error_message = [
            "Nie rozumiem. Proszę inaczej sformułować pytanie.\n",
            "Nie rozumiem. Proszę zapytać np. o odjazd autobusu z " +
            "danego przystanku.\n",
            'Nie rozumiem. Można zapytać np. „Kiedy odjeżdża tramwaj ' +
            'z Dworca Głównego do Opery Bałtyckiej".\n']
        self.completion_data = {
            "z_przystanku": {
                "question": "Z którego przystanku ma nastąpić odjazd?\n",
                "phrase": "dopyt_przyst_odj"},
            "do_przystanku": {
                "question": "Dokąd ma jechać pojazd?\n",
                "phrase": "kier_przyst"}}

    def extract_deeper(self, data):
        for k1 in data.keys():
            if isinstance(data[k1], dict):
                if data[k1] == {}:
                    if k1 in self.defaults:
                        result = self.defaults[k1]
                else:
                    d2 = self.extract_deeper(data[k1])
                    result = d2
            else:
                result = data[k1]
            if result is not None and result != {}:
                return result
        return None

    def extract_vars(self, data, query="last query"):
        for k1 in data.keys():
            self.dialog_state[query]["type"] = k1  # We assume 1 key
            d1 = data[k1]
            for k2 in d1.keys():
                d2 = d1[k2]
                if isinstance(d2, dict):
                    if d2 == {}:
                        if k2 in self.defaults:
                            self.dialog_state[query][k2] = self.defaults[k2]
                    else:
                        d2 = self.extract_deeper(d2)
                        if d2 is not None:
                            self.dialog_state[query][k2] = d2
                else:
                    self.dialog_state[query][k2] = d2

    def needs_completion(self, query="last query"):
        lq = self.dialog_state[query]
        if lq["type"] == "pyt_odj":
            if "z_przystanku" in lq and ("do_przystanku" in lq
                                         or "kierunek" in lq):
                return "OK"
            else:
                if "z_przystanku" not in lq:
                    return "z_przystanku"
                else:
                    return "do_przystanku"

    def start(self):
        initial_prompt = "Dzień dobry, tu rozkład jazdy gdańskiej komunikacji "
        initial_prompt += "miejskiej. Czym mogę służyć?\n"
        prompt = initial_prompt
        question = input(prompt).strip()
        while question != "":
            prompt = "Czym jeszcze mogę służyć?\n"
            tokenized_question = tokenize(question.lower())
            for p1 in self.initial_phrases:
                parsed = recognize_whole_phrase(Ph, p1, tokenized_question)
                if parsed[0]:
                    #  print(parsed[2])
                    self.extract_vars(parsed[2])

                    lq = self.dialog_state["last query"]

                    if lq["type"] == "pyt_nastepny":
                        prev_query = self.dialog_state["previous query"]
                        last_result = self.dialog_state["last_result"]

                        print(prev_query)
                        print(last_result)

                        if prev_query != {} and last_result !={}:
                            h, m = last_result["dept_time"].split(":")
                            t = int(h) *60 + int(m) +1
                            t_h = t//60
                            t_m = t%60
                            new_time = f"{t_h:02}:{t_m:02}"
                            next_query = prev_query.copy()
                            next_query["czas"] =  new_time
                            r2 = Tm.exec_query(next_query)

                            if r2!={}:
                                self.dialog_state["last_result"] = r2
                                self.dialog_state["previous_query"] = next_query
                                print(f"{Tm.vehicle_type(r2['line']).capitalize()} linii {r2['line']} odjedzie z przystanku ",
                                      end="")
                                
                                print(f"{r2['from_stop']} w kierunku {r2['destination']} o {r2['dept_time']}.")
                            else:
                                print("Brak dalszych polaczen")
                        else:
                            print("Nie znam poprzedniego zapytania")
                        break
                                
                            
                    nc = self.needs_completion()
                    while nc != "OK":
                        if nc in self.completion_data:
                            cd = self.completion_data[nc]
                            aux_question = input(cd["question"])
                            tq1 = tokenize(aux_question)
                            node = Ph.get_definition_node(cd["phrase"])
                            parsed1 = recognize_whole_phrase(Ph, node,
                                                             tq1)
                            #  print(parsed1)
                            if parsed1[0]:
                                self.extract_vars(parsed1[2], "aux query")
                                for n2 in self.dialog_state["aux query"]:
                                    if n2 != "type":
                                        x = self.dialog_state["aux query"][n2]
                                        self.dialog_state["last query"][n2] = x
                                nc = self.needs_completion()
                            else:
                                break
                        else:
                            break
                    if nc == "OK":
                        lq = self.dialog_state["last query"]
                        #  print(lq)
                        r1 = Tm.exec_query(lq)
                        if r1 != {}:
                            self.dialog_state["last_result"] = r1
                            print(f"{Tm.vehicle_type(r1['line']).capitalize()}",
                                  end=" ")
                            print(f"linii {r1['line']} odjedzie z przystanku ",
                                  end="")
                            print(f"{r1['from_stop']} w kierunku", end=" ")
                            print(f"{r1['destination']} o", end=" ")
                            print(f"{r1['dept_time']}.")
                            pq = self.dialog_state["last query"]
                            self.dialog_state["previous query"] = pq
                            self.dialog_state["last query"] = {}
                        else:
                            print("W rozkładzie brak takiego połączenia! ")
                        break
                        
            else:
                prompt = self.error_message[self.verbosity_level]
                self.verbosity_level = min(self.verbosity_level + 1,
                                           len(self.error_message) - 1)
            question = input(prompt)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Dialog Manager.")
    parser.add_argument("-f", "--file", default="dialog.json",
                        help="Dialogue data file.")
    args = parser.parse_args()
    if "file" in args and args.file is not None:
        diag_file = args.file
    else:
        diag_file = "dialog.json"
    diag = json.load(open(diag_file, "r"))
    diag.pop()
    
    Ph.initialize(diag)
    dm = Dialog_Manager(Tm.get_defaults())
    dm.start()
    
