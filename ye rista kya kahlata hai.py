# import networkx as nx
# import matplotlib.pyplot as plt

# # 1. Define the tabular data (Source, Family Line, Relationship, Target)
# # Extracted directly from the previous table's descriptions
# family_table_data = [
#     # Generation 1
#     ("Vishambhar", "Maheshwari", "father_of", "Akshara (Gen 1)"),
#     ("Rajshri", "Maheshwari", "mother_of", "Akshara (Gen 1)"),
#     ("Rajshekhar", "Singhania", "father_of", "Naitik"),
#     ("Gayatri", "Singhania", "mother_of", "Naitik"),
#     ("Naitik", "Singhania", "husband_of", "Akshara (Gen 1)"),
    
#     # Generation 2
#     ("Akshara (Gen 1)", "Singhania", "mother_of", "Naira"),
#     ("Naitik", "Singhania", "father_of", "Naira"),
#     ("Manish", "Goenka", "father_of", "Kartik"),
#     ("Soumya", "Goenka", "mother_of", "Kartik"),
#     ("Kartik", "Goenka", "husband_of", "Naira"),
    
#     # Generation 3
#     ("Naira", "Goenka", "mother_of", "Akshara (Gen 3)"),
#     ("Kartik", "Goenka", "father_of", "Akshara (Gen 3)"),
#     ("Harshvardhan", "Birla", "father_of", "Abhimanyu"),
#     ("Manjari", "Birla", "mother_of", "Abhimanyu"),
#     ("Abhimanyu", "Birla", "first_husband_of", "Akshara (Gen 3)"),
#     ("Abhinav", "Sharma", "second_husband_of", "Akshara (Gen 3)"),
    
#     # Generation 4
#     ("Akshara (Gen 3)", "Sharma", "mother_of", "Abhira"),
#     ("Abhinav", "Sharma", "father_of", "Abhira"),
#     ("Madhav", "Poddar", "father_of", "Armaan"),
#     ("Vidya", "Poddar", "adoptive_mother_of", "Armaan"),
#     ("Armaan", "Poddar", "husband_of", "Abhira")
# ]

# # 2. Initialize the Directed Graph
# G = nx.DiGraph()

# # 3. Populate the Semantic Network
# for source, family, relation, target in family_table_data:
#     # Add nodes with an attribute for their Family Line
#     G.add_node(source, family=family)
#     G.add_node(target) # The target's family will be updated when they are the source
    
#     # Add the relationship edge
#     G.add_edge(source, target, label=relation)
    
#     # Optional: Link characters to their specific Family House
#     G.add_edge(source, f"{family} Family", label="belongs_to")

# # 4. Set up the visualization
# plt.figure(figsize=(16, 12))

# # Use a spring layout to naturally space out the generations
# pos = nx.spring_layout(G, k=0.8, iterations=50, seed=42)

# # Create a color map based on Family Line for visual distinction
# color_map = []
# for node in G:
#     if "Family" in str(node):
#         color_map.append('lightgray') # Family Hub Nodes
#     elif "Maheshwari" in G.nodes[node].get('family', ''):
#         color_map.append('lightgreen')
#     elif "Singhania" in G.nodes[node].get('family', ''):
#         color_map.append('lightblue')
#     elif "Goenka" in G.nodes[node].get('family', ''):
#         color_map.append('lightcoral')
#     elif "Birla" in G.nodes[node].get('family', ''):
#         color_map.append('plum')
#     elif "Sharma" in G.nodes[node].get('family', ''):
#         color_map.append('gold')
#     elif "Poddar" in G.nodes[node].get('family', ''):
#         color_map.append('orange')
#     else:
#         color_map.append('white')

# # 5. Draw the network components
# # Draw nodes
# nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=2500, edgecolors='black')

# # Draw edges
# nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15, edge_color='gray', width=1.5)

# # Draw node labels (Names)
# nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

# # Draw edge labels (Relationships)
# edge_labels = nx.get_edge_attributes(G, 'label')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color='darkred')

# # 6. Finalize plot
# plt.title("Semantic Network: Yeh Rishta Kya Kehlata Hai (Generations 1-4)", fontsize=16, fontweight='bold')
# plt.axis('off') # Hide axes
# plt.tight_layout()
# plt.show()

# # 7. Example: Querying the Semantic Network via Code
# print("--- Network Query ---")
# query_character = "Akshara (Gen 3)"
# print(f"Who is connected to {query_character}?")
# for predecessor in G.predecessors(query_character):
#     relation = G.edges[predecessor, query_character]['label']
#     print(f"- {predecessor} is the {relation} {query_character}")












































# import networkx as nx
# import matplotlib.pyplot as plt

# # 1. Define ALL 92 Members and their relationships
# # Format: (Source Node, Family Line, Relationship, Target Node)
# family_table_data = [
#     # --- MAHESHWARI FAMILY ---
#     ("Bhairavi", "Maheshwari", "mother_of", "Vishambhar"),
#     ("Bhairavi", "Maheshwari", "mother_of", "Omkarnath"),
#     ("Vishambhar", "Maheshwari", "husband_of", "Rajshri"),
#     ("Omkarnath", "Maheshwari", "husband_of", "Sunaina"),
#     ("Vishambhar", "Maheshwari", "father_of", "Shaurya"),
#     ("Vishambhar", "Maheshwari", "father_of", "Akshara (Gen 1)"),
#     ("Rajshri", "Maheshwari", "mother_of", "Shaurya"),
#     ("Rajshri", "Maheshwari", "mother_of", "Akshara (Gen 1)"),
#     ("Shaurya", "Maheshwari", "husband_of", "Varsha"),
#     ("Omkarnath", "Maheshwari", "father_of", "Anshu"),
#     ("Sunaina", "Maheshwari", "mother_of", "Anshu"),
#     ("Anshu", "Maheshwari", "husband_of", "Jasmeet"),
#     ("Shaurya", "Maheshwari", "father_of", "Ananya"),
#     ("Varsha", "Maheshwari", "mother_of", "Ananya"),
#     ("Anshu", "Maheshwari", "father_of", "Nannu"),
#     ("Jasmeet", "Maheshwari", "mother_of", "Nannu"),
#     ("Shaurya", "Maheshwari", "father_of", "Kuhu"),

#     # --- SINGHANIA FAMILY ---
#     ("Mahendra Pratap", "Singhania", "husband_of", "Kaveri (Bhabhimaa)"),
#     ("Mahendra Pratap", "Singhania", "brother_of", "Rajshekhar"),
#     ("Rajshekhar", "Singhania", "husband_of", "Gayatri"),
#     ("Rajshekhar", "Singhania", "husband_of", "Devyani"),
#     ("Rajshekhar", "Singhania", "father_of", "Naitik"),
#     ("Gayatri", "Singhania", "mother_of", "Naitik"),
#     ("Rajshekhar", "Singhania", "father_of", "Nandini"),
#     ("Gayatri", "Singhania", "mother_of", "Nandini"),
#     ("Rajshekhar", "Singhania", "father_of", "Rashmi"),
#     ("Gayatri", "Singhania", "mother_of", "Rashmi"),
#     ("Devyani", "Singhania", "mother_of", "Naman"),
#     ("Devyani", "Singhania", "mother_of", "Muskaan (Singhania)"),
#     ("Naitik", "Singhania", "husband_of", "Akshara (Gen 1)"),
#     ("Naitik", "Singhania", "father_of", "Naksh"),
#     ("Akshara (Gen 1)", "Singhania", "mother_of", "Naksh"),
#     ("Naitik", "Singhania", "father_of", "Naira"),
#     ("Akshara (Gen 1)", "Singhania", "mother_of", "Naira"),
#     ("Naksh", "Singhania", "husband_of", "Keerti"),
#     ("Naman", "Singhania", "husband_of", "Karishma"),
#     ("Naman", "Singhania", "father_of", "Mishti"),
#     ("Karishma", "Singhania", "mother_of", "Mishti"),
#     ("Rashmi", "Singhania", "mother_of", "Gayu"),
#     ("Gayu", "Singhania", "wife_of", "Samarth"),
#     ("Nandini", "Singhania", "adoptive_mother_of", "Yash"),
#     ("Nandini", "Singhania", "mother_of", "Anmol"),
#     ("Naksh", "Singhania", "father_of", "Krish (Singhania)"),
#     ("Keerti", "Singhania", "mother_of", "Krish (Singhania)"),
#     ("Gayu", "Singhania", "mother_of", "Vansh"),
#     ("Gayu", "Singhania", "mother_of", "Vatsal"),
#     ("Samarth", "Singhania", "father_of", "Vatsal"),
#     ("Muskaan (Singhania)", "Singhania", "wife_of", "Alok"),

#     # --- GOENKA FAMILY ---
#     ("Suhasini", "Goenka", "mother_of", "Manish"),
#     ("Suhasini", "Goenka", "mother_of", "Akhilesh"),
#     ("Suhasini", "Goenka", "sister_of", "Purushottam"),
#     ("Manish", "Goenka", "husband_of", "Soumya"),
#     ("Manish", "Goenka", "husband_of", "Swarna"),
#     ("Akhilesh", "Goenka", "husband_of", "Surekha"),
#     ("Manish", "Goenka", "father_of", "Kartik"),
#     ("Soumya", "Goenka", "mother_of", "Kartik"),
#     ("Manish", "Goenka", "father_of", "Shubham (Aryan)"),
#     ("Swarna", "Goenka", "mother_of", "Shubham (Aryan)"),
#     ("Akhilesh", "Goenka", "father_of", "Mansi"),
#     ("Surekha", "Goenka", "mother_of", "Mansi"),
#     ("Akhilesh", "Goenka", "father_of", "Luv"),
#     ("Surekha", "Goenka", "mother_of", "Luv"),
#     ("Akhilesh", "Goenka", "father_of", "Kush"),
#     ("Surekha", "Goenka", "mother_of", "Kush"),
#     ("Kartik", "Goenka", "husband_of", "Naira"),
#     ("Kartik", "Goenka", "husband_of", "Sirat"),
#     ("Kartik", "Goenka", "father_of", "Kairav"),
#     ("Naira", "Goenka", "mother_of", "Kairav"),
#     ("Kartik", "Goenka", "father_of", "Akshara (Gen 3)"),
#     ("Naira", "Goenka", "mother_of", "Akshara (Gen 3)"),
#     ("Kartik", "Goenka", "father_of", "Aarohi"),
#     ("Sirat", "Goenka", "mother_of", "Aarohi"),

#     # --- BIRLA FAMILY ---
#     ("Harshvardhan", "Birla", "husband_of", "Manjari"),
#     ("Harshvardhan", "Birla", "brother_of", "Anand"),
#     ("Anand", "Birla", "husband_of", "Mahima"),
#     ("Harshvardhan", "Birla", "father_of", "Abhimanyu"),
#     ("Manjari", "Birla", "mother_of", "Abhimanyu"),
#     ("Harshvardhan", "Birla", "father_of", "Neil"),
#     ("Anand", "Birla", "father_of", "Parth"),
#     ("Mahima", "Birla", "mother_of", "Parth"),
#     ("Anand", "Birla", "father_of", "Anisha"),
#     ("Mahima", "Birla", "mother_of", "Anisha"),
#     ("Anand", "Birla", "father_of", "Nishtha"),
#     ("Mahima", "Birla", "mother_of", "Nishtha"),
#     ("Parth", "Birla", "husband_of", "Shefali"),
#     ("Parth", "Birla", "father_of", "Shivansh"),
#     ("Shefali", "Birla", "mother_of", "Shivansh"),
#     ("Neil", "Birla", "husband_of", "Aarohi"),
#     ("Neil", "Birla", "father_of", "Ruhi"),
#     ("Aarohi", "Birla", "mother_of", "Ruhi"),
#     ("Abhimanyu", "Birla", "first_husband_of", "Akshara (Gen 3)"),
#     ("Abhimanyu", "Birla", "father_of", "Abhir"),
#     ("Akshara (Gen 3)", "Goenka", "mother_of", "Abhir"),

#     # --- PODDAR FAMILY ---
#     ("Kaveri (Dadisa)", "Poddar", "mother_of", "Madhav"),
#     ("Kaveri (Dadisa)", "Poddar", "mother_of", "Manoj"),
#     ("Kaveri (Dadisa)", "Poddar", "mother_of", "Kajal"),
#     ("Madhav", "Poddar", "husband_of", "Vidya"),
#     ("Manoj", "Poddar", "husband_of", "Manisha"),
#     ("Sanjay", "Poddar", "husband_of", "Kajal"),
#     ("Madhav", "Poddar", "father_of", "Armaan"),
#     ("Vidya", "Poddar", "adoptive_mother_of", "Armaan"),
#     ("Madhav", "Poddar", "father_of", "Rohit"),
#     ("Vidya", "Poddar", "mother_of", "Rohit"),
#     ("Sanjay", "Poddar", "father_of", "Krish (Poddar)"),
#     ("Kajal", "Poddar", "mother_of", "Krish (Poddar)"),
#     ("Manoj", "Poddar", "father_of", "Aryan"),
#     ("Manisha", "Poddar", "mother_of", "Aryan"),
#     ("Manoj", "Poddar", "father_of", "Kiara"),
#     ("Manisha", "Poddar", "mother_of", "Kiara"),
#     ("Sanjay", "Poddar", "father_of", "Charu"),
#     ("Kajal", "Poddar", "mother_of", "Charu"),

#     # --- SHARMA & EXTENDED CONNECTIONS ---
#     ("Abhinav", "Sharma", "husband_of", "Akshara (Gen 3)"),
#     ("Abhinav", "Sharma", "father_of", "Abhira"),
#     ("Akshara (Gen 3)", "Goenka", "mother_of", "Abhira"),
#     ("Armaan", "Poddar", "husband_of", "Abhira"),
#     ("Abhinav", "Sharma", "brother_of", "Muskaan (Sharma)"),
#     ("Kairav", "Goenka", "husband_of", "Muskaan (Sharma)"),
#     ("Mohit Agarwal", "Extended", "husband_of", "Nandini"),
#     ("Rukmini Agarwal", "Extended", "mother_of", "Mohit Agarwal"),
#     ("Yash", "Singhania", "husband_of", "Rose"),
#     ("Nikhil", "Extended", "first_husband_of", "Rashmi"),
#     ("Rama", "Extended", "mother_of", "Nikhil"),
#     ("Sameer", "Extended", "second_husband_of", "Rashmi"),
#     ("Maudi", "Extended", "mother_of", "Sheela"),
#     ("Sheela", "Extended", "mother_of", "Sirat"),
#     ("Mukesh", "Extended", "husband_of", "Sheela"),
#     ("Sheela", "Extended", "mother_of", "Sonu"),
#     ("Mukesh", "Extended", "father_of", "Sonu"),
#     ("Purushottam", "Goenka", "father_of", "Ila")
# ]

# # 2. Initialize Graph
# G = nx.DiGraph()

# # 3. Populate Nodes and Edges
# for source, family, relation, target in family_table_data:
#     # Safely assign the family attribute to the source node
#     if source not in G.nodes:
#         G.add_node(source, family=family)
#     else:
#         G.nodes[source]['family'] = family
        
#     if target not in G.nodes:
#         G.add_node(target, family="Unknown") # Will update if target becomes a source later

#     # Add the edge
#     G.add_edge(source, target, label=relation)

# # 4. Color Mapping Logic
# color_map = []
# for node in G.nodes():
#     fam = G.nodes[node].get('family', 'Unknown')
#     if fam == "Maheshwari": color_map.append('#A2D9CE') # Soft Green
#     elif fam == "Singhania": color_map.append('#AED6F1') # Soft Blue
#     elif fam == "Goenka": color_map.append('#F5B7B1') # Soft Red
#     elif fam == "Birla": color_map.append('#D7BDE2') # Soft Purple
#     elif fam == "Poddar": color_map.append('#F9E79F') # Soft Yellow
#     elif fam == "Sharma": color_map.append('#FAD7A1') # Soft Orange
#     elif fam == "Extended": color_map.append('#D5DBDB') # Gray
#     else: color_map.append('#FFFFFF') # White for trailing nodes

# # 5. Visualization Setup
# # INCREASED figure size massively to accommodate 92 nodes
# plt.figure(figsize=(30, 24))

# # Kamada-Kawai layout often works better for highly interconnected networks than Spring Layout
# pos = nx.kamada_kawai_layout(G) 

# # Draw nodes
# nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=1800, edgecolors='black', linewidths=1.5)

# # Draw edges
# nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15, edge_color='#888888', width=1.0, alpha=0.6)

# # Draw Node Labels (Names)
# nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

# # Draw Edge Labels (Relationships)
# edge_labels = nx.get_edge_attributes(G, 'label')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, font_color='red', alpha=0.7)

# # 6. Add a Custom Legend for the Families
# import matplotlib.patches as mpatches
# legend_handles = [
#     mpatches.Patch(color='#A2D9CE', label='Maheshwari'),
#     mpatches.Patch(color='#AED6F1', label='Singhania'),
#     mpatches.Patch(color='#F5B7B1', label='Goenka'),
#     mpatches.Patch(color='#D7BDE2', label='Birla'),
#     mpatches.Patch(color='#F9E79F', label='Poddar'),
#     mpatches.Patch(color='#FAD7A1', label='Sharma'),
#     mpatches.Patch(color='#D5DBDB', label='Extended Connections')
# ]
# plt.legend(handles=legend_handles, loc='upper left', fontsize=16, title="Family Lines", title_fontsize='18')

# # Final formatting
# plt.title("Full Semantic Network: 92 Family Members of Yeh Rishta Kya Kehlata Hai", fontsize=24, fontweight='bold')
# plt.axis('off')
# plt.tight_layout()

# # Save locally to view it in full resolution, then show.
# plt.savefig("yrkkh_semantic_network.png", dpi=300, bbox_inches='tight')
# print("Graph saved as 'yrkkh_semantic_network.png'. Opening interactive window...")
# plt.show()

# # 7. Code Output / Verification
# print(f"\nTotal Number of Characters (Nodes) Processed: {G.number_of_nodes()}")
# print(f"Total Number of Relationships (Edges) Processed: {G.number_of_edges()}")

















































import networkx as nx
from pyvis.network import Network

# 1. Define ALL 92 Members and their relationships
family_table_data = [
    # --- MAHESHWARI FAMILY ---
    ("Bhairavi", "Maheshwari", "mother_of", "Vishambhar"),
    ("Bhairavi", "Maheshwari", "mother_of", "Omkarnath"),
    ("Vishambhar", "Maheshwari", "husband_of", "Rajshri"),
    ("Omkarnath", "Maheshwari", "husband_of", "Sunaina"),
    ("Vishambhar", "Maheshwari", "father_of", "Shaurya"),
    ("Vishambhar", "Maheshwari", "father_of", "Akshara (Gen 1)"),
    ("Rajshri", "Maheshwari", "mother_of", "Shaurya"),
    ("Rajshri", "Maheshwari", "mother_of", "Akshara (Gen 1)"),
    ("Shaurya", "Maheshwari", "husband_of", "Varsha"),
    ("Omkarnath", "Maheshwari", "father_of", "Anshu"),
    ("Sunaina", "Maheshwari", "mother_of", "Anshu"),
    ("Anshu", "Maheshwari", "husband_of", "Jasmeet"),
    ("Shaurya", "Maheshwari", "father_of", "Ananya"),
    ("Varsha", "Maheshwari", "mother_of", "Ananya"),
    ("Anshu", "Maheshwari", "father_of", "Nannu"),
    ("Jasmeet", "Maheshwari", "mother_of", "Nannu"),
    ("Shaurya", "Maheshwari", "father_of", "Kuhu"),

    # --- SINGHANIA FAMILY ---
    ("Mahendra Pratap", "Singhania", "husband_of", "Kaveri (Bhabhimaa)"),
    ("Mahendra Pratap", "Singhania", "brother_of", "Rajshekhar"),
    ("Rajshekhar", "Singhania", "husband_of", "Gayatri"),
    ("Rajshekhar", "Singhania", "husband_of", "Devyani"),
    ("Rajshekhar", "Singhania", "father_of", "Naitik"),
    ("Gayatri", "Singhania", "mother_of", "Naitik"),
    ("Rajshekhar", "Singhania", "father_of", "Nandini"),
    ("Gayatri", "Singhania", "mother_of", "Nandini"),
    ("Rajshekhar", "Singhania", "father_of", "Rashmi"),
    ("Gayatri", "Singhania", "mother_of", "Rashmi"),
    ("Devyani", "Singhania", "mother_of", "Naman"),
    ("Devyani", "Singhania", "mother_of", "Muskaan (Singhania)"),
    ("Naitik", "Singhania", "husband_of", "Akshara (Gen 1)"),
    ("Naitik", "Singhania", "father_of", "Naksh"),
    ("Akshara (Gen 1)", "Singhania", "mother_of", "Naksh"),
    ("Naitik", "Singhania", "father_of", "Naira"),
    ("Akshara (Gen 1)", "Singhania", "mother_of", "Naira"),
    ("Naksh", "Singhania", "husband_of", "Keerti"),
    ("Naman", "Singhania", "husband_of", "Karishma"),
    ("Naman", "Singhania", "father_of", "Mishti"),
    ("Karishma", "Singhania", "mother_of", "Mishti"),
    ("Rashmi", "Singhania", "mother_of", "Gayu"),
    ("Gayu", "Singhania", "wife_of", "Samarth"),
    ("Nandini", "Singhania", "adoptive_mother_of", "Yash"),
    ("Nandini", "Singhania", "mother_of", "Anmol"),
    ("Naksh", "Singhania", "father_of", "Krish (Singhania)"),
    ("Keerti", "Singhania", "mother_of", "Krish (Singhania)"),
    ("Gayu", "Singhania", "mother_of", "Vansh"),
    ("Gayu", "Singhania", "mother_of", "Vatsal"),
    ("Samarth", "Singhania", "father_of", "Vatsal"),
    ("Muskaan (Singhania)", "Singhania", "wife_of", "Alok"),

    # --- GOENKA FAMILY ---
    ("Suhasini", "Goenka", "mother_of", "Manish"),
    ("Suhasini", "Goenka", "mother_of", "Akhilesh"),
    ("Suhasini", "Goenka", "sister_of", "Purushottam"),
    ("Manish", "Goenka", "husband_of", "Soumya"),
    ("Manish", "Goenka", "husband_of", "Swarna"),
    ("Akhilesh", "Goenka", "husband_of", "Surekha"),
    ("Manish", "Goenka", "father_of", "Kartik"),
    ("Soumya", "Goenka", "mother_of", "Kartik"),
    ("Manish", "Goenka", "father_of", "Shubham (Aryan)"),
    ("Swarna", "Goenka", "mother_of", "Shubham (Aryan)"),
    ("Akhilesh", "Goenka", "father_of", "Mansi"),
    ("Surekha", "Goenka", "mother_of", "Mansi"),
    ("Akhilesh", "Goenka", "father_of", "Luv"),
    ("Surekha", "Goenka", "mother_of", "Luv"),
    ("Akhilesh", "Goenka", "father_of", "Kush"),
    ("Surekha", "Goenka", "mother_of", "Kush"),
    ("Kartik", "Goenka", "husband_of", "Naira"),
    ("Kartik", "Goenka", "husband_of", "Sirat"),
    ("Kartik", "Goenka", "father_of", "Kairav"),
    ("Naira", "Goenka", "mother_of", "Kairav"),
    ("Kartik", "Goenka", "father_of", "Akshara (Gen 3)"),
    ("Naira", "Goenka", "mother_of", "Akshara (Gen 3)"),
    ("Kartik", "Goenka", "father_of", "Aarohi"),
    ("Sirat", "Goenka", "mother_of", "Aarohi"),

    # --- BIRLA FAMILY ---
    ("Harshvardhan", "Birla", "husband_of", "Manjari"),
    ("Harshvardhan", "Birla", "brother_of", "Anand"),
    ("Anand", "Birla", "husband_of", "Mahima"),
    ("Harshvardhan", "Birla", "father_of", "Abhimanyu"),
    ("Manjari", "Birla", "mother_of", "Abhimanyu"),
    ("Harshvardhan", "Birla", "father_of", "Neil"),
    ("Anand", "Birla", "father_of", "Parth"),
    ("Mahima", "Birla", "mother_of", "Parth"),
    ("Anand", "Birla", "father_of", "Anisha"),
    ("Mahima", "Birla", "mother_of", "Anisha"),
    ("Anand", "Birla", "father_of", "Nishtha"),
    ("Mahima", "Birla", "mother_of", "Nishtha"),
    ("Parth", "Birla", "husband_of", "Shefali"),
    ("Parth", "Birla", "father_of", "Shivansh"),
    ("Shefali", "Birla", "mother_of", "Shivansh"),
    ("Neil", "Birla", "husband_of", "Aarohi"),
    ("Neil", "Birla", "father_of", "Ruhi"),
    ("Aarohi", "Birla", "mother_of", "Ruhi"),
    ("Abhimanyu", "Birla", "first_husband_of", "Akshara (Gen 3)"),
    ("Abhimanyu", "Birla", "father_of", "Abhir"),
    ("Akshara (Gen 3)", "Goenka", "mother_of", "Abhir"),

    # --- PODDAR FAMILY ---
    ("Kaveri (Dadisa)", "Poddar", "mother_of", "Madhav"),
    ("Kaveri (Dadisa)", "Poddar", "mother_of", "Manoj"),
    ("Kaveri (Dadisa)", "Poddar", "mother_of", "Kajal"),
    ("Madhav", "Poddar", "husband_of", "Vidya"),
    ("Manoj", "Poddar", "husband_of", "Manisha"),
    ("Sanjay", "Poddar", "husband_of", "Kajal"),
    ("Madhav", "Poddar", "father_of", "Armaan"),
    ("Vidya", "Poddar", "adoptive_mother_of", "Armaan"),
    ("Madhav", "Poddar", "father_of", "Rohit"),
    ("Vidya", "Poddar", "mother_of", "Rohit"),
    ("Sanjay", "Poddar", "father_of", "Krish (Poddar)"),
    ("Kajal", "Poddar", "mother_of", "Krish (Poddar)"),
    ("Manoj", "Poddar", "father_of", "Aryan"),
    ("Manisha", "Poddar", "mother_of", "Aryan"),
    ("Manoj", "Poddar", "father_of", "Kiara"),
    ("Manisha", "Poddar", "mother_of", "Kiara"),
    ("Sanjay", "Poddar", "father_of", "Charu"),
    ("Kajal", "Poddar", "mother_of", "Charu"),

    # --- SHARMA & EXTENDED CONNECTIONS ---
    ("Abhinav", "Sharma", "husband_of", "Akshara (Gen 3)"),
    ("Abhinav", "Sharma", "father_of", "Abhira"),
    ("Akshara (Gen 3)", "Goenka", "mother_of", "Abhira"),
    ("Armaan", "Poddar", "husband_of", "Abhira"),
    ("Abhinav", "Sharma", "brother_of", "Muskaan (Sharma)"),
    ("Kairav", "Goenka", "husband_of", "Muskaan (Sharma)"),
    ("Mohit Agarwal", "Extended", "husband_of", "Nandini"),
    ("Rukmini Agarwal", "Extended", "mother_of", "Mohit Agarwal"),
    ("Yash", "Singhania", "husband_of", "Rose"),
    ("Nikhil", "Extended", "first_husband_of", "Rashmi"),
    ("Rama", "Extended", "mother_of", "Nikhil"),
    ("Sameer", "Extended", "second_husband_of", "Rashmi"),
    ("Maudi", "Extended", "mother_of", "Sheela"),
    ("Sheela", "Extended", "mother_of", "Sirat"),
    ("Mukesh", "Extended", "husband_of", "Sheela"),
    ("Sheela", "Extended", "mother_of", "Sonu"),
    ("Mukesh", "Extended", "father_of", "Sonu"),
    ("Purushottam", "Goenka", "father_of", "Ila")
]

# 2. Define aesthetic colors for UI
color_map = {
    "Maheshwari": "#A2D9CE",  # Soft Green
    "Singhania": "#AED6F1",   # Soft Blue
    "Goenka": "#F5B7B1",      # Soft Red
    "Birla": "#D7BDE2",       # Soft Purple
    "Poddar": "#F9E79F",      # Soft Yellow
    "Sharma": "#FAD7A1",      # Soft Orange
    "Extended": "#D5DBDB"     # Gray
}

# 3. Create the Interactive Network Canvas
# We use a dark background for a sleek, modern UI look
net = Network(
    height="900px", 
    width="100%", 
    bgcolor="#1a1a1a", 
    font_color="white", 
    directed=True,
    select_menu=True, # Adds a dropdown to search for specific characters
    filter_menu=True  # Adds a menu to filter by family
)

# 4. Extract unique nodes and their primary family line
nodes_dict = {}
for source, family, relation, target in family_table_data:
    if source not in nodes_dict:
        nodes_dict[source] = family
    if target not in nodes_dict:
        nodes_dict[target] = "Unknown" # Will be updated if they appear as a source

# Add Nodes to the PyVis network with styling
for node_name, family in nodes_dict.items():
    node_color = color_map.get(family, "#ffffff")
    
    # The 'title' attribute creates the hover tooltip
    hover_text = f"<b>{node_name}</b><br>Family: {family}"
    
    net.add_node(
        node_name, 
        label=node_name, 
        title=hover_text, 
        color=node_color,
        group=family,
        size=25 # Base node size
    )

# Add Edges (Relationships)
for source, family, relation, target in family_table_data:
    net.add_edge(
        source, 
        target, 
        title=relation,     # Hover text for the line
        label=relation,     # Text shown on the line
        color="#888888",
        arrows="to"
    )

# 5. Physics Configuration for Auto-Untangling
# Force Atlas 2 is best for social network graphs. It pushes nodes apart smoothly.
net.force_atlas_2based(
    gravity=-70, 
    central_gravity=0.01, 
    spring_length=150, 
    spring_strength=0.05, 
    damping=0.4, 
    overlap=0
)

# Optional: Un-comment the line below to show an interactive physics settings menu in the browser
# net.show_buttons(filter_=['physics'])

# 6. Generate and Save the UI
output_file = "yrkkh_interactive_network.html"
net.save_graph(output_file)

print(f"Success! Interactive UI generated.")
print(f"Open '{output_file}' in your web browser (Chrome/Safari/Edge) to view the network.")