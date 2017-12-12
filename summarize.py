
# coding: utf-8

# In[4]:



import pickle
from collections import Counter

def main():
    f=open("summary.txt","w", encoding="utf8", newline = '')
    clusterinput = open("clusterinput.pkl","rb")
    users=pickle.load(clusterinput) 
    classifyinput = open("classifyinput.pkl","rb")
    messagedata=pickle.load(classifyinput)
    counterdata=Counter()
    for val in users:        
        counterdata.update(val['screen_name'])
        counterdata.update(val['connection'])
    
    f.write("Number of users collected "+str(len(users)))
    f.write("\n")
    f.write("Number of connection users collected "+str(len(counterdata)))
    f.write("\n")
    f.write("Number of messages collected "+str(len(messagedata)))
    f.write("\n")
    cluster_op = open("clusteroutput.pkl","rb")
    clusters=pickle.load(cluster_op)
    total=0
    for i in range(0,len(clusters)):
        total=total+len(clusters[i])
 
    f.write("Number of communities discovered "+str(len(clusters)))
    f.write("\n")
    f.write("Average number of users per community "+str(total/len(clusters)))
    f.write("\n")
    classify_op = open("classifyoutput.pkl","rb")
    classify=pickle.load(classify_op)
    c_counter=Counter()
    c_counter.update(classify)
    f.write("Number of instances for class 0 -Male found "+str(c_counter[0]))
    f.write("\n")
    f.write("Number of instances for class 1 -Female found "+str(c_counter[1]))
    f.write("\n")
    instance0 = open("classifyoutputinstance0.pkl","rb")
    classify=pickle.load(instance0)
    f.write("Example of class 0 "+str( classify[0][1]))
 
    instance0 = open("classifyoutputinstance0.pkl","rb")
    classify=pickle.load(instance0)
    print(classify)
    instance1 = open("classifyoutputinstance1.pkl","rb")
    classify=pickle.load(instance1)
    print(classify)
    f.write("\n") 
    f.write("Example of class 1 "+str(classify[0][1]))
if __name__ == '__main__':
    main()

