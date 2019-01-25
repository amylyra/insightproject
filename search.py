from elasticsearch import Elasticsearch

endpoint = ('https://search-insightprojecttest-qcbe6ffjwxsdscktijg6uragwi.us-west-1.es.amazonaws.com')
ingredient_index = 'ingredient_2'

def init_search(endpoint=endpoint):
    es = Elasticsearch(endpoint)
    return es

def ingredient_search(ing_name, es, index=ingredient_index):
    """Give single ingredient name, return Ingredient(name, about, safty, function)
    """
    query = {
      "from": 0,
      "size": 1,
      "query": {
        "bool": {
          "should": [
            {
              "term": {
                "name.keyword": {
                  "value": ing_name,
                  "boost": 100
                }
              }
            },
            {
              "match_phrase": {
                "name": {
                  "query": ing_name,
                  "boost": 50
                }
              }
            },
            {
              "match": {
                "name": {
                  "query": ing_name,
                  "operator": "and",
                  "boost": 20
                }
              }
            }
          ]
        }
      }
    }
    try:
        result = es.search(index=index,
                           body=query
                          )['hits']['hits'][0]['_source']
        name = result['name']
        about = result['About']
        safety = result['Overall Hazard']
        function = result['Function(s)']
        return(name, about, safety, function)
    except:
        return None
