import requests


# Headers info for HTTP requests
headers = {"User-Agent":
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" +
           "(KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"}


# Function to retrieve JSON from a GET request.
def getJSON(url):
    # Variable stores a URL's data
    # URL should be a JSON endpoint, preferably
    r = requests.get(url, headers=headers)
    # Convert it into a JSON format
    data = r.json()
    return data


# Function to find post links from data.
def getLinks(data):
    # List to populate later on.
    links = []
    # Variable to easily access where reddit posts are stored
    posts = data["data"]["children"]
    # Iterate through posts to find their title and their link.
    for post in posts:
        # Save relavant data into variable
        entry = {"title": post["data"]["id"], "url": post["data"]["url"]}
        # Populate our own list with skimmed information.
        links.append(entry)
    return links


# Function that will go through our list on links and download them.
def downloadLinks(links):
    # Iterate through the list of links
    for x in links:
        # Make sure the link ends with a JPG
        # Don't want to download a not-picture
        if x["url"].lower().endswith(tuple(['.jpg'])):
            # Save it with the title.jpg in a downloads path
            folder = 'downloads/' + x["title"] + '.jpg'
            # GET request of the photo link
            dlGet = requests.get(x["url"], headers=headers)
            # Open a path to create/write file.
            # It's being written in binary.
            with open(folder, 'wb') as f:
                try:
                    f.write(dlGet.content)
                    # Close it when you're done.
                    f.close()
                    # Feedback in Terminal about progress.
                    print('Successfully Downloaded %s!' % x["title"])
                except:
                    print('Download for %s failed. Moving on..' % x["title"])
                    pass
        else:
            pass
    return


# Terminal INterface
def interfaceDownloads():
    # Save subreddit from user input
    subreddit = input('From which subreddit frontpage' +
                      'would you like to download pictures from? ')
    # Construct subreddit path from user input
    path = 'https://www.reddit.com/r/' + subreddit + '/.json'
    try:
        # Check to see if a Subreddit exists first.
        if requests.get(path, headers=headers).status_code == 200:
            # If it's a go, go through functions defined.
            print('Subreddit exists! Retrieving Front Page...')
            data = getJSON(path)
            print('Getting Links...')
            links = getLinks(data)
            print('Downloading Pictures...')
            downloadLinks(links)
            print('Downloads complete!')
        # If no-go:
        else:
            # Retrieve the status code the input returned
            error_code = requests.get(path).status_code
            # Print input and the error code it returned
            print(subreddit + ' failed with the error code: ' +
                  str(error_code))
            # Restart prompt
            return interfaceDownloads()
    # Any other error for any other reason
    # Should print in the terminal
    # And restart the prompt.
    except Exception as error:
        print('Something went wrong...')
        print(error)
        return interfaceDownloads()

interfaceDownloads()
