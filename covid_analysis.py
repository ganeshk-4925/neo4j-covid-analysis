from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt

# ---- Update with your Neo4j Aura credentials ----
uri = "neo4j+s://8a33168f.databases.neo4j.io"
username = "neo4j"
password = "p24MvltUmWFae8yeshIVwoKqmcJafew-Twd9BgpDWMQ"
# -------------------------------------------------

driver = GraphDatabase.driver(uri, auth=(username, password))

def run_query(tx, query):
    result = tx.run(query)
    return pd.DataFrame([dict(record) for record in result])

# ---- Choose ONE of these queries at a time ----

# 1. Top 10 Countries by Total Confirmed Cases
query = """
MATCH (c:Country)-[:HAS_PROVINCE]->(p:Province)-[r:REPORTED_ON]->(d:Day)
RETURN c.name AS Country, SUM(r.confirmed) AS TotalConfirmed
ORDER BY TotalConfirmed DESC
LIMIT 10
"""

# 2. Global Confirmed Cases Over Time
# query = """
# MATCH (:Province)-[r:REPORTED_ON]->(d:Day)
# RETURN d.date AS Date, SUM(r.confirmed) AS GlobalConfirmed
# ORDER BY Date
# """

# 3. Confirmed Cases Over Time for Selected Countries
# query = """
# MATCH (c:Country)-[:HAS_PROVINCE]->(p:Province)-[r:REPORTED_ON]->(d:Day)
# WHERE c.name IN ['US', 'India', 'Brazil', 'Russia', 'France']
# RETURN c.name AS Country, d.date AS Date, SUM(r.confirmed) AS Confirmed
# ORDER BY d.date
# """

with driver.session() as session:
    df = session.execute_read(run_query, query)

# ---- Visualization ----

if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])

    if 'Country' in df.columns:
        pivot = df.pivot(index='Date', columns='Country', values='Confirmed').fillna(0)
        pivot.plot(figsize=(14, 6), title="Confirmed Cases Over Time (Selected Countries)")
        plt.xlabel("Date")
        plt.ylabel("Confirmed Cases")
    else:
        plt.figure(figsize=(12, 6))
        plt.plot(df['Date'], df['GlobalConfirmed'], color='darkgreen')
        plt.title("Global Confirmed COVID-19 Cases Over Time")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Confirmed Cases")
else:
    plt.figure(figsize=(10, 6))
    plt.barh(df['Country'], df['TotalConfirmed'], color='coral')
    plt.xlabel("Total Confirmed Cases")
    plt.ylabel("Country")
    plt.title("Top 10 Countries by Confirmed COVID-19 Cases")
    plt.gca().invert_yaxis()

plt.tight_layout()
plt.grid(True)
plt.show()
