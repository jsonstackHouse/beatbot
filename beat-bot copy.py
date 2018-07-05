from slackclient import SlackClient
import json
from flask import Flask, request, Response
import requests
from beat_methods import get_gig, choose_button, category_attachment, gig_build, paginator, get_band

server = Flask(__name__)

print("hello")
return Response('it works')

oauth_token = ''
verification_token = ''
bot_token = ''

count = 0
index = 0
selec = ''

@server.route('https://beatscrape.herokuapp.com/test', methods=['GET'])
def local_test():
    return Response('it works')


# nicely formated json printing. Debug only

def print_json(json_data):

    print (json.dumps(
                    json_data,
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                    ))

    

#handle initial slash command

@server.route('/music', methods=['POST'])
def get_gigs():
    global date, index
    token_received = request.form.get('token')
    channel = request.form.get('channel_id')
    date = request.form.get('text')
    trigger_id = request.form.get('trigger_id')
    response_url = request.form.get('response_url')
    headers = {
              'content-type' : "application/json",
              'charset' : "utf-8",
              'Authorization': "Bearer" + oauth_token
              }
    url = "https://slack.com/api/chat.postMessage"
    payload = {
    "response_type": "in_channel",
    "channel" : channel,
    "attachments": category_attachment
}
    if token_received == verification_token:
        if len(date) != 0:
            response = requests.request("POST", url, headers=headers, json=payload)
        else: 
            return("Error: You need to include a date in the form 'YYYY-MM-DD'"), 200
    else:
        return("Incorrect token"), 200

    return Response(), 200

# def Eventinator({a:b,c:d,e:f,g:h}):
#         b = name
#         d = loc
#         f = area
#         h = price


# interactive message button handling

@server.route('/interaction', methods=['POST'])
def button_handler():
    global date
    data = request.form.to_dict()
    inner_data = data['payload']
    inner_data = json.loads(inner_data)
    ts = inner_data['message_ts']
    token_received = inner_data['token']
    payload = {}
    headers = {
    'content-type' : "application/json",
    'charset' : "utf-8",
    'Authorization': "Bearer" + oauth_token
    }   
    url = 'https://slack.com/api/chat.update'
    channel = inner_data['channel']
    channel = channel['id']
    payload = {
    "channel" : channel,
    "ts" : ts
    }

    ## category selector
    if token_received == verification_token:
        global index, selec, count, bandcamp_link
        if inner_data["actions"][0]["name"] == "games_list":
            index = 0
            selection = inner_data['actions']
            selection = selection[0]['selected_options'][0]['value']
            selec = get_gig(date, selection)
            count = len(selec)
            print(count)
            if not selec:
                payload["text"] = "There are no events in this category today"
                payload["attachments"] = choose_button
                response = requests.request("POST", url, headers=headers, json=payload)
    
        
        ## reset category selector
        elif inner_data["actions"][0]["name"] == "choose":
            payload["attachments"] = category_attachment
            response = requests.request("POST", url, headers=headers, json=payload)
            return Response(), 200
        

        elif inner_data["actions"][0]["name"] == "Next":
            print(count)
            print("index is " + str(index))
            index = (index + 1) % int(count)    

        elif inner_data["actions"][0]["name"] == "Prev":
            index = (index - 1) % int(count)

        elif inner_data["actions"][0]["name"] == "Sample Tracks":
            url = "https://slack.com/api/chat.unfurl"
            payload = {
                "channel" : channel,
                "ts" : ts,
                "unfurls": {
        bandcamp_link: {
            "text": "Every day is the test."
        }
    }
    
    }
            response = requests.request("POST", url, headers=headers, json=payload)
            print(response.text)


        object = selec[index]
        name = object[0]
        loc = object[1]
        area = object[2]
        price = object[3]
        if not price:
            price = "Not provided"
        bandcamp_link = get_band(name)

        payload["attachments"] = [
        {
        "color": "#F5D105",
        "pretext": "",
        "fallback" : "fallback_id",
        "callback_id" : "callback_id",
        "title": name,
        "fields" : [
            {
            "title" : "Location",
            "value" : loc
            },
            {
            "title" : "Price",
            "value" : price
            }
        ],
        "attachment_type" : "default",
        "actions" : paginator,
    },
    {
        "text" : "There are " + str(count) + " gigs |" + str(index + 1) + " / " + str(count) + "|"
    }
]
        response = requests.request("POST", url, headers=headers, json=payload)
        return Response(), 200
     
    else:
        print("incorrect token")
        return Response("Incorrect token"), 200


# Message menu handling

@server.route('/options', methods=['POST'])
def options_load():
    pass


# events

@server.route('/events', methods=['POST'])
def events_handler():
    print("hello")
    data = request.data
    data = json.loads(data)
    #print(data)
    #print(type(data))
    try:
        challenge = data["challenge"]
        return Response(challenge), 200
    except:
        return Response("link shared"), 200

    # dict = {"challenge" : challenge}
    # print(dict)
    
    



if __name__== "__main__":
    server.run(debug=True)