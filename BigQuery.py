from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client()

def addto(l, type = None):
    for items in l:
        myquery = "INSERT INTO `raycastanedatechx24.ingredient_data.ingredients` (name,type,timestamp) VAlUES (\"%s\", \"%s\",\"%s\")" % (items.lower(), type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        client.query(myquery)


def get(num, type=None):
    query = """
    SELECT *
    FROM `raycastanedatechx24.ingredient_data.ingredients`
    """
    
    if type:
        query += f"WHERE type = '{type}' "
        
    query += """
    ORDER BY timestamp DESC
    """
    
    query_job = client.query(query)
    results = query_job.result()
    

    x = set()
    y = []
    for row in results:
        if row[0] not in x:
            y.append(row)
            x.add(row[0])
        if len(y) == num:
            return y
    return y
            





  
