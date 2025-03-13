import "./App.css"; // Keep the existing styles
import FileSharing from "./FileSharing"; // Import the file-sharing component

function App() {
  return (
    <div className="App">
      <header>
        <h1>File Sharing App</h1>
      </header>

      <main>
        <FileSharing /> {/* Add the FileSharing component here */}
      </main>

      <footer>
        <p className="read-the-docs">Upload, download, and share files easily.</p>
      </footer>
    </div>
  );
}

export default App;
