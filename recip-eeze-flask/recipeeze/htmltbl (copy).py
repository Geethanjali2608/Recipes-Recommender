import numpy as np
def mk_tbl(rows):
    #this is for creating dynamic tables
    for row in rows:
        arr = []
        arr.append(row)
        '''title = row['title']
        ready_time = row['ready_time']
        prep_time = row['prep_time']
        cook_time = row['cook_time']
        url = row['url']
        photo_url = row['photo_url']'''

        '''<tr><td><img src=photo_url alt="recipe photo" width="100" height="60"/></td>
        <td><input type="text" name="title" value="title" size="20" /></td>
        <td><input type="text" name="ready_time" value="ready_time" size="10" /></td>
        <td><input type="text" name="prep_time" value="prep_time" size="5" /></td>
        <td><input type="text" name="cook_time" value="cook_time" size="5" /></td>
        <td><a href=url target="_blank">recipe link</a></td></tr>'''
        return arr
