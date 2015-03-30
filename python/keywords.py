from attrdict import AttrDict

# Label keywords correspond to the words found on 
# the physical labels themselves.
label_keywords = {'calories':'Calories', 'total_fat':'Total Fat', 'protein':'Protein', 'carbohydrates': 'Total Carbohydrates'}

# Json keywords correspond to the keys used in code.
json_keywords = {'calories':'calories', 'total_fat':'total_fat', 'protein':'protein', 'carbohydrates': 'carbohydrates'}

# The Keywords object can be used to access both sets of keywords.
Keywords = {'json':json_keywords, 'label':label_keywords}
Keywords = AttrDict(Keywords)
