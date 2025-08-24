from langgraph.graph import START,StateGraph,END
from tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from nodes.dubai_property_search import AgenticNode
from typing import TypedDict,Annotated,List
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represent the structure of the state used in graph
    """
    messages: Annotated[List,add_messages]

def ai_property_search_graph(llm):
    
    graph_builder=StateGraph(State)
    ai_properties_node=AgenticNode(llm)

    ## added the nodes

    graph_builder.add_node("fetch_properties",ai_properties_node.fetch_properties)
        # retrieve = ToolNode([ai_properties_node.retriver_tool])
        # self.graph_builder.add_node("retrieve",retrieve)
        # self.graph_builder.add_node("decide_relevant",ai_properties_node.grade_documents)
        # self.graph_builder.add_node("rewrite_query",ai_properties_node.rewrite)
    graph_builder.add_node("summarize",ai_properties_node.summarize)
        #added the edges

    graph_builder.add_edge(START,END)
        # self.graph_builder.add_conditional_edges("fetch_properties",
        #                                          tools_condition,
        #                                          {
        #                                              "tools":"retrieve",
        #                                              END:END
        #                                          }
        #                                          )
        # self.graph_builder.add_conditional_edges("retrieve",
        #                                          ai_properties_node.grade_documents
        #                                          )
        # self.graph_builder.add_edge("rewrite_query","fetch_properties")
    # graph_builder.add_edge("summarize",END)
    return graph_builder
        
def setup_graph(llm):
    """
    Sets up the graph for the selected use case.
    """
    graph_builder=ai_property_search_graph(llm)
    return graph_builder.compile()
