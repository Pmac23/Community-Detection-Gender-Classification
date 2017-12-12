
# coding: utf-8

# In[2]:


from TwitterAPI import TwitterAPI,TwitterOAuth

import pickle
import time
import sys

from collections import Counter
import requests
consumer_key = 'jJPw0zqd4AZ38yHdEAaFM8k6s'
consumer_secret = 'Fzb1AcxX1w5omt3RdDrAgrhtq8a59POP83uSZzb7ljzqL1gtzS'
access_token = '147889345-6j36hcWF7mYT9ElW6wgBBf7vA6Xsme8qYSqTuHHH'
access_token_secret = 'xCtJBsT9opM114dWruZ91tGdH3wqS2BYXdCfgqDEIVDQj'

def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def get_census_names():
    males = requests.get('http://www2.census.gov/topics/genealogy/1990surnames/dist.male.first').text.split('\n')
    females = requests.get('http://www2.census.gov/topics/genealogy/1990surnames/dist.female.first').text.split('\n')
    males_pct = dict([(m.split()[0].lower(), float(m.split()[1]))
                  for m in males if m])
    females_pct = dict([(f.split()[0].lower(), float(f.split()[1]))
                    for f in females if f])
    male_names = set([m for m in males_pct if m not in females_pct or
                  males_pct[m] > females_pct[m]])
    female_names = set([f for f in females_pct if f not in males_pct or
                  females_pct[f] > males_pct[f]])    
    return male_names, female_names


def count_friends(users):
    c = Counter()

    for u in users:
        c.update(u['connection'])
   
    return c
    ###TODO
    pass

def robust_request(twitter, resource, params, max_tries=5):
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)

def get_users(twitter, screen_names):
    response=robust_request(twitter,"users/lookup", {'screen_name': screen_names})
    user_data=[]
    for r in response:
        user_data.append(r)
    return user_data
    ###TODO
    pass



def get_followers(twitter,users,countval):
    for val in users:  
        followlist=[]
        request =robust_request(twitter,'followers/list', {'screen_name': val['screen_name'],'count':countval})           
        for s in request: 
            if s['screen_name'] not in followlist:
                followlist.append(s['screen_name'])
        val.update({'connection':followlist})            
    return users
  
def get_friends(twitter,users,countval):
    namelist=[]
    for val in users: 
        followlist=[]  
        request =robust_request(twitter,'friends/list', {'screen_name': val['screen_name'],'count':countval})           
        for s in request: 
            if s['screen_name'] and s['screen_name'] not in followlist:
                followlist.append(s['screen_name'])
        if 'connection' in val:             
            val['connection']= val['connection']+followlist                               
        else:
            val['connection']=followlist
    
    
    return users
              
        
def main():
    cluster_ip = open("clusterinput.pkl","wb")
    classify_ip=open("classifyinput.pkl","wb")
    data_male= open("male.pkl","wb")
    data_female= open("female.pkl","wb")
    data=open("countdata.pkl","wb")
    
    tweetlist=[]
    #o = TwitterOAuth.read_file('credentials.txt')
    
    
    twitter = get_twitter()
    print("Connection established")
    screen_names=['Google', 'Tesla']
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    users =get_followers(twitter,users,50)
    print("follower list for given screen_names")
    users=get_friends(twitter,users,50)   
    print("friend list of given screen_names")
 
    since_id=0
    namelist=[]
    
    while len(tweetlist)<50:
        for data in screen_names: 
            request =robust_request(twitter,'search/tweets', {'q': '@'+data,'count':80,'since_id':since_id,"lang": "en"})           
            for r in request:
                if(r['user']['screen_name'] not in namelist):  
                    tweetlist.append(r)
                    namelist.append(r['user']['screen_name'])
                    print(len(tweetlist))
                    if(since_id<r['id']):
                        since_id=r['id']
    #print(len(tweetlist))       
    print("tweetlist for screen_names done")
    pickle.dump(tweetlist, classify_ip)
    male_names, female_names = get_census_names() 
     
    pickle.dump(male_names,data_male)
    pickle.dump(female_names,data_female)
 
    f_counts = count_friends(users)
    datalist=[]   
    for user in users:      
        for friend in user['connection']:    
            if(f_counts[friend]>1 and friend not in datalist):
                datalist.append(friend)
           
    user1 = sorted(get_users(twitter, datalist), key=lambda x: x['screen_name'])      
    user1=get_friends(twitter,user1,20)
    print("friendlist for followers done")
 
    users.extend(user1)
     
    pickle.dump(users, cluster_ip)
    
      
if __name__ == '__main__':
    main()

