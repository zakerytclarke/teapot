from names_dataset import NameDataset, NameWrapper

# The V3 lib takes time to init (the database is massive). Tip: Put it into the init of your app.
nd = NameDataset()

print(nd.get_top_names(n=10, gender='Male', country_alpha2='US'))
import ipdb
ipdb.set_trace()




extractionms = [
    "first_name",
    "last_name",
    "phone",
    "address",
    "keyword"
]

infos=[
    "url",
    "phone",
    "address",
    "hours":{
        "m",
        "t\"...
    }
    "social_media"
]
