from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
loader=PyPDFLoader("docs/HR_document File.pdf")
hr_doc= loader.load()

#split in chunks
splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
chunks=splitter.split_documents(hr_doc)

#embedding
embeddings=OllamaEmbeddings(model="nomic-embed-text")
#stroe in Chroma
vectorstore=Chroma.from_documents(documents=chunks, embedding=embeddings,
                                  persist_directory="./chroma_db",
                                  collection_name="hr_docs")

##retriever
retriever=vectorstore.as_retriever(search_type="similarity", Search_kwargs={"k": 4})

#langchain

def doc_format(hr_doc):
    "\n\n".join(doc.page_content for doc in hr_doc
                )
#system Prompt for RAG

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
rag_prompt=ChatPromptTemplate.from_template(""" You are a Helpful HR assistant. You are given the following extracted parts of a long document and a question. Provide a conversational answer based on the context provided.
If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer or go beyond the context provided. Use three sentences maximum.
Context:
{context}
Question: {question}
Answer in Markdown:""")
llm=ChatOllama(model="llama3",Temperature=0,streaming=True)
#pipeline
rag_chain=({"context": retriever | doc_format, "question": RunnablePassthrough()} | rag_prompt | llm| StrOutputParser()
           )

#Execute


