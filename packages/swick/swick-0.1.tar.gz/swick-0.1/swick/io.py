from unicodedata import decimal
from . import swc

import re


class SWCFormatError(Exception):
    """
    Error thrown during reading or writing of ``.swc`` files in
    cases in which the format is not or cannot be properly
    adhered to.
    """
    pass


def parse_int(value: str,  name: str, min_value: int, file_name: str,
              line_number: int,):
    """
    Attempts to interpet a given string ``value`` as an integer,
    returning the integer on success and raising an ``SWCFormatError``
    on failure.

    :parameter value: the string value to be parsed
    :parameter name: the name of the field being parsed
    :parameter min_value: minimum valid integer value
    :parameter file_name: the name of the file being read
    :parameter line_number: the line where the value occurs
    :return: an integer interpretation of the value
    """

    try:
        assert value.lstrip("-").isdigit()
        int_value = int(value)
        assert int_value >= min_value
        return int_value
    except (AssertionError, ValueError):
        raise SWCFormatError(f"Could not read {file_name}. Line"
                             f" {line_number} has {name} with value"
                             f" {value!r}; expected an integer"
                             f" greater than {min_value - 1}.")


def parse_float(value: str,  name: str, file_name: str, line_number: int,):
    """
    Attempts to interpet a given string ``value`` as a float, returning the
    float on success and raising an ``SWCFormatError`` on failure.

    :parameter value: the string value to be parsed
    :parameter name: the name of the field being parsed
    :parameter file_name: the name of the file being read
    :parameter line_number: the line where the value occurs
    :return: a float interpretation of the value
    """

    try:
        return float(value)
    except ValueError:
        raise SWCFormatError(f"Could not read {file_name}. Line"
                             f" {line_number} has {name} with value"
                             f" {value!r}; expected a float.")


def compute_object(root_node: tuple[int, swc.Node],
                   nodes: dict[int, list[tuple[int, swc.Node]]]):
    """
    Beginning at the rode node, searches available nodes in order to construct
    and return an ``Object`` containing all of the nodes connected to the root.

    :parameter root_node: an ID-Node pair for the root node
    :parameter nodes: dictionary mapping parent IDs to list of ID-Node pairs
    :return: an ``Object`` containing all nodes connected to the root
    """
    parent_id_stack = [root_node[0]]
    object_nodes = {root_node[0]: root_node[1]}

    while parent_id_stack:
        parent_id = parent_id_stack.pop()
        if parent_id not in nodes:
            continue
        for child in nodes[parent_id]:
            object_nodes[child[0]] = child[1]
            parent_id_stack.append(child[0])
        nodes.pop(parent_id)

    sorted_object_nodes = dict(sorted(object_nodes.items()))
    return swc.Object(sorted_object_nodes)


def read_swc(path: str):
    """
    Reads an ``.swc`` file to create and return an ``SWC`` object.

    :parameter path: the path to the ``.swc`` file to be read
    :return: an ``SWC`` object containing the loaded data
    """

    swc_file = open(path, 'r')
    nodes = dict()
    root_nodes = []
    id_line_numbers = dict()

    line_number = 0
    for line in swc_file:
        line_number = line_number + 1

        # ignore empty, white-space only, and comment lines
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        fields = re.split(r'[\t ]+', line)
        if len(fields) != 7:
            raise SWCFormatError(f"Could not read {path}. Line"
                                 f" {line_number} contains"
                                 f" {len(fields)} fields;"
                                 f" expected 7 fields.")

        id = parse_int(fields[0], "ID", 1, path, line_number)
        type = parse_int(fields[1], "type", 0, path, line_number)
        x = parse_float(fields[2], "x position", path, line_number)
        y = parse_float(fields[3], "y position", path, line_number)
        z = parse_float(fields[4], "z position", path, line_number)
        radius = parse_float(fields[5], "radius", path, line_number)
        parent_id = parse_int(fields[6], "parent ID", -1, path, line_number)

        if parent_id == id:
            raise SWCFormatError(f"Could not read {path}. Line"
                                 f" {line_number} refers to itself as the"
                                 f" parent. Root nodes should use parent ID"
                                 f" -1.")

        if id in id_line_numbers:
            raise SWCFormatError(f"Could not read {path}. Line"
                                 f" {line_number} contains an ID {id}"
                                 f" which already exists on line"
                                 f" {id_line_numbers[id]}.")
        else:
            id_line_numbers[id] = line_number

        node = swc.Node(type, x, y, z, radius, parent_id)
        id_node_pair = (id, node)
        is_root = parent_id == -1

        if is_root:
            root_nodes.append(id_node_pair)
        else:
            if parent_id in nodes:
                nodes[parent_id].append(id_node_pair)
            else:
                nodes[parent_id] = [id_node_pair]

    objects = []
    for root_node in root_nodes:
        objects.append(compute_object(root_node, nodes))

    if nodes:
        unreachable_ids = []
        for parent_id in nodes:
            for id_node_pair in nodes[parent_id]:
                unreachable_ids.append(id_node_pair[0])
        raise SWCFormatError(f"Could not read {path}. The nodes with the"
                             f" following IDs are unreachable:"
                             f" {unreachable_ids}")

    return swc.SWC(objects)


def write_swc(path: str, swc: swc.SWC, delimeter: str = " ",
              decimal_places: int = -1):
    """
    Writes an SWC object into an ``.swc`` file.

    :parameter path: the path to the ``.swc`` file to be written
    :parameter swc: the SWC object to be written to a file
    :parameter delimeter: separator for fields (tabs and spaces only)
    :parameter decimal_places: number of decimal places written for floats; if
                               -1, uses as many as necessary for each field
    :return: an ``SWC`` object containing the data to be written
    """

    swc_file = open(path, 'w')

    if not len(delimeter):
        raise ValueError(f"Could not write {path}. Delimeter may not be an"
                         f" empty string.")
    elif re.sub(r'[\t ]+', '', delimeter) != "":
        raise ValueError(f"Could not write {path}. Delimeter may only contain"
                         f" tabs and space, but was specified as"
                         f" {delimeter!r}.")

    if decimal_places < -1:
        raise ValueError(f"Could not write {path}. {decimal_places} is not a"
                         f" valid value for number of decimal places; expected"
                         f" a value of -1 or greater.")

    for object in swc.objects:
        for id in object.nodes:
            node = object.nodes[id]
            if decimal_places == -1:
                swc_file.write(f"{id}{delimeter}{node.type}{delimeter}{node.x}"
                               f"{delimeter}{node.y}{delimeter}{node.z}"
                               f"{delimeter}{node.radius}{delimeter}"
                               f"{node.parent_id}\n")
            else:
                swc_file.write(f"{id}{delimeter}{node.type}{delimeter}"
                               f"{node.x:.{decimal_places}f}{delimeter}"
                               f"{node.y:.{decimal_places}f}{delimeter}"
                               f"{node.z:.{decimal_places}f}{delimeter}"
                               f"{node.radius:.{decimal_places}f}{delimeter}"
                               f"{node.parent_id}\n")
