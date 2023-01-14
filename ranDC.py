import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from struct import pack
import pickle as pk
from hmmlearn import hmm
from sklearn.decomposition import PCA
from sklearn import tree
from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP , TCP, UDP


models = pk.load(open("pickle/models.pickle", 'rb'))
dt = pk.load(open("pickle/DT_pca.pickle", 'rb'))
data = pk.load(open('pickle/data.pickle', 'rb'))
labels = pk.load(open('pickle/labels.pickle', 'rb'))
obs = pk.load(open('pickle/obs.pickle', 'rb'))
all_obs = pk.load(open('pickle/all_obs.pickle', 'rb'))

class Pcaper:
    def __init__(self):
        self.ip_list = self.tcp_list = self.eth_list = []
        self.ip_list = [field.name for field in IP().fields_desc]
        self.tcp_list = [field.name for field in TCP().fields_desc]
        self.eth_list = [field.name for field in Ether().fields_desc]
        self.udp_list = [field.name for field in UDP().fields_desc]
        try:
            self.ip_list.remove("options")
            self.tcp_list.remove("options")
            self.eth_list.remove("options")
            self.udp_list.remove["options"]
        except:
            pass
        self.tot_col = self.eth_list + self.ip_list + ["time"] + self.tcp_list

    def run(self,filepath:str):
        self.pack = rdpcap(filepath)
        df = pd.DataFrame(columns = self.tot_col)
        for pa in self.pack:
            try:
                if pa[ARP]:
                    continue
            except:
                pass
            field_val = []
            for field in self.eth_list:
                field_val.append(pa[Ether].fields[field])
            for field in self.ip_list:
                field_val.append(pa[IP].fields[field])
            field_val.append(pa.time)
            t = type(pa[IP].payload)
            for field in self.tcp_list:
                try:
                    field_val.append(pa[t].fields[field])
                except:
                    field_val.append(None)
            me = pd.DataFrame([field_val],columns=self.tot_col)
            df = pd.concat([df,me],axis=0)
        return df
        # df.to_csv(path_or_buf=csvname+".csv",index=False)


def proc(pcap):
    obj = Pcaper()
    df = obj.run(pcap)
    df = df.convert_dtypes()
    df = pd.get_dummies(df, columns=['type','flags','version','ihl','tos','proto','dataofs','reserved','urgptr'])
    if 'src.1' in df.columns:
        df =df.drop(columns=['src.1', 'dst.1'])
    if 'src' in df.columns:
        df =df.drop(columns=['src', 'dst'])
    df = df.dropna()
    pca = PCA(n_components=3)
    fit = pca.fit_transform(df)
    df = pd.DataFrame(fit)
    df.columns = ['transformed_f1', 'transformed_f2', 'transformed_f3']
    return df


def hmmproc(df):
    data = np.zeros((len(df), 3))
    maxsize = -1

    for i, row in df.iterrows():
        row = list(row)
        d = ' '.join([str(elem) for elem in row])
        d = np.fromstring(d, sep=' ')
        data[i, :d.shape[0]] = d
        if d.shape[0] > maxsize:
            maxsize = d.shape[0]
        data = data[:, :maxsize]
    all_obs = []
    for i in range(data.shape[0]):
        n_dim = 2
        obs = np.zeros((n_dim, d.shape[0]))
        for r in range(d.shape[0]):
            obs = data
        if i % 10000 == 0:
            print("Processed obs %s" % i)
        all_obs.append(obs)
        
    # all_obs = np.atleast_3d(all_obs)
    for n,i in enumerate(data):
        data[n] /= data[n].sum(axis=0)
    
    return data, obs, all_obs


def MLclass(df):
    pred = dt.predict(df)
    return pred


def GMMHMM(X_test):
    data, obs, all_obs = hmmproc(X_test)
    logprob = np.array([[m.score(i.reshape(1,-1)) for i in data] for m in models])
    y_hat = np.argmax(logprob, axis=0)
    return y_hat


def result(pred):
    ll = {}
    maxclass = []
    for val in pred:
        if val not in ll:
            ll[val] = 1
        else:
            ll[val] += 1
    for x in ll:
        maxclass.append([ll[x], x])    
    return [ll, max(maxclass)[1]]