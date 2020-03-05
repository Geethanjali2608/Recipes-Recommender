#recipe recommender


import pandas as pd
import numpy as np
import heapq
import pickle

filename = 'recipes_recommender_model.sav'
rr_model = pickle.load(open(filename, 'rb'))

recipes_df = pd.read_csv('datasets/rr-recipes.csv')
users_df = pd.read_csv('datasets/rr-users.csv')
ratings_df = pd.read_csv('datasets/rr-ratings.csv')

def get_r(user_id):
    # Select which system to use. Due to memory constraints, item based is the only viable option
    recommender_system = rr_model

    # N will represent how many items to recommend
    N = 200

    # The setting to a set and back to list is a failsafe.
    rated_items = list(set(ratings_df.loc[ratings_df['user'] == user_id]['item'].tolist()))

    # Self explanitory name
    all_item_ids = list(set(ratings_df['item'].tolist()))

    # New_items just represents all the items not rated by the user
    new_items = [x for x in all_item_ids if x not in rated_items]

    # Estimate ratings for all unrated items
    predicted_ratings = {}
    for item_id in new_items:
        predicted_ratings[item_id] = recommender_system.predict(user_id, item_id).est
        pass

    # Get the item_ids for the top ratings
    recommended_ids = heapq.nlargest(N, predicted_ratings, key=predicted_ratings.get)
    recommended_ids = sorted(recommended_ids)

    # predicted_ratings
    recommended_df = recipes_df.loc[recipes_df['recipe_id'].isin(recommended_ids)].copy()
    recommended_df.set_index('recipe_id', inplace=True)
    recommended_df.insert(1, 'pred_rating', np.zeros(len(recommended_ids)))
    # recommended_df = recipes_df.copy()
    for idx,item_id in enumerate(recommended_ids):
        recommended_df.iloc[idx, recommended_df.columns.get_loc('pred_rating')] =predicted_ratings[item_id]
        pass

    return recommended_df.head(N).sort_values('pred_rating', ascending=False)

# ask the user for input
# get their ID number
user_id = int(input('Enter user id: '))
# get them to list some ingredients, currently it breaks if the second or next ingredient is not there
ingredient_list = input('Enter the ingredients separated by commas that you have on hand: ')
# split the input up into an array for the loop
items = np.array(ingredient_list.split(','))
'''# get the lowest rating
rating = int(input('Enter the lowest rating you\'ll accept: '))'''
# get their user name
user_name = users_df.loc[users_df['user_id'] == user_id]

# print some details
print(f'\nWelcome back {user_name.iloc[0,1]}')
print(f'Your selected ingredients: {ingredient_list}')
print('\nHere are your recommendations.')
test = get_r(user_id)
for item in items:
    test = test[test['ingredients'].str.contains(item)]

#test = test[test['pred_rating'] >= rating]
test
