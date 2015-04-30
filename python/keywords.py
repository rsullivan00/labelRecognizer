from attrdict import AttrDict

# Label keywords correspond to the words found on
# the physical labels themselves.
label_keywords = {
    'calories': 'Calories',
    'total_fat': 'Total Fat',
    'protein': 'Protein',
    'carbohydrates': 'Total Carbohydrate',
    'trans_fat': 'Trans Fat',
    'poly_fat': 'Polyunsaturated Fat',
    'mono_fat': 'Monounsaturated Fat',
    'saturated_fat': 'Saturated Fat',
    'cholesterol': 'Cholesterol',
    'sodium': 'Sodium',
    'potassium': 'Potassium',
    'fiber': 'Dietary Fiber',
    'sugars': 'Sugars'
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

# The Keywords object can be used to access both sets of keywords.
Keywords = {
    'json': json_keywords,
    'label': label_keywords
}
Keywords = AttrDict(Keywords)
