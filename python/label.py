import re
from keywords import label_keywords, Keywords


class Label:
    """
    Label class contains all nutritional information corresponding
    to a food label.
    """
    def __init__(self, attr_list=None, keyword_map=None):
        # TODO: Clean up this method
        attrs = list(Keywords.json.values())
        attrs.extend(['name'])
        attrs.extend(Keywords.spec_types.values())

        true_false_attrs = Keywords.spec_types.values()

        # Initialize all to None/False
        for attr in attrs:
            if attr in true_false_attrs:
                setattr(self, attr, False)
            else:
                setattr(self, attr, None)

        if attr_list is None:
            attr_list = [None]*len(attrs)

        def parse_attr_val(attr, val):
            # Special type attrs are True/False
            if attr in true_false_attrs:
                def processTF(tfstring):
                    if tfstring == "Yes":
                        return True
                    else:
                        return False

                return processTF(val)
            elif val == "":
                return None

            return val

        for i, attr in enumerate(attrs):
            attr_list[i] = parse_attr_val(attr, attr_list[i])
            setattr(self, attr, attr_list[i])

        if keyword_map is not None:
            for attr in attrs:
                key = attr
                if key in Keywords.label:
                    key = Keywords.label[attr]

                if key in keyword_map:
                    amount = parse_attr_val(attr, keyword_map[key])
                else:
                    amount = None

                setattr(self, attr, amount)

    def __str__(self):
        # Only print nutritional info
        print_attrs = Keywords.json.values()
        return str({k: self[k] for k in print_attrs})

    def __repr__(self):
        return str(self.__dict__)

    def __getitem__(self, key):
        return getattr(self, key)
