import pickle

with open('exper_results.pkl', 'rb') as handle:
    b = pickle.load(handle)
print(b)
