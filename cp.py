import pickle
with open("info.pkl", "rb") as f:
    print(pickle.load(f))