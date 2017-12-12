
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import os
import pickle
import networkx as nx
from collections import Counter



def partition_girvan_newman(graph):
    v={}
    graphcopy=graph.copy()
    v=nx.edge_betweenness_centrality(graph)
        
    while nx.number_connected_components(graphcopy)<3:           
        maxdepth={}
        maxval=0.0 
        for n in v:         
            if graphcopy.has_edge(n[0],n[1]) or graphcopy.has_edge(n[1],n[0]):
                if float(v[n])>=float(maxval):
                    if float(v[n])==float(maxval):
                        if n[0]<maxdepth['val'][0]:
                            maxdepth['val']=n
                            maxval=float(v[n])
                         
                        if n[0]==maxdepth['val'][0]:
                            if n[1]<maxdepth['val'][1]:
                                maxdepth['val']=n
                                maxval=float(v[n])
                   
                    else:
                        maxdepth['val']=n
                        maxval=float(v[n])
                     
        if graphcopy.has_edge(maxdepth['val'][1],maxdepth['val'][0]):    
                   graphcopy.remove_edge(maxdepth['val'][1],maxdepth['val'][0])
        if graphcopy.has_edge(maxdepth['val'][0],maxdepth['val'][1]):             
                   graphcopy.remove_edge(maxdepth['val'][0],maxdepth['val'][1])
       
           
    components=[]
    for s in nx.connected_component_subgraphs(graphcopy):
          components.append(s)
    return components,graphcopy
    pass




def draw_network(graph,final, filename):
   
    plt.figure(figsize=(12,12))
      
    l={}
    for f in final:
        l[f['screen_name']]=f['screen_name']
    
    
    pos=nx.spring_layout(graph)
    nodes = graph.nodes()
    colors=[]
    for u in nodes:
        if(u =='Google'):
            colors.append('b')
        if(u =='Tesla' ):
            colors.append('r')
        #if(u =='ManUtd'):
            #colors.append('w')
       
    nx.draw_networkx(graph,pos,with_labels=True,labels=l,alpha=.5, width=.6,
                     node_size=100,node_color=colors)
    
    plt.savefig(filename)
    #plt.show()
    ###TODO
    pass



def create_graph(userdata):
    graph = nx.Graph()
    
    for f in userdata:
           for friend in f['connection']:
                    graph.add_edge(f['screen_name'],friend,color='g')
              
    return graph
    ###TODO
    pass


def count_friends(users):
    c = Counter()

    for u in users:
        c.update(u['connection'])
   
    return c
    ###TODO
    pass

        
def main():
    if not os.path.isfile("clusterinput.pkl"):
        print("data not loaded properly")
    else:    
        if os.path.getsize("clusterinput.pkl")==0:
            print("data size not proper")
        else:    
            clusterinput = open("clusterinput.pkl","rb")
            clusteroutput = open("clusteroutput.pkl","wb")
      
            data=pickle.load(clusterinput)
            graph= create_graph(data)

            draw_network(graph,data,'withoutcluster.jpg')       
            clusters,graphcopy= partition_girvan_newman(graph)   
    
            print('first partition: cluster 1 has %d nodes and cluster 2 has %d nodes' %
              (clusters[0].order(), clusters[1].order()))
            print('cluster 1 nodes:')
            print(clusters[0].nodes())
            print('cluster 2 nodes:')
            print(clusters[1].nodes())
            
      
            draw_network(graphcopy,data, "withcluster.jpg")
            pickle.dump(clusters,clusteroutput)
if __name__ == '__main__':
    main()

