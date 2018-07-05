import requests
from bs4 import BeautifulSoup



def get_gig(url, selection):
	link = 'http://www.beat.com.au/gig-guide/' + url
	text = requests.get(link).text
	soup = BeautifulSoup(text, "html.parser")
	tableStats = soup.find("div", {"class" : "w-clearfix archive_wrapper"}) 
	category_list = []
	for item in tableStats.findAll("div", {"class" : "gigguide-genre-collapse"}):
		for category in item.findAll("div", {"class" : "w-clearfix gigguide_genre-gigs"}):
			category = category.findAll("div", {"class" : "w-clearfix archive_node-summary-wrapper " + selection})
			for events in category:
				list = []
				dict = {}
				keys = range(4)
				for info in events.findAll("h5", {"class" : "gigguide_node-summary-detail"}):
					list.append(info.string)
				for i in keys:
					dict[i] = list[i]
				category_list.append(dict)
	return(category_list)


category_attachment = [
        {
            "text": "Choose a category to play ",
            "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
            "color": "#F5D105",
            "attachment_type": "default",
            "callback_id": "game_selection",
            "actions": [
                {
                    "name": "games_list",
                    "text": "Pick a game...",
                    "type": "select",
                    "options": [
                        {
                            "text": "jazz soul funk latin world music",
                            "value": "jazz-soul-funk-latin-world-music"
                        },
                        {
                            "text": "comedy",
                            "value": "comedy"
                        },
                        {
                            "text": "arts theatre burlesque markets",
                            "value": "arts-theatre-burlesque-markets"
                        },
                        {
                            "text": "hip hop r & b",
                            "value": "hip-hop-r-b"
                        },
                        {
                            "text": "house electro trance club nights",
                            "value": "house-electro-trance-club-nights"
                        },
                        {
                            "text": "indie rock pop metal punk covers",
                            "value": "indie-rock-pop-metal-punk-covers"
                        },
                        {
                            "text": "acoustic country blues folk",
                            "value": "acoustic-country-blues-folk"
                        }
                    ]
                }
            ]
        }
    ]


choose_button = [
		{
			"text" : "",
			"color" : "#AD130A",
			"attachment_type" : "default",
			"callback_id" : "try_again",
			"actions" : [
				{
					"name" : "choose",
					"text" : "choose another category",
                    "style" : "danger",
					"type" : "button",
					"value" : "choose",
				},
                {
                    "text" : "Event No. " + "order"


                }
			]
		}
	]
	

paginator = [
        {
            "name" : "Prev",
            "text" : "Prev",
            "type" : "button",
            "value" : "Prev"
        },
        {
            "name" : "Next",
            "text" : "Next",
            "type" : "button",
            "value" : "Next"
        },
        {
                "name" : "choose",
                "text" : "choose another category",
                "type" : "button",
                "value" : "choose",
        },
        {
            "name" : "Sample Tracks",
            "text" : "Sample Tracks",
            "type" : "button",
            "value" : "Sample Tracks"
        }
    ]	


gig_build = {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#F5D105",
            "pretext": "",
            "title": "band",
            "text": "location",
            "fields": [
                {
                    "title": "price",
                    "value": "url"
                }
            ]
        }


def get_band(artist):
    link = 'https://bandcamp.com/search?q=' + artist
    text = requests.get(link).text
    soup = BeautifulSoup(text, "html.parser")
    tableStats = soup.findAll("div", {"class" : "itemurl"}) 
    new_list = []
    for item in tableStats:
        new_list.append(item.text)
    return(new_list[0])

