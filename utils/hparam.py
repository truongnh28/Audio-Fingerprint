import yaml


def load_hparam(path):
    docs = yaml.load_all(open(path, 'r', encoding='utf-8'), Loader=yaml.Loader)

    hparam_dict = dict()
    for doc in docs:
        for k, v in doc.items():
            hparam_dict[k] = v
            pass
        pass

    return hparam_dict


# Create your own dictionary class
class Dotdict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    # Construction method
    def __init__(self, dict=None):
        # Judgment is not empty
        dic = dict() if not dict else dict

        for key, value in dic.items():
            if hasattr(value, 'keys'):
                value = Dotdict(value)
                pass
            self[key] = value

        pass

    pass


class Hparam(Dotdict):
    # Construction method
    def __init__(self, filepath='./config/config.yaml'):
        super(Dotdict, self).__init__()

        # Load the yaml file through the path and make it into a dictionary
        hp_dict = load_hparam(filepath)

        # Convert to your own dictionary
        hp_dotdict = Dotdict(hp_dict)

        for k, v in hp_dotdict.items():
            setattr(self, k, v)

            pass

        pass

    __getattr__ = Dotdict.__getitem__
    __setattr__ = Dotdict.__setitem__
    __delattr__ = Dotdict.__delitem__

    pass


hp = Hparam()
