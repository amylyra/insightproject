from elasticsearch import Elasticsearch

endpoint = ('https://search-insightprojecttest-qcbe6ffjwxsdscktijg6uragwi.us-west-1.es.amazonaws.com')
product_index = 'product'
ingredient_index = 'ingredient_2'

def init_search(endpoint=endpoint):
    es = Elasticsearch(endpoint)
    return es

def product_search(brand,name, es, index=product_index):
    """Give single product brand/ name, return Product(brand,name,ingredients,listPrice,size,rating)
    """
    query = {
      "from": 0,
      "size": 1,
      "query": {
        "bool": {
          "must": [
            { "match": { "brand": brand}}, 
            { "match": { "name": name}}  
          ]
              
        }
      }
    }
    try:
        result = es.search(index=index,
                           body=query
                          )['hits']['hits'][0]['_source']
        brand = result['brand']
        name = result['name']
        ingredients = result['ingredients']
        listPrice = result['listPrice']
        size = result['size']
        rating = result['rating']
        return(brand, name, ingredients, listPrice, size, rating)
    except:
        return None
    
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
