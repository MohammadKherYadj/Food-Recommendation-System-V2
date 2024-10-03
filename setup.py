import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix


users = pd.read_csv("Data/users.csv")
foods =  pd.read_csv("Data/foods.csv")
ratings = pd.read_csv("Data/ratings.csv")

foods_with_ratings = ratings.merge(foods,on="Food_ID")

number_of_ratings = foods_with_ratings.groupby("Description")["Rating"].count().reset_index().rename(columns={
    "Rating" : "Number Of Ratings"
}
)

final_ratings = number_of_ratings.merge(foods_with_ratings,on="Description")

pivot_food = final_ratings.pivot_table(columns="User_ID",index="Description",values="Rating")

pivot_food.fillna(0,inplace=True)

food_sparse = csr_matrix(pivot_food)

model = NearestNeighbors(algorithm="brute")

model.fit(food_sparse)

def Recommand_Food(food_name):
    suggestion_food_list = []
    try:
        food_id = np.where(pivot_food.index == food_name)[0][0]
        destance,suggestion = model.kneighbors(pivot_food.iloc[food_id,:].values.reshape(1,-1),n_neighbors=6)
        for i in range(len(suggestion)):
            suggestion_food = pivot_food.index[suggestion[i]]
            for j in suggestion_food:
                if j == food_name:
                    continue
                else:             
                    suggestion_food_list.append(j)    
        return suggestion_food_list   
    except:
        return {"message":"No Data Recommanded"}   

def return_by_rating(food_rating):
    data = foods_with_ratings[foods_with_ratings["Rating"] == food_rating]
    result = data["Description"].values.tolist()
    return {"By Rating":result}

Name = "Milk, calcium fortified, whole"
print(Recommand_Food(Name))