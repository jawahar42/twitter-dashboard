import tweepy
from tweepy import OAuthHandler

from flask import Flask
from flask import json
from flask import Response
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/user/*": {"origins": "*"}}) 


class TwitterClient(object):
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'xvEAK72HXroHyhTk3dTuVFTig'
        consumer_secret = 'U89hJup3zCLAOkH2YarbCkp9yhrgBvNeDSI6ZgKnc2PHT1nO0T'
 
        # attempt authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

 
api = TwitterClient().api

@app.route('/user/<username>')
def show_user_profile(username):
    try :
        user_json = api.get_user(username)._json
    except tweepy.TweepError as e:
        if e.api_code == 63 or e.api_code == 50:
           return Response(status = 404)
        else:
            print(e.reason)
            raise

    response = Response(
        response=json.dumps(user_json),
        status=200,
        mimetype='application/json'
    )
    
    return response