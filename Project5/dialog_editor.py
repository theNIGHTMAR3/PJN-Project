#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 18:02:20 2023

@author: Jan Daciuk
"""
import dearpygui.dearpygui as dpg
import json
# dearpygui.dearpygui.add_item_activated_handler(**kwargs)
# dearpygui.dearpygui.add_item_active_handler(**kwargs)
# dearpygui.dearpygui.add_item_clicked_handler(button=- 1, **kwargs)
# dearpygui.dearpygui.add_item_deactivated_after_edit_handler(**kwargs)
# dearpygui.dearpygui.add_item_deactivated_handler(**kwargs)
# dearpygui.dearpygui.add_item_double_clicked_handler(button=- 1, **kwargs)
# dearpygui.dearpygui.add_item_edited_handler(**kwargs)
# dearpygui.dearpygui.add_item_hover_handler(**kwargs)
# dearpygui.dearpygui.add_item_resize_handler(**kwargs)
# dearpygui.dearpygui.add_mouse_click_handler(button=- 1, **kwargs)
# dearpygui.dearpygui.add_mouse_down_handler(button=- 1, **kwargs)
# dearpygui.dearpygui.add_mouse_release_handler(button=- 1, **kwargs)
# dearpygui.dearpygui.add_node(**kwargs)
# dearpygui.dearpygui.add_node_attribute(**kwargs)
# dearpygui.dearpygui.add_node_editor(**kwargs)
# dearpygui.dearpygui.add_node_link(attr_1, attr_2, **kwargs)
# dearpygui.dearpygui.add_tab(**kwargs)
# dearpygui.dearpygui.add_tab_bar(**kwargs)
# dearpygui.dearpygui.add_tab_button(**kwargs)
# dearpygui.dearpygui.add_time_picker(**kwargs)
# dearpygui.dearpygui.add_tooltip(parent, **kwargs)
# dearpygui.dearpygui.bind_item_handler_registry(item, handler_registry)
# dearpygui.dearpygui.child_window(**kwargs)
# dearpygui.dearpygui.configure_app(**kwargs)→ None
# dearpygui.dearpygui.configure_item(item: Union[int, str], **kwargs)→ None
# dearpygui.dearpygui.delete_item(item, **kwargs)
# dearpygui.dearpygui.disable_item(item: Union[int, str])
# dearpygui.dearpygui.does_alias_exist(alias)
# dearpygui.dearpygui.does_item_exist(item)
# dearpygui.dearpygui.enable_item(item: Union[int, str])
# dearpygui.dearpygui.generate_uuid()
# dearpygui.dearpygui.get_active_window()
# dearpygui.dearpygui.get_alias_id(alias)
# dearpygui.dearpygui.get_aliases()
# dearpygui.dearpygui.get_all_items()
# dearpygui.dearpygui.get_app_configuration()
# dearpygui.dearpygui.get_item_alias(item)
# dearpygui.dearpygui.get_item_children(item: Union[int, str], slot: int = - 1)→ Optional[Union[dict, List[int]]]
# dearpygui.dearpygui.get_item_configuration(item)
# dearpygui.dearpygui.get_item_info(item)
# dearpygui.dearpygui.get_item_label(item: Union[int, str])→ Optional[str]
# dearpygui.dearpygui.get_item_parent(item: Union[int, str])→ Optional[int]
# dearpygui.dearpygui.get_item_pos(item: Union[int, str])→ List[int]
# dearpygui.dearpygui.get_item_rect_max(item: Union[int, str])→ List[int]
# dearpygui.dearpygui.get_item_rect_size(item: Union[int, str])→ List[int]
# dearpygui.dearpygui.get_item_slot(item: Union[int, str])→ Optional[int]
# dearpygui.dearpygui.get_item_source(item: Union[int, str])→ Optional[str]
# dearpygui.dearpygui.get_item_type(item: Union[int, str])→ str
# dearpygui.dearpygui.get_item_user_data(item: Union[int, str])→ Optional[Any]
# dearpygui.dearpygui.get_item_width(item: Union[int, str])→ Optional[int]
# dearpygui.dearpygui.get_value(item)
# dearpygui.dearpygui.handler_registry(**kwargs)
# dearpygui.dearpygui.hide_item(item: Union[int, str], *, children_only: bool = False)
# dearpygui.dearpygui.is_item_left_clicked(item: Union[int, str])→ Optional[bool]
# dearpygui.dearpygui.is_item_middle_clicked(item: Union[int, str])→ Optional[bool]
# dearpygui.dearpygui.is_item_right_clicked(item: Union[int, str])→ Optional[bool]
# dearpygui.dearpygui.item_handler_registry(**kwargs)
# dearpygui.dearpygui.last_container()
# dearpygui.dearpygui.last_item()
# dearpygui.dearpygui.menu(**kwargs)
# dearpygui.dearpygui.menu_bar(**kwargs)
# dearpygui.dearpygui.node(**kwargs)
# dearpygui.dearpygui.tab(**kwargs)
# dearpygui.dearpygui.tab_bar(**kwargs)


class node_number():
    # This class is used for generating node numbers.
    # They form a part of nodes names.
    def __init__(self):
        self.number = 0

    def get(self):
        """
        Generate the consecutive natural number.

        Returns
        -------
        int
            The next integer.

        """
        self.number += 1
        return str(self.number)

    def set(self, number):
        self.number += number


class item_position():
    # This class is used for remembering last node position.
    # it is used for good positioning of a new node.
    def __init__(self):
        self.last_node = None  # last generated node
        self.last_pos = [0, 0]  # position of that last node
        self.positions = {}
        self.from_file = False

    def set_last_node(self, node_id):
        """
        Remember the last generated node.

        Parameters
        ----------
        node_id : str
            Last node name.

        Returns
        -------
        None.

        """
        self.last_node = node_id

    def get_new_pos(self, node=None):
        """
        Calculate the position of a new node.

        Returns
        -------
        (int, int)
            Position of a new node.
        """
        #print(f"get_new_pos(node={node})")
        if (node is not None and self.positions is not None
                and node in self.positions):
            #print("Node position found")
            return self.positions[node]
        if self.last_node is not None:
            pos = dpg.get_item_pos(self.last_node)
        else:
            pos = [0, 0]
        dpg.split_frame()
        if self.last_node is not None:
            pos[0] += 150   # dpg.get_item_width(tag) always returns 0
        return pos

    def set_positions(self, positions):
        """
        Remember positions of nodes loaded from a file.

        Parameters
        ----------
        positions : list([int, [int, int]])
            Positions (second item being 2 coordinates) of nodes (first item).

        Returns
        -------
        None.

        """
        self.positions = {}
        for z in positions:
            n, c = z
            self.positions[n] = c

    def reset_positions(self):
        """
        Clear positions loaded from a file.

        Returns
        -------
        None.

        """
        self.positions = None

    def set_from_file(self, value):
        """
        Set variable (field) from_file.

        Parameters
        ----------
        value : Bool
            If True, the x coordinate of phrase starting node is not modified.

        Returns
        -------
        None.

        """
        self.from_file = value

    def get_from_file(self):
        """
        Return from_file field value.

        Returns
        -------
        int
            If True, the x coordinate of phrase starting node is not modified.

        """
        return self.from_file


nn = node_number()


class Phrases():
    # This class holds information about phrases used in a dialog
    def __init__(self, predef=[]):
        self.nodes = []
        self.node_text = {}
        self.node_links = {}
        self.node_sem = {}
        self.phrase_ref = set()
        self.phrase_def = set()
        self.phrase_end = set()
        self.predef_nodes = set()
        self.predef = predef
        self.phrase_definition = {}

    def clear(self):
        self.nodes = []
        self.node_text = {}
        self.node_links = {}
        self.node_sem = {}
        self.phrase_ref = set()
        self.phrase_def = set()
        self.phrase_end = set()
        self.predef_nodes = set()

    def set_predef(self, predef):
        self.predef = predef

    def get_predef(self):
        return self.predef

    def initialize(self, diag):
        # To load from a file, diag is a list.
        self.nodes = diag[0]
        self.node_text = diag[1]
        self.node_links = diag[2]
        self.node_sem = diag[3]
        self.phrase_ref = set(diag[4])
        self.phrase_def = set(diag[5])
        self.phrase_end = set(diag[6])
        self.predef_nodes = set(diag[7])
        for n1 in self.phrase_def:
            self.phrase_definition[self.node_text[n1]] = n1

    def as_list(self):
        # Create a list to be saved in a file.
        return [self.nodes, self.node_text, self.node_links, self.node_sem,
                list(self.phrase_ref), list(self.phrase_def),
                list(self.phrase_end), list(self.predef_nodes)]

    def check(self):
        # Check whether a dialog is complete
        incomplete = []
        undefined = []
        for node in self.nodes:
            if node not in self.phrase_end:
                if node not in self.node_text or self.node_text[node] == "":
                    incomplete.append(node)
                elif node in self.phrase_def or node in self.phrase_ref:
                    if node not in self.node_sem or self.node_sem[node] == "":
                        incomplete.append(node)
                    elif node in self.phrase_ref:
                        t1 = self.node_text[node]
                        for n1 in self.nodes:
                            if n1 in self.phrase_def:
                                if self.node_text[n1] == t1:
                                    break
                        else:
                            undefined.append(node)

    def add_link(self, source, target):
        # target follows source in a phrase.
        if source in self.node_links:
            self.node_links[source].append(target)
        else:
            self.node_links[source] = [target]

    def remove_link(self, source, target):
        # target no longer follows source in a phrase.
        print(f"remove_link(source={source}, target={target})")
        self.node_links[source].remove(target)

    def add_node(self, node_name):
        # Remember a new node just created.
        if node_name not in self.nodes:
            self.nodes.append(node_name)

    def delete_node(self, node_name):
        self.nodes.remove(node_name)
        if node_name in self.node_text:
            del self.node_text[node_name]
        if node_name in self.node_sem:
            del self.node_sem[node_name]
        if node_name in self.phrase_ref:
            del self.phrase_ref[node_name]
        elif node_name in self.phrase_def:
            del self.phrase_def[node_name]
        elif node_name in self.phrase_end:
            del self.phrase_end[node_name]
        if node_name in self.node_links:
            print(f"Removing all links from node {node_name}")
            del self.node_links[node_name]
        for n1 in self.nodes:
            if n1 in self.node_links:
                if node_name in self.node_links[n1]:
                    print(f"Removing link from {n1} to {node_name}")
                    self.remove_link(n1, node_name)

    def set_node_text(self, node, text):
        self.node_text[node] = text
        self.add_node(node)

    def get_node_text(self, node):
        return self.node_text[node]

    def set_node_sem(self, node, semantics):
        self.node_sem[node] = semantics
        self.add_node(node)

    def get_node_sem(self, node):
        return self.node_sem[node]

    def mark_as_phrase_def(self, node):
        self.phrase_def.add(node)
        self.add_node(node)
        self.phrase_definition[self.node_text[node]] = node

    def mark_as_phrase_ref(self, node):
        self.phrase_ref.add(node)
        self.add_node(node)

    def mark_as_phrase_end(self, node):
        self.phrase_end.add(node)
        self.add_node(node)

    def mark_as_predef(self, node):
        self.predef_nodes.add(node)
        self.add_node(node)

    def is_phrase_def(self, node):
        return node in self.phrase_def

    def is_phrase_ref(self, node):
        return node in self.phrase_ref

    def is_predef(self, node):
        return node in self.predef_nodes

    def is_end(self, node):
        return node in self.phrase_end

    def get_links(self, node):
        if node in self.node_links:
            return self.node_links[node]
        else:
            return []

    def get_definition_node(self, text):
        return self.phrase_definition[text]


class GUI_State():
    def __init__(self):
        self.uuid2node_name = {}
        self.input_port = {}
        self.output_port = {}
        self.last_pos = item_position()

    def node_from_uuid(self, uuid):
        return self.uuid2node_name[uuid]

    def set_node_from_uuid(self, node, uuid):
        self.uuid2node_name[uuid] = node

    def set_input_port(self, node, port_uuid):
        self.input_port[node] = port_uuid

    def get_input_port(self, node):
        return self.input_port[node]

    def set_output_port(self, node, port_uuid):
        self.output_port[node] = port_uuid

    def get_output_port(self, node):
        return self.output_port[node]

    def get_positions(self, nodes):
        n2u = {}
        for (u, n) in self.uuid2node_name.items():
            n2u[n] = u
        return [[node, dpg.get_item_pos(n2u[node])] for node in nodes]

    def set_positions(self, positions):
        self.last_pos.set_positions(positions)

    def clear_positions(self):
        self.last_pos.reset_positions()


gs = GUI_State()
Ph = Phrases()


def set_predef(predef):
    global Ph
    print(f"set_predef({predef})")
    Ph.set_predef(predef)


def get_predef():
    print("get_predef()")
    global Ph
    print(f"  returning {Ph.get_predef()}")
    print(f"  Ph is {Ph}")
    return Ph.get_predef()


def callback_close_window(sender):
    dpg.delete_item(sender)


# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    global Ph, gs
    print(f"link_callback({app_data}, {sender})")
    print(f"parents: {dpg.get_item_parent(app_data[0])},", end=" ")
    print(f"({dpg.get_item_info(dpg.get_item_parent(app_data[0]))}),", end=" ")
    print(f"{dpg.get_item_parent(app_data[1])}", end=" ")
    print(f"({dpg.get_item_info(dpg.get_item_parent(app_data[1]))})")
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    n1 = gs.node_from_uuid(dpg.get_item_parent(app_data[0]))
    n2 = gs.node_from_uuid(dpg.get_item_parent(app_data[1]))
    Ph.add_link(n1, n2)


# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    print(f"delink_callback(sender={sender}, app_data={app_data})")
    # app_data -> link_id
    global gs, Ph
    dpg.delete_item(app_data)
    if isinstance(app_data, list):
        n1 = gs.node_from_uuid(dpg.get_item_parent(app_data[0]))
        n2 = gs.node_from_uuid(dpg.get_item_parent(app_data[1]))
        Ph.remove_link(n1, n2)


def callback_delete_item(sender):
    print(f"callback_delete_item({sender})")
    global Ph, gs
    for selected_node in dpg.get_selected_nodes("noded"):
        print(f"Calling dpg.delete_item({selected_node})")
        dpg.delete_item(selected_node)
        n1 = gs.node_from_uuid(selected_node)
        print(f"Deleting node {n1} from phrases")
        Ph.delete_node(n1)


# def delete_node(sender, app_data):  # to be removed
#     global gs
#     dpg.delete_item(app_data)
#     gs.set_last_node(None)


def add_node_text(sender, app_data):
    global Ph, gs
    print(f"add_node_text(sender={sender}, app_data={app_data})")
    print(f"parent={dpg.get_item_parent(sender)}")
    print(f"grandparent={dpg.get_item_parent(dpg.get_item_parent(sender))}")
    grandparent = dpg.get_item_parent(dpg.get_item_parent(sender))
    Ph.set_node_text(gs.node_from_uuid(grandparent), app_data)


def add_node_meaning(sender, app_data):
    global Ph, gs
    grandparent = dpg.get_item_parent(dpg.get_item_parent(sender))
    Ph.set_node_sem(gs.node_from_uuid(grandparent), app_data)


def add_node_predef(sender, app_data):
    print(f"add_node_predef(sender={sender}, app_data={app_data})")
    print(f"parent={dpg.get_item_parent(sender)}")
    print(f"grandparent={dpg.get_item_parent(dpg.get_item_parent(sender))}")
    grandparent = dpg.get_item_parent(dpg.get_item_parent(sender))
    Ph.set_node_text(gs.node_from_uuid(grandparent), app_data)


def add_node(node_type, text="", name="", semantics=""):
    global Ph, gs
    global nn
    print(f"add_node(node_type={node_type}, text={text}, name={name})")
    tag = dpg.generate_uuid()
    if name == "":
        node_name = f"n{nn.get()}"
    else:
        node_name = name
    print(f"Creating {node_type} node {node_name} tag {tag} text {text}")
    gs.set_node_from_uuid(node_name, tag)
    pos = gs.last_pos.get_new_pos(node_name)
    if node_type == "word":
        Ph.set_node_text(node_name, text)
        with dpg.node(label="word", parent="noded", tag=tag, pos=pos):
            p1 = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input,
                                    tag=p1):
                dpg.add_input_text(width=120, on_enter=False, hint="word",
                                   default_value=text, callback=add_node_text)
            gs.set_input_port(node_name, p1)
            p1 = dpg.generate_uuid()
            dpg.add_node_attribute(attribute_type=dpg.mvNode_Attr_Output,
                                   tag=p1)
            gs.set_output_port(node_name, p1)
    elif node_type == "phrase definition":
        if not gs.last_pos.get_from_file():
            pos[0] = 0
            pos[1] += 100
        Ph.set_node_text(node_name, text)
        Ph.set_node_sem(node_name, semantics)
        with dpg.node(label="phrase definition", parent="noded", tag=tag,
                      pos=pos):
            p1 = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output,
                                    tag=p1):
                dpg.add_input_text(width=120, on_enter=False, hint="name",
                                   default_value=text, callback=add_node_text)
                dpg.add_input_text(width=120, on_enter=False, hint="meaning",
                                   default_value=semantics,
                                   callback=add_node_meaning)
        Ph.mark_as_phrase_def(node_name)
        gs.set_output_port(node_name, p1)
    elif node_type == "phrase reference":
        Ph.set_node_text(node_name, text)
        Ph.set_node_sem(node_name, semantics)
        with dpg.node(label="phrase", parent="noded", tag=tag, pos=pos):
            p1 = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input,
                                    tag=p1):
                dpg.add_input_text(width=120, on_enter=False,
                                   hint="phrase name", default_value=text,
                                   callback=add_node_text)
            gs.set_input_port(node_name, p1)
            p1 = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output,
                                    tag=p1):
                dpg.add_input_text(width=120, on_enter=False, hint="meaning",
                                   default_value=semantics,
                                   callback=add_node_meaning)
            gs.set_output_port(node_name, p1)
        Ph.mark_as_phrase_ref(node_name)
    elif node_type == "END":
        with dpg.node(label="END", parent="noded", tag=tag, pos=pos):
            p1 = dpg.generate_uuid()
            dpg.add_node_attribute(attribute_type=dpg.mvNode_Attr_Input,
                                   tag=p1)
        Ph.mark_as_phrase_end(node_name)
        gs.set_input_port(node_name, p1)
    elif node_type == "predefined phrase":
        Ph.set_node_text(node_name, text)
        with dpg.node(label="predefined phrase", parent="noded", tag=tag,
                      pos=pos):
            p1 = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input,
                                    tag=p1):
                gs.set_input_port(node_name, p1)
                p1 = dpg.generate_uuid()
                print(f"Predefined: {get_predef()}")
                dpg.add_combo(items=get_predef(),
                              default_value=text,
                              callback=add_node_predef, width=120)
            dpg.add_node_attribute(attribute_type=dpg.mvNode_Attr_Output,
                                   tag=p1)
            gs.set_output_port(node_name, p1)
        Ph.mark_as_predef(node_name)
    pos = dpg.get_item_pos(tag)
    gs.last_pos.set_last_node(tag)


def add_word_node(sender, app_data, user_data=["", ""]):
    if user_data is not None:
        text, name = user_data
    else:
        text = ""
        name = ""
    print(f"add_word_node(text={text}, name={name})")
    add_node("word", text=text, name=name)


def add_phrase_start_node(sender, app_data, user_data=["", "", ""]):
    if user_data is not None:
        text, name, sem = user_data
    else:
        text = ""
        name = ""
        sem = ""
    print(f"add_phrase_start_node(text={text}, name={name}, sem={sem})")
    add_node("phrase definition", text=text, name=name, semantics=sem)


def add_phrase_node(sender, app_data, user_data=["", ""]):
    if user_data is not None:
        text, name, sem = user_data
    else:
        text = ""
        name = ""
        sem = ""
    print(f"add_phrase_reference_node(text={text}, name={name}, sem={sem})")
    add_node("phrase reference", text=text, name=name, semantics=sem)


def add_end_node(sender, app_data, user_data=""):
    if user_data is not None:
        name = user_data
    else:
        name = ""
    add_node("END", name=name)


def add_predef_node(sender, app_data, user_data=["", ""]):
    if user_data is not None:
        text, name = user_data
    else:
        name = ""
        text = ""
    add_node("predefined phrase", name=name, text=text)


def load_dialog(sender, app_data):
    global Ph, gs, nn
    Ph.clear()
    gs.last_pos.set_from_file(True)
    print(f"sender={sender}, app_data={app_data}")
    file_name = app_data["file_name"]
    diag = json.load(open(file_name, "r"))
    (nx, node_text, node_links, node_sem, ph_ref, ph_def,
     ph_end, ph_predef_n, pos) = diag
    print(f"nodes={nx}")
    print(f"phrase definition nodes={ph_def}, phrase reference nodes={ph_ref}")
    print(f"predefined phrase nodes={ph_predef_n}, end nodes={ph_end}")
    print(f"node text={node_text}")
    print(f"node links {node_links}")
    print(f"positions {pos}")
    gs.set_positions(pos)
    mx_node = 0
    for node in nx:
        nnn = int(node[1:])
        if nnn > mx_node:
            mx_node = nnn
        if node in ph_def:
            add_phrase_start_node(sender, app_data,
                                  user_data=[node_text[node], node,
                                             node_sem[node]])
        elif node in ph_ref:
            add_phrase_node(sender, app_data,
                            user_data=[node_text[node], node,
                                       node_sem[node]])
        elif node in ph_end:
            add_end_node(sender, app_data, user_data=node)
        elif node in ph_predef_n:
            add_predef_node(sender, app_data,
                            user_data=[node_text[node], node])
        else:
            add_word_node(sender, app_data,
                          user_data=[node_text[node], node])
    nn.set(mx_node)
    print("Linking nodes...")
    for node in node_links:
        print(f"Linking node {node}")
        for target in node_links[node]:
            print(f"{node} -> {target}")
            Ph.add_link(node, target)
            dpg.add_node_link(gs.get_output_port(node),
                              gs.get_input_port(target),
                              parent="noded")
    gs.clear_positions()
    gs.last_pos.set_from_file(False)


def save_dialog(sender, app_data):
    global Ph, gs
    print(f"save_dialog(sender={sender}, app_data={app_data})")
    file_name = app_data["file_name"]
    data = Ph.as_list()
    data.append(gs.get_positions(data[0]))
    json.dump(data, open(file_name, "w"))


def quit_dialog_editor():
    dpg.delete_item("DialEd")
    dpg.destroy_context()


def latex_dialog(sender, app_data):
    global Ph, gs
    print(f"latex_dialog(sender={sender}, app_data={app_data})")
    file_name = app_data["file_name"]
    from ed_latex_print import ed_latex_print
    elp = ed_latex_print(Ph, gs, file_name)
    elp.print_phrases()


def on_key_la(sender, app_data):
    if dpg.is_key_down(dpg.mvKey_O):
        dpg.show_item("load_file_dialog")
    elif dpg.is_key_down(dpg.mvKey_S):
        dpg.show_item("save_file_dialog")
    elif dpg.is_key_down(dpg.mvKey_P):
        dpg.show_item("print_file_latex")
    elif dpg.is_key_down(dpg.mvKey_Q):
        quit_dialog_editor()

def dialog_editor(title, predef):
    set_predef(predef)
    node_number()
    dpg.create_context()
    with dpg.font_registry():
        fontpath = "/usr/share/fonts/truetype/noto/"
        with dpg.font(fontpath + "NotoSans-Regular.ttf", 20) as font1:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range(0x0100, 0x017f)
            default_font = font1
            dpg.bind_font(default_font)

    dpg.create_context()
    dpg.create_viewport(title='Dialog Editor', width=1280, height=800)
    dpg.setup_dearpygui()

    with dpg.window(label=title,
                    width=1280, height=800, menubar=False,
                    tag="DialEd"):
        dpg.add_node_editor(callback=link_callback, minimap=True,
                            minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,
                            delink_callback=delink_callback, tag="noded")
        with dpg.handler_registry():
            dpg.add_key_release_handler(key=dpg.mvKey_Delete,
                                        callback=callback_delete_item)
            dpg.add_key_press_handler(dpg.mvKey_Control, callback=on_key_la)
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Load dialog",
                                  callback=lambda:
                                      dpg.show_item("load_file_dialog"))
                dpg.add_menu_item(label="Save dialog",
                                  callback=lambda:
                                      dpg.show_item("save_file_dialog"))
                dpg.add_menu_item(label="Print phrases",
                                  callback=lambda:
                                      dpg.show_item("print_file_latex"))
                dpg.add_menu_item(label="Quit", callback=quit_dialog_editor)
            with dpg.menu(label="Add node"):
                dpg.add_menu_item(label="Add word", callback=add_word_node)
                dpg.add_menu_item(label="Add phrase start",
                                  callback=add_phrase_start_node)
                dpg.add_menu_item(label="Add phrase reference",
                                  callback=add_phrase_node)
                if predef != []:
                    dpg.add_menu_item(label="Add predefined phrase",
                                      callback=add_predef_node)
                dpg.add_menu_item(label="Add end node", callback=add_end_node)

    with dpg.file_dialog(show=False, tag="save_file_dialog", width=800,
                         directory_selector=False,
                         height=300, default_filename="dialog",
                         callback=save_dialog):
        dpg.add_file_extension(".json", color=(255, 0, 255, 255),
                               custom_text="[json]")
        dpg.add_file_extension(".*")
    with dpg.file_dialog(show=False, tag="load_file_dialog", width=800,
                         directory_selector=False,
                         height=300, default_filename="dialog",
                         callback=load_dialog):
        dpg.add_file_extension(".json", color=(255, 0, 255, 255),
                               custom_text="[json]")
        dpg.add_file_extension(".*")
    with dpg.file_dialog(show=False, tag="print_file_latex", width=800,
                         directory_selector=False,
                         height=300, default_filename="dialog",
                         callback=latex_dialog):
        dpg.add_file_extension(".tex", color=(255, 0, 255, 255),
                               custom_text="[LaTeX]")
        dpg.add_file_extension(".*")

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    dpg.add_window(label='Dialog Editor')


if __name__ == "__main__":
    dialog_editor("Public Transport Schedule Query Setup",
                  ["przystanekM", "przystanekD", "czas", "numer"])
