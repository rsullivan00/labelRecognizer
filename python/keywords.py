from attrdict import AttrDict

label_keywords = {'calories':'Calories', 'total_fat':'Total Fat', 'protein':'Protein', 'carbohydrates': 'Total Carbohydrates'}
json_keywords = {'calories':'calories', 'total_fat':'total_fat', 'protein':'protein', 'carbohydrates': 'carbohydrates'}
Keywords = {'json':json_keywords, 'label':label_keywords}
Keywords = AttrDict(Keywords)
