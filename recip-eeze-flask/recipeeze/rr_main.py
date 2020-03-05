#recipe recommender
import pandas as pd
import numpy as np
import heapq
import pickle

filename = 'recipeeze/recipes_recommender_model.sav'
rr_model = pickle.load(open(filename, 'rb'))

recipes_df = pd.read_csv('recipeeze/datasets/rr-recipes.csv')
users_df = pd.read_csv('recipeeze/datasets/rr-users.csv')
ratings_df = pd.read_csv('recipeeze/datasets/rr-ratings.csv')

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

def set_up_rr(user_id,ingredient_list):
    # split the input up into an array for the loop
    items = ingredient_list.split(',')
    rr_list = get_r(user_id)
    for j in range(0,len(items)):
        rr_list = rr_list[rr_list['ingredients'].str.contains(items[j])]
    return rr_list
