import pandas as pd
import plotly.graph_objects as go
import networkx as nx

G = nx.DiGraph()

with open('kernel_dependencies.csv', 'r') as f:
    lines = f.readlines()
    edge_count = 0
    #Every row on csv is [module,dep,dep dep...], so just parse the lines and treat them as list objects 
    for line in lines[:]:
        parts = [part.strip() for part in line.strip().split(',')]
        
        if len(parts) > 0:
            module = parts[0]
            G.add_node(module)
           
            if len(parts) > 1:
                dependencies = parts[1:]
                for dep in dependencies:
                    if dep:
                        # Edge from module to dependency 
                        G.add_edge(module, dep)
                        edge_count += 1
                        if edge_count < 5:  # Print first few for debugging
                            print(f"Edge: {module} -> {dep}")

info = f"Nodes: {len(G.nodes())}, Edges: {len(G.edges())}"
print(info)

# Use spring layout
pos = nx.spring_layout(G, k=0.5, iterations=50)
#quicker computation for testing
#pos = nx.shell_layout(G)

# Create edge trace
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

# Create node trace
node_x = []
node_y = []
node_text = []
node_size = []

#create dict of the edges for efficiency
out_degrees = dict(G.out_degree())

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    
    # Node info for hover
    #connections = len(list(G.neighbors(node)))
    connections = G.out_degree(node)
    #dependencies = len(list(G.predecessors(node)))
    dependencies = G.in_degree(node)
    node_text.append(f'{node}<br>Uses: {connections}<br>Used by: {dependencies}')
    
    # Size based on number of connections
    node_size.append(10 + connections * 2)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    text=node_text,
    marker=dict(
        showscale=True,
        colorscale='pinkyl',
        size=node_size,
        color=[out_degrees[node] for node in G.nodes()],
        #color=[len(list(G.neighbors(node))) for node in G.nodes()],
        colorbar=dict(
            thickness=15,
            xanchor='left',
        ),
        line_width=2))

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title={'text':'Linux Kernel Module Dependencies',
                        'x': 0.005,
                        'xanchor': 'left'
                        },
                    plot_bgcolor="#1a1a1a",
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[dict(
                        text="Network map showing kernel module dependencies",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 )],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

#fig.show()
fig.write_html('kernel_map.html')
#fig.write_image("kernel_network_2.png", width=3820, height=2160, scale=1)