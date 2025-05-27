#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 20:21:11 2024

@author: Jan Daciuk
"""
import regex


prolog = r"""\documentclass[10pt]{article}
\usepackage{iftex}
\ifXeTeX
\usepackage{fontspec}
\usepackage[EU1]{fontenc}
\else
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\fi
\usepackage[polish]{babel}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{shapes.multipart}
\pgfdeclarelayer{background layer}
\pgfdeclarelayer{foreground layer}
\pgfsetlayers{background layer,main,foreground layer}
\usepackage[margin=1cm]{geometry}
%\usepackage{hyperref}
\usepackage{bookmark}
\pagestyle{empty}
\begin{document}\small
"""
epilog = r"""\end{document}
"""
tn3 = (r"\node[rectangle split,rectangle split allocate boxes=3,"
       + r"rectangle split parts=3,rounded corners,draw,"
       + r"rectangle split part fill={blue!20,white,white}] ")
tn2 = (r"\node[rectangle split,rectangle split parts=2,rounded corners,"
       + "rectangle split part fill={blue!20,white},draw] ")


def de_(s):
    return regex.sub("_", "\\_", s)


class ed_latex_print:
    def __init__(self, ph, gs, file_name, threshold=1800):
        self.ph = ph
        self.gs = gs
        self.file_name = file_name
        self.threshold = threshold
        ppl = gs.get_positions(ph.nodes)
        self.n2p = {}
        for pp in ppl:
            self.n2p[pp[0]] = pp[1]

    def find_bottom(self, start_node):
        """
        Find the largest y coordinate of a part of a graph.

        Parameters
        ----------
        start_node : str
            start node of a part of a graph to be searched.

        Returns
        -------
        local_max : int
            The largest y coordinate in the part of the graph accessible from
            start_node.

        """
        local_max = self.n2p[start_node][1]
        self.visited = set()
        self.visited.add(start_node)
        for next_node in self.ph.get_links(start_node):
            if next_node not in self.visited:
                self.visited.add(next_node)
                next_max = self.find_bottom(next_node)
                if next_max > local_max:
                    local_max = next_max
        self.visited = set()
        return local_max

    def print_node(self, fp, node):
        ppl = self.gs.get_positions([node])
        pp = ppl[0][1]
        pp[0] = pp[0] // 2
        pp[1] = - pp[1] // 2
        if self.ph.is_end(node):
            fp.write(r"\node[rounded corners,draw,fill=blue!20] ")
            fp.write(f"({node})\n")
            fp.write(f"at ({pp[0]}pt,{pp[1]}pt) ")
            fp.write(r"{\textbf{END}")
        elif self.ph.is_phrase_def(node):
            fp.write(tn3)
            fp.write(f"({node})\n")
            fp.write(f"at ({pp[0]}pt,{pp[1]}pt) ")
            fp.write(r"{\textbf{phrase definition}\nodepart{two}")
            fp.write(f"{de_(self.ph.get_node_text(node))}")
            fp.write(r"\nodepart{three}")
            fp.write(f"{de_(self.ph.get_node_sem(node))}\n")
        elif self.ph.is_phrase_ref(node):
            fp.write(tn3)
            fp.write(f"({node})\n")
            fp.write(f"at ({pp[0]}pt,{pp[1]}pt) ")
            fp.write(r"{\textbf{phrase}\nodepart{two}")
            fp.write(f"{de_(self.ph.get_node_text(node))}")
            fp.write(r"\nodepart{three}")
            fp.write(f"{de_(self.ph.get_node_sem(node))}\n")
        elif self.ph.is_predef(node):
            fp.write(tn2)
            fp.write(f"({node})\n")
            fp.write(f"at ({pp[0]}pt,{pp[1]}pt) ")
            fp.write(r"{\textbf{predef. phrase}\nodepart{two}")
            fp.write(f"{de_(self.ph.get_node_text(node))}\n")
        else:
            fp.write(tn2)
            fp.write(f"({node})\n")
            fp.write(f"at ({pp[0]}pt,{pp[1]}pt) ")
            fp.write(r'{\textbf{word}\nodepart{two}')
            fp.write(f"{de_(self.ph.get_node_text(node))}\n")
        fp.write("};\n")
        if not self.ph.is_phrase_def(node):
            fp.write(r"\fill ")
            fp.write(f"({node}.west) circle [radius=3pt];\n")
        if not self.ph.is_end(node):
            fp.write(r"\fill ")
            fp.write(f"({node}.east) circle [radius=3pt];\n")

    def print_phrase(self, fp, start_node):
        # print(f"print_phrase(start_node={start_node})")
        path = [start_node]
        visited = set(start_node)
        if self.ph.is_phrase_def(start_node):
            while path != []:
                current_node = path.pop()
                self.print_node(fp, current_node)
                for next_node in self.ph.get_links(current_node):
                    visited.add(next_node)
                    path.append(next_node)

    def draw_link(self, fp, node1, node2):
        # fp.write(r"\draw " + f"({node1}.east) -- ({node2}.west);")
        fp.write(r"\draw " + f"({node1}.east) .. controls "
                 + f"([xshift=15pt]{node1}.east) and "
                 + f"([xshift=-15pt]{node2}.west) .. ({node2}.west);\n")

    def draw_phrase_links(self, fp, start_node):
        phrase_nodes = []
        to_be_visited = [start_node]
        fp.write(r"\begin{pgfonlayer}{background layer}" + "\n")
        while to_be_visited != []:
            next_node = to_be_visited[0]
            to_be_visited = to_be_visited[1:]
            phrase_nodes.append(next_node)
            for n1 in self.ph.get_links(next_node):
                self.draw_link(fp, next_node, n1)
                if n1 not in to_be_visited:
                    to_be_visited.append(n1)
        fp.write(r"\end{pgfonlayer}" + "\n")

    def print_phrases(self):
        print("print_phrases()")
        with open(self.file_name, "w") as fp:
            fp.write(prolog)
            ph_d = []
            for n1 in self.ph.nodes:
                if self.ph.is_phrase_def(n1):
                    ph_d.append([n1, self.find_bottom(n1)])
            ph_d.sort(key=(lambda x: x[1]))
            while ph_d != []:
                print(f"Printing page, ph_d is: {ph_d}")
                fp.write(r"\scalebox{0.7}{\begin{tikzpicture}" + "\n")
                page_phrases = [p1 for p1 in ph_d if p1[1] < self.threshold]
                print(f"page_phrases={page_phrases}")
                for n1 in page_phrases:
                    self.print_phrase(fp, n1[0])
                    self.draw_phrase_links(fp, n1[0])
                fp.write(r"\end{tikzpicture}}" + "\n")
                ph_d = ph_d[len(page_phrases):]
                if ph_d != []:
                    fp.write(r"\newpage" + "\n")
                    for n1 in self.ph.nodes:
                        self.n2p[n1][1] = self.n2p[n1][1] - self.threshold
                    for n1 in ph_d:
                        n1[1] = n1[1] - self.threshold
                print(f"ph_d after update: {ph_d}")
            fp.write(epilog)
