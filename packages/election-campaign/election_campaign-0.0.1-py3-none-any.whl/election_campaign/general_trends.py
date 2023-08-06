try:
    import pandas
    import json
    import requests
except:
    print("Please install (pip install) and import the following python library (pandas, json, requests).")

url = "https://research-questions-api.herokuapp.com/generaltrends/"

def get_alltweets(data_type=None):
    """An endpoint to retrieve all tweets in the database, without any filters or limits.

    Parameters
    ----------
    data_type : None, "json" or "pandas.dataframe"
        The preferred data type of the result of the api request, as specified by the end user.

    Returns
    -------
    data
        The result of the api request in the data format specified by the end user.
    """

    url_temp = url
    request = requests.get(url = url_temp)
    data = request.json()
    data = json.dumps(data)
    
    if (data_type == None) or (data_type == "json"):
        return data
    elif data_type == "pandas.dataframe":
        data = pandas.read_json(data)
        return data
    else:
        return ("Incorrect or unavailable specified data type!")


def get_limitedtweets(limit=None, data_type=None):
    """An endpoint to retrieve a limited number of tweets in the database.

    Parameters
    ----------
    limit: int
        The integer value specified by the end user to limit the size of the result of the query.
    data_type : None, "json" or "pandas.dataframe"
        The preferred data type of the result of the api request, as specified by the end user.

    Returns
    -------
    data
        The limited result of the api request in the data format specified by the end user.
    """
    
    if limit == None:
        return ("Please specify an integer value for the limit!")
    elif type(limit) == int:
        url_temp = url + "limit?limit=" + str(limit)
        request = requests.get(url = url_temp)
        data = request.json()
        data = json.dumps(data)
        
        if (data_type == None) or (data_type == "json"):
            return data
        elif data_type == "pandas.dataframe":
            data = pandas.read_json(data)
            return data
        else:
            return ("Incorrect or unavailable specified data type!")
    else:
        return ("Please specify an integer value for the limit!")

def get_filteredtweets(filter=None, data_type=None):
    """An endpoint to retrieve all tweets in the database, filtering the result by tweets using
    whichever keywords or tags specified by the end-user.

    Parameters
    ----------
    filter: str
        The string (keyword) specified by the end user to filter the result of the query by tweets.
    data_type : None, "json" or "pandas.dataframe"
        The preferred data type of the result of the api request, as specified by the end user.

    Returns
    -------
    data
        The filtered result of the api request in the data format specified by the end user.
    """
    
    if filter == None:
        return ("Please specify a string (keyword) for the filter!")
    elif type(filter) == str:
        url_temp = url + "filter?filter=" + filter
        request = requests.get(url = url_temp)
        data = request.json()
        data = json.dumps(data)
        
        if (data_type == None) or (data_type == "json"):
            return data
        elif data_type == "pandas.dataframe":
            data = pandas.read_json(data)
            return data
        else:
            return ("Incorrect or unavailable specified data type!")
    else:
        return ("Please specify a string (keyword) for the filter!")