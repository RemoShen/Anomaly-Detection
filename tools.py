from ipaddress import IPv4Network, IPv6Network
from pickle import TRUE
import re

import joblib
from define_occr import sim_ipv4, sim_ipv6, port, para
import csv

import numpy as np
from sklearn import preprocessing
def reads(cath,file):
        file_new = cath+'/'+file
        lines = []
        with open(file_new,'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip('\n')
                lines.append(line)
        return lines
def check_ip(ipaddress):
    try:
        if(IPv4Network(ipaddress).network_address.version == 4):
            return 4
        elif (IPv6Network(ipaddress).network_address.version == 6):
            return 6
    except ValueError:
        return 0
    
    
def check_simip(simipstr):
    if(re.fullmatch(sim_ipv4, simipstr) != None):
        return True
    elif(re.fullmatch(sim_ipv6, simipstr) != None):
        return True
    else: return False

def check_sim_v4(simipstr):
    if(re.fullmatch(sim_ipv4, simipstr) != None):
        return True
    else: return False

def check_sim_v6(simipstr):
    if(re.fullmatch(sim_ipv6, simipstr) != None):
        return True
    else: return False

def check_port(port_str):
    if(re.fullmatch(port, port_str) != None):
        return True
    else: return False
    
    
def check_para(para_str):
    if(para_str not in para):
        return False
    else: return True


def is_num(num_str):
    try:
        float(num_str)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(num_str)
        return True
    except (TypeError, ValueError):
        pass
    return False


def Merge(dict1, dict2): 
    for k, v in dict2.items():
        if k in dict1.keys():
            dict1[k] += v
        else:
            dict1.update({f'{k}': dict2[k]}) 
    return dict1

def kkresu():
    data = []
    with open('vc.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([row[1], row[2], row[3]])
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
    A = np.array(data)
    X=min_max_scaler.fit_transform(A)
    num, dim = X.shape
    clf = Kmeans(k=7)
    
    joblib.dump(clf, 'set.pkl')


def SumDict(myDict): 
    sum = 0
    for i in myDict: 
        sum = sum + myDict[i] 
    return sum

def normalize(X, axis=-1, p=2):
    lp_norm = np.atleast_1d(np.linalg.norm(X, p, axis))
    lp_norm[lp_norm == 0] = 1
    return X / np.expand_dims(lp_norm, axis)


def euclidean_distance(one_sample, X):
    one_sample = one_sample.reshape(1, -1)
    X = X.reshape(X.shape[0], -1)
    distances = np.power(np.tile(one_sample, (X.shape[0], 1)) - X, 2).sum(axis=1)
    return distances


class Kmeans():
    def __init__(self, k=7, max_iterations=500, varepsilon=0.0001):
        self.k = k
        self.max_iterations = max_iterations
        self.varepsilon = varepsilon

    def init_random_centroids(self, X):
        n_samples, n_features = np.shape(X)
        centroids = np.zeros((self.k, n_features))
        for i in range(self.k):
            centroid = X[np.random.choice(range(n_samples))]
            centroids[i] = centroid
        return centroids

    def _closest_centroid(self, sample, centroids):
        distances = euclidean_distance(sample, centroids)
        closest_i = np.argmin(distances)
        return closest_i

    def create_clusters(self, centroids, X):
        n_samples = np.shape(X)[0]
        clusters = [[] for _ in range(self.k)]
        for sample_i, sample in enumerate(X):
            centroid_i = self._closest_centroid(sample, centroids)
            clusters[centroid_i].append(sample_i)
        return clusters

    def update_centroids(self, clusters, X):
        n_features = np.shape(X)[1]
        centroids = np.zeros((self.k, n_features))
        for i, cluster in enumerate(clusters):
            centroid = np.mean(X[cluster], axis=0)
            centroids[i] = centroid
        return centroids

    def get_cluster_labels(self, clusters, X):
        y_pred = np.zeros(np.shape(X)[0])
        for cluster_i, cluster in enumerate(clusters):
            for sample_i in cluster:
                y_pred[sample_i] = cluster_i
        return y_pred

    def predict(self, X):
        centroids = self.init_random_centroids(X)

        for _ in range(self.max_iterations):
            clusters = self.create_clusters(centroids, X)
            former_centroids = centroids
            centroids = self.update_centroids(clusters, X)
            diff = centroids - former_centroids
            if diff.any() < self.varepsilon:
                break

        return self.get_cluster_labels(clusters, X)
