import re
from keywords import label_keywords, Keywords


class Label:
    """
    Label class contains all nutritional information corresponding
    to a food label.
    """
    def __init__(self, attr_list=None, keyword_map=None):
        attrs = list(Keywords.json.values()).extend([
            'name', 'skewed', 'not_bw', 'curved',
            'wrinkled', 'shadowed', 'blurry'])

        if keyword_map is not None:
            non_decimal = re.compile(r'[^\d.]+')
            for k in label_keywords:
                key = label_keywords[k]
                try:
                    amount = keyword_map[key][0]
                    amount = non_decimal.sub('', amount)
                except KeyError:
                    amount = None

                setattr(self, k, amount)

            print(self)
            return

        if attr_list is None:
            attr_list = [None]*len(attrs)

        for i, attr in enumerate(attrs):
            # Final 6 attributes are true/false
            true_false_attrs = attrs[-6:]
            if attr in true_false_attrs:

                def processTF(tfstring):
                    if tfstring == "Yes":
                        return True
                    else:
                        return False

                attr_list[i] = processTF(attr_list[i])
            elif attr_list[i] == "":
                attr_list[i] = None

            setattr(self, attr, attr_list[i])

    def __str__(self):
        return str(self.__dict__)

    def __getitem__(self, key):
        return getattr(self, key)
