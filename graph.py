import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_edge(self, u, v):
        self.graph.add_edge(u, v)

    def plot_graph(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue',
                node_size=2000, font_size=16, font_color='black', font_weight='bold', ax=ax)
        plt.title("Graph Visualization")
        return fig


def main():
    st.title("Graph Visualization 🖼️")

    if 'graph' not in st.session_state:
        st.session_state.graph = Graph()

    st.sidebar.header("Add Edges")
    node_u = st.sidebar.text_input("Node U:")
    node_v = st.sidebar.text_input("Node V:")
    add_button = st.sidebar.button("Add Edge")

    if add_button and node_u and node_v:
        st.session_state.graph.add_edge(node_u, node_v)
        st.sidebar.success(f"Added edge: {node_u} - {node_v}")

    st.sidebar.header("Graph Information")
    st.sidebar.write(f"Number of nodes: {
                     st.session_state.graph.graph.number_of_nodes()}")
    st.sidebar.write(f"Number of edges: {
                     st.session_state.graph.graph.number_of_edges()}")

    st.subheader("Graph Visualization:")
    if st.session_state.graph.graph.number_of_edges() > 0:
        fig = st.session_state.graph.plot_graph()
        st.pyplot(fig)
    else:
        st.write("No edges in the graph. Add edges to visualize the graph.")


if __name__ == "__main__":
    main()
