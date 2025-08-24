from tavily import TavilyClient
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool
from LLMS.groqllm import GroqLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Annotated, Literal, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langchain import hub
from pydantic import BaseModel, Field

class AgenticNode:
    def __init__(self,llm):
        """
        Initialize the PropertiesNode with API keys for Tavily and GROQ.
        """
        self.tavily = TavilyClient()
        self.llm = llm
        # this is used to capture various steps in this file so that later can be use for steps shown
        self.state = {}

    def retriver_tool(self):
        danube_vector_db = Chroma(persist_directory="./databases/danube_properties_chroma_db")
        retriver_danube = danube_vector_db.as_retriever()

        danube_retriver_tool=create_retriever_tool(retriever=retriver_danube,
                                    name="retriver_vector_danube_properties",
                                    description="Search and run information about danube properties")
        
        # shobha_vector_db = Chroma(persist_directory="./databases/shobha_properties_chroma_db")
        # retriver_shobha = danube_vector_db.as_retriever()

        # shobha_retriver_tool=create_retriever_tool(retriever=retriver_shobha
        #                             name="retriver_vector_shobha_properties",
        #                             description="Search and run information about shobha properties")

        tools=[danube_retriver_tool]
        return tools

    def fetch_properties(self,state):
        """
        Invokes the agent model to generate a response based on the current state. Given
        the question, it will decide to retrieve using the retriever tool, or simply end.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with the agent response appended to messages
        """
        print("---CALL AGENT---")
        
        messages = state["messages"]
        model = self.llm.bind_tools(self.retriver_tool())
        response = model.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}
    

    def grade_documents(self,state) -> Literal["summerize", "rewrite_query"]:
        """
        Determines whether the retrieved documents are relevant to the question.
        Args:
            state (messages): The current state

        Returns:
            str: A decision for whether the documents are relevant or not
        """

        print("---CHECK RELEVANCE---")

        # Data model
        class Relavance(BaseModel):
            """Decision for relevance check."""
            is_relevance: str = Field(description="Relevance is 'relevant' or 'not-relevant'")

        # LLM with tool and validation
        llm_with_tool = self.llm.with_structured_output(Relavance)

        # Prompt
        prompt = PromptTemplate(
            template="""You are a decision maker of a retrieved document to a user question. \n 
            Here is the retrieved document: \n\n {context} \n\n
            Here is the user question: {question} \n
            If the document contains keyword(s) or semantic meaning related to the user question, decision it as relevant. \n
            Give a decision result as 'relevant' or 'not-relevant' to indicate whether the document is relevant to the question.""",
            input_variables=["context", "question"],
        )

        # Chain
        chain = prompt | llm_with_tool

        messages = state["messages"]
        last_message = messages[-1]

        question = messages[0].content
        docs = last_message.content

        scored_result = chain.invoke({"question": question, "context": docs})

        score = scored_result.is_relevance

        if score == "relevant":
            print("---DECISION: DOCS RELEVANT---")
            return "summerize"

        else:
            print("---DECISION: DOCS NOT RELEVANT---")
            print(score)
            return "rewrite_query"

    def rewrite(self,state):
        """
        Transform the query to produce a better question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """

        print("---TRANSFORM QUERY---")
        messages = state["messages"]
        question = messages[0].content

        msg = [
            HumanMessage(
                content=f""" \n 
        Look at the input and try to reason about the underlying semantic intent / meaning. \n 
        Here is the initial question:
        \n ------- \n
        {question} 
        \n ------- \n
        Formulate an improved question: """,
            )
        ]
        
        response = self.llm.invoke(msg)
        return {"messages": [response]}
    
    def summarize(self, state):
            """
            Generate answer

            Args:
                state (messages): The current state

            Returns:
                dict: The updated message
            """
            print("---GENERATE---")
            messages = state["messages"]
            question = messages[0].content
            last_message = messages[-1]

            docs = last_message.content

            # Prompt
            prompt = hub.pull("rlm/rag-prompt")

            # LLM
            llm = self.llm

            # Post-processing
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            # Chain
            rag_chain = prompt | llm | StrOutputParser()

            # Run
            response = rag_chain.invoke({"context": docs, "question": question})
            return {"messages": [response]}