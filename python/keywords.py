from attrdict import AttrDict

# Label keywords correspond to the words found on
# the physical labels themselves.
label_keywords = {
    'calories': 'Calories',
    'total_fat': 'Total Fat',
    'saturated_fat': 'Saturated Fat',
    'trans_fat': 'Trans Fat',
    'poly_fat': 'Polyunsaturated Fat',
    'mono_fat': 'Monounsaturated Fat',
    'cholesterol': 'Cholesterol',
    'sodium': 'Sodium',
    'potassium': 'Potassium',
    'carbohydrates': 'Total Carbohydrate',
    'fiber': 'Dietary Fiber',
    'sugars': 'Sugars',
    'protein': 'Protein'
}


# Json keywords correspond to the keys used in code.
json_keywords = {
    'calories': 'calories',
    'total_fat': 'total_fat',
    'protein': 'protein',
    'carbohydrates': 'carbohydrates',
    'trans_fat': 'trans_fat',
    'poly_fat': 'poly_fat',
    'mono_fat': 'mono_fat',
    'saturated_fat': 'saturated_fat',
    'cholesterol': 'cholesterol',
    'sodium': 'sodium',
    'potassium': 'potassium',
    'fiber': 'fiber',
    'sugars': 'sugars'
}

# First pass at categorization
#    'blurry': 'blurry',
#    'wrinkled': 'wrinkled',
#    'shadowed': 'shadowed',
#    'skewed': 'skewed',
#    'curved': 'curved',
#    'not_bw': 'not_bw',

type_keywords = {
    'color': 'color',
    'skewed': 'skewed',
    'curved': 'curved',
    'lighting': 'lighting',
    'horizontal': 'horizontal'
}

# The Keywords object can be used to access both sets of keywords.
Keywords = {
    'json': json_keywords,
    'label': label_keywords,
    'spec_types': type_keywords,
    'include': 'include',
    'standard': 'standard'
}

# Make the Keywords object attribute-accessible
# e.g. Keywords.label.calories == 'Calories'
Keywords = AttrDict(Keywords)

Keywords.ordered = [
    Keywords.label.calories,
    Keywords.label.total_fat,
    Keywords.label.saturated_fat,
    Keywords.label.trans_fat,
    Keywords.label.poly_fat,
    Keywords.label.mono_fat,
    Keywords.label.cholesterol,
    Keywords.label.sodium,
    Keywords.label.potassium,
    Keywords.label.carbohydrates,
    Keywords.label.fiber,
    Keywords.label.sugars,
    Keywords.label.protein
]
