import pickle

with open('info.pkl', 'rb') as f:
    i = pickle.load(f)
    print(i)