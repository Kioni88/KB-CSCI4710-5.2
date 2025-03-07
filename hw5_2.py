(No subject)

Benally, Kioni


​
Walton, Cayden M.
​
from SPARQLWrapper import SPARQLWrapper, JSON
import networkx as nx
import matplotlib.pyplot as plt
import spacy

nlp = spacy.load("en_core_web_trf")

# Setup the SPARQLWrapper instance
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Define the SPARQL query
sparql.setQuery("""
    SELECT DISTINCT ?researcher ?researcherLabel ?affiliation 
           ?affiliationLabel ?advisor ?advisorLabel
    WHERE {
        ?researcher wdt:P106 wd:Q82594. 
        ?researcher wdt:P108 ?affiliation.
        ?researcher wdt:P184 ?advisor.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 30
""")

# Set the return format to JSON
sparql.setReturnFormat(JSON)

# Execute the query and convert the result to JSON
results = sparql.query().convert()

# Access the bindings from the result
bindings = results["results"]["bindings"]

# Extract the headers from the first result
headers = bindings[0].keys()

# Format headers by replacing 'Label' with 'Name'
formated_headers = [
    header.replace("Label", "Name") if "Label" in header else header for header in headers
]

# Print formatted headers
print(", ".join(formated_headers))

G = nx.DiGraph()
for result in bindings:
    researcher = result["researcherLabel"]["value"].strip()
    affiliation = result["affiliationLabel"]["value"].strip()
    advisor = result["advisorLabel"]["value"].strip()

    # Add edges between researcher, affiliation, and advisor
    G.add_edge(researcher, affiliation, label="affiliation")
    G.add_edge(researcher, advisor, label="advisor")

successors = list(G.successors("Alan Kay"))
subgraph_nodes = ["Alan Kay"] + successors
print(subgraph_nodes)
J = G.subgraph(subgraph_nodes).copy()

pos = nx.spring_layout(J, seed=42)

nx.draw(J, pos, with_labels=True, node_color="skyblue", node_size=2008,font_size = 12, font_color = "black", font_weight="bold", arrows = True)

edge_labels = nx.get_edge_attributes(J,"label")
nx.draw_networkx_edge_labels(J,pos,edge_labels=edge_labels)

for node in J.nodes:
    print(f"Node: {node}")

ancestors = list(nx.ancestors(G,"Viewpoints Research Institute"))
for node in ancestors:
    print(f"Node: {node}")

plt.show()
