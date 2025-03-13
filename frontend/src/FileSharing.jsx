import { useState, useEffect } from "react";

const API_BASE_URL = "https://file-sharing-site-fcd2.onrender.com";

export default function FileSharing() {
  const [files, setFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [notes, setNotes] = useState("");

  // Fetch uploaded files
  useEffect(() => {
    fetch(`${API_BASE_URL}/files`)
      .then((res) => res.json())
      .then((data) => setFiles(Object.entries(data)))
      .catch((err) => console.error("Error fetching files:", err));
  }, []);

  // Handle file selection
  const handleFileChange = (event) => {
    setSelectedFiles(event.target.files);
  };

  // Handle file upload
  const handleUpload = async () => {
    const formData = new FormData();
    for (let file of selectedFiles) {
      formData.append("file", file);
    }
    formData.append("notes", notes);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      alert("File uploaded successfully!");
      window.location.reload();
    } else {
      alert("Upload failed.");
    }
  };

  // Handle file download
  const handleDownload = (filename) => {
    window.open(`${API_BASE_URL}/files/${filename}`, "_blank");
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h2>File Sharing App</h2>

      {/* File Upload */}
      <input type="file" multiple onChange={handleFileChange} />
      <input
        type="text"
        placeholder="Notes (optional)"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />
      <button onClick={handleUpload}>Upload</button>

      {/* File List */}
      <h3>Uploaded Files</h3>
      <ul>
        {files.map(([filename, details]) => (
          <li key={filename}>
            {filename} - <button onClick={() => handleDownload(filename)}>Download</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
