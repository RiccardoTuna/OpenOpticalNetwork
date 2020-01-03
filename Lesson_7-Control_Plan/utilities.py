import json
from pathlib import Path
from gnpy.core.utils import merge_amplifier_restrictions
from gnpy.core.equipment import equipment_from_json


def _load_equipment(path):
    with open(path, 'r') as file:
        eqp_dict = json.load(file)
        eqp = equipment_from_json(eqp_dict, path)
    return eqp, eqp_dict


def get_edfa_parameters(edfa_json_path, eqipment_json_path):
    """ This is an utility that, given the JSON files returns to you the parameters needed for the __init__ of GNPy Edfa.
    Once you have the edfa_params you can instantiate and Edfa as:
    >>> from gnpy.core.elements import Edfa
    >>>
    >>> edfa_instance = Edfa(**edfa_params)

    :param edfa_json_path: path of the json file with the EDFA parameters
    :param eqipment_json_path: path of the json file with the equipment
    :return: edfa_params: a dictionary containing the parameters to properly instantiate the GNPy EDFA
    """
    eqp_file_name = Path(eqipment_json_path)
    eqp, eqp_dict = _load_equipment(eqp_file_name)

    file_name = Path(edfa_json_path)
    with open(file_name, 'r') as file:
        edfa_params = json.load(file)

    def_params = edfa_params.setdefault('params', {})
    edfa_params['params'] = merge_amplifier_restrictions(def_params, eqp['Edfa']['simple_edfa'].__dict__)
    edfa_params.pop('type_variety')
    edfa_params.pop('type')

    return edfa_params