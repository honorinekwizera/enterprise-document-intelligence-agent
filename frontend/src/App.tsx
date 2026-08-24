import { useEffect, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

type Source = {
  filename: string;
  chunk_index: number;
  distance: number;
  excerpt?: string;
};

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<string[]>([]);
  const [selectedDocument, setSelectedDocument] = useState("");
  const [question, setQuestion] = useState("What is this document about?");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [uploadStatus, setUploadStatus] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isAsking, setIsAsking] = useState(false);

  async function loadDocuments() {
    const response = await fetch(`${API_BASE_URL}/documents`);
    const data = await response.json();
    setDocuments(data.documents || []);

    if (data.documents?.length > 0 && !selectedDocument) {
      setSelectedDocument(data.documents[data.documents.length - 1]);
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  async function handleUpload() {
    if (!file) {
      setUploadStatus("Please choose a PDF first.");
      return;
    }

    setIsUploading(true);
    setUploadStatus("Uploading and indexing document...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();

      setUploadStatus(
        `Uploaded ${data.filename}. Extracted ${data.character_count} characters and stored ${data.stored_chunk_count} chunks.`
      );

      await loadDocuments();
      setSelectedDocument(data.filename);
    } catch (error) {
      setUploadStatus("Upload failed. Check that the backend is running.");
    } finally {
      setIsUploading(false);
    }
  }

  async function handleAsk() {
    if (!question.trim()) {
      return;
    }

    setIsAsking(true);
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          filename: selectedDocument || null,
        }),
      });

      if (!response.ok) {
        throw new Error("Chat request failed");
      }

      const data = await response.json();

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      setAnswer("Something went wrong. Check that the backend server is running.");
    } finally {
      setIsAsking(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">AI Document Intelligence</p>
        <h1>Enterprise Document Intelligence Agent</h1>
        <p className="subtitle">
          Upload a PDF, index it with embeddings, search it with ChromaDB, and ask
          questions using an LLM-powered RAG pipeline.
        </p>
      </section>

      <section className="grid">
        <div className="card">
          <h2>1. Upload PDF</h2>
          <p className="helper">
            The backend extracts text, chunks the document, creates OpenAI
            embeddings, and stores them in ChromaDB.
          </p>

          <input
            type="file"
            accept="application/pdf"
            onChange={(event) => setFile(event.target.files?.[0] || null)}
          />

          <button onClick={handleUpload} disabled={isUploading}>
            {isUploading ? "Processing..." : "Upload and Index"}
          </button>

          {uploadStatus && <p className="status">{uploadStatus}</p>}
        </div>

        <div className="card">
          <h2>2. Select Document</h2>
          <p className="helper">
            Choose which uploaded document the assistant should search.
          </p>

          <select
            value={selectedDocument}
            onChange={(event) => setSelectedDocument(event.target.value)}
          >
            <option value="">Search all documents</option>
            {documents.map((document) => (
              <option key={document} value={document}>
                {document}
              </option>
            ))}
          </select>

          <p className="status">{documents.length} document(s) indexed</p>
        </div>
      </section>

      <section className="card chat-card">
        <h2>3. Ask the Document</h2>

        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask a question about the selected document..."
        />

        <button onClick={handleAsk} disabled={isAsking}>
          {isAsking ? "Thinking..." : "Ask AI"}
        </button>

        {answer && (
          <div className="answer">
            <h3>Answer</h3>
            <p>{answer}</p>
          </div>
        )}

        {sources.length > 0 && (
          <div className="sources">
            <h3>Sources Used</h3>

            {sources.map((source, index) => (
              <div className="source" key={`${source.filename}-${source.chunk_index}-${index}`}>
                <strong>
                  {source.filename} · Chunk {source.chunk_index}
                </strong>
                <span>Distance: {source.distance}</span>
                {source.excerpt && <p>{source.excerpt}</p>}
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;