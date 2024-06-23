from chromadb.utils import embedding_functions
from rich import print
from nara.extra import TimeIt
from db.embeddingCls import Model, paraphrase_MiniLM_L3_v2, all_mpnet_base_v2
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import chromadb

class Db:
    def __init__(self,
                api_key:str = "",
                model:Model = all_mpnet_base_v2,
                verbose:bool = False,
                persistent:bool = False,
                name:str = "my_db",
                collection_name:str = "my_collection",
                saperator:str = "\n[+]\n"
                ):
        self.api_key:str = api_key
        self.model:Model = model
        self.verbose:bool = verbose
        self.docs:list[str] = []
        self.name:str = name
        self.persistent:bool = persistent
        self.collection_name:str = collection_name
        self.saperator:str = saperator
        self.embedingFunction = self._Db()
        self.chroma_client = self._clint()
        self.collection = self._collection()
        self.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
        )
    
    def _Db(self):
        if self.api_key:
            huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
            api_key = self.api_key,
            model_name = self.model.model_name
            )

            return huggingface_ef
        else:
            sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=self.model.model_name)

            return sentence_transformer_ef

    def _clint(self):
        if self.persistent:
            return chromadb.PersistentClient(path=self.name)
        return chromadb.Client()

    def _collection(self):
        try:
            value = self.chroma_client.create_collection(name=self.collection_name, embedding_function=self.embedingFunction)
            return value
        except:
            value = self.chroma_client.get_collection(name=self.collection_name)
            return value

    def add(self, docs:list[str],metadatas:list[dict[str, str]]|None = None, ids:list[str]|None = None):
        def random_id():
            import random
            import string
            return ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids if ids else [random_id() for _ in range(len(docs))]
            )

    @TimeIt
    def query(self, query_texts:list[str] ,n_results:int = 5)->list[dict[str, str]]:
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )["documents"]
        conv = self.doc_to_conversation(results[0])

        return conv

    def doc_to_conversation(self, docs:list[str]) -> list[dict[str, str]]:
        conversations:list[dict[str, str]] = []
        for doc in docs:
            if doc.startswith("[USER_MSG_ID_"):
                role = "user"
                content = doc
            elif doc.startswith("[ASSISTANT_MSG_ID_"):
                role = "assistant"
                content = doc
            elif doc.startswith("[SYSTEM_MSG_ID_"):
                role = "system"
                content = doc
            elif doc.startswith("[DOC"):
                role = "user"
                content = doc
            else:
                role = "user"
                content = doc
            conversations.append({"role": role, "content": content})
        return conversations

    def conversation_to_doc(self, conversations:list[dict[str, str]], add:bool = False) -> list[str]:
        docs = []
        for inx, msg  in enumerate(conversations):

            if msg["role"] == "user":
                docs.append(f'[USER_MSG_ID_{inx}] {msg["content"]}')
            elif msg["role"] == "assistant":
                docs.append(f'[ASSISTANT_MSG_ID_{inx}] {msg["content"]}')
            elif msg["role"] == "system":
                docs.append(f'[SYSTEM_MSG_ID_{inx}] {msg["content"]}')
        if add:
            self.add(docs=docs)
        return docs

    def convos_to_doc(self, query_texts:list[str], metadatas:list[dict[str, str]]) -> list[str]:
        querys = []
        metas = []
        for query, meta in zip(query_texts, metadatas):
            querys.append(query)
            metas.append({"data": json.dumps(meta["data"])})
        self.add(docs=querys, metadatas=metas)
    
    def pdf_to_doc(self, pdf_path:str, add:bool = False) -> list[str]:
        import fitz  # PyMuPDF

        # Open the PDF file
        pdf_document = pdf_path
        pdf = fitz.open(pdf_document)

        # Extract text from each page
        text = ""
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text()
        doc:list[str] = self.text_splitter.split_text(text)
        newDocs = []
        pdfName = pdf_path.split("\\")[-1].split(".")[0]
        for inx, msg  in enumerate(doc):
            newDocs.append(f'[DOC_{pdfName}_MSG_ID_{inx}] {msg}')
        
        if add:
            self.add(docs=newDocs)

        return newDocs


