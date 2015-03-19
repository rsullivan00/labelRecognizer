import jsonpickle

class Label:
    """Label class contains all nutritional information corresponding to a food label."""
    def __init__(self, attr_list=None):
        attrs = ['name', 'calories', 'total_fat', 'saturated_fat', 'trans_fat', 'poly_fat', 'mono_fat', 'cholesterol', 'sodium', 'potassium', 'carbohydrates', 'fiber', 'sugars', 'protein', 'skewed', 'not_bw', 'curved', 'wrinkled', 'shadowed', 'blurry']
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
