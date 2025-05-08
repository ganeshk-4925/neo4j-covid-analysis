from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt

# Replace with your actual credentials
uri = "neo4j+s://8a33168f.databases.neo4j.io"
username = "neo4j"
password = "p24MvltUmWFae8yeshIVwoKqmcJafew-Twd9BgpDWMQ"

driver = GraphDatabase.driver(uri, auth=(username, password))

# Example query: Get top 10 provinces with highest confirmed cases
query = """
MATCH (p:Province)-[r:REPORTED_ON]->(d:Day)
RETURN p.name AS Province, SUM(r.confirmed) AS TotalConfirmed
ORDER BY TotalConfirmed DESC
LIMIT 10
"""

def run_query(tx, query):
    result = tx.run(query)
    return pd.DataFrame([dict(record) for record in result])

with driver.session() as session:
    df = session.execute_read(run_query, query)

print(df)

# Plotting
plt.figure(figsize=(10, 6))
plt.barh(df['Province'], df['TotalConfirmed'], color='teal')
plt.xlabel("Total Confirmed Cases")
plt.ylabel("Province")
plt.title("Top 10 Provinces by Confirmed COVID-19 Cases")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
