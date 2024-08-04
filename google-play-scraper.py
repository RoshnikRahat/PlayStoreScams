from google_play_scraper import app,reviews_all,permissions
import pandas  as pd
 

# data analysis and cleaning
df=pd.read_excel("AppData.xlsx")


def scrape_info(app_id):
    """This is used to scrape all the data about the application including it's name, package name reviews etc"""
    try:

        app_info = app(app_id)
        return app_info
    except Exception as e:
        print("Failed for ", app_id)
        print(e)

# 
def scrape_permissions(app_id):
    """Returns in a list of dicts all the information associated with the app"""
    try:
        return permissions(app_id,country='pk')
    except Exception as e:
        print("Failed for ", app_id)
        print(e)

def scrape_allReviews(app_id):
    "Includes rating, id, username, profilepic"
    try:
        # Replace this with the actual function to get reviews
        reviews = reviews_all(app_id, sleep_milliseconds=0)
        
        # Add the app_id to each review and collect all reviews
        for review in reviews:
            review['app_id'] = app_id
        
        return reviews
    except Exception as e:
        print("Failed for", app_id)
        print(e)
        return []



df["PlayStore_Info"]=df["Package_Name"].apply(scrape_info)
print(df["PlayStore_Info"])

df["PlayStore_Permissons"]=df["Package_Name"].apply(scrape_permissions)
print(df["PlayStore_Permissons"])

df.to_excel("AppInfoAndPermissions.xlsx")



#Initialize an empty list to collect all reviews
all_reviews = []


# Iterate through each row in the dataframe
for index, app_id in enumerate(df['Package_Name']):
    print(index, app_id)
    reviews = scrape_allReviews(app_id)
    if reviews:
        print(reviews[0])
    
    if reviews:
        print("And adding to the combined dataframe")
        all_reviews.extend(reviews)  # Add the reviews to the list

# Convert the combined reviews list to a DataFrame
combined_df = pd.DataFrame(all_reviews)

# Save the combined DataFrame to a CSV file or any other desired format
combined_df.to_csv('combined_reviews.csv', index=False)

print("All reviews have been combined and saved.")