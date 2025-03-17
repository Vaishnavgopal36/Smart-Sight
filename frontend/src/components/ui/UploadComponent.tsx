import { useState } from "react";
import axios from "axios";

const UploadComponent = () => {
  const [file, setFile] = useState<File | null>(null);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("query", query);

    try {
      const { data } = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(data);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Failed to upload file.");
    }
    setLoading(false);
  };

  return (
    <div className="p-6 bg-gray-100 rounded-lg shadow-md max-w-md mx-auto mt-10">
      <h2 className="text-xl font-semibold mb-4">Upload an Image</h2>
      <input type="file" onChange={handleFileChange} className="mb-3 p-2 border rounded w-full" />
      <input
        type="text"
        placeholder="Enter a query..."
        value={query}
        onChange={handleQueryChange}
        className="mb-3 p-2 border rounded w-full"
      />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-blue-500 text-white p-2 rounded w-full hover:bg-blue-600"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {response && (
        <div className="mt-4 p-4 bg-white rounded shadow">
          <h3 className="font-bold">Response:</h3>
          <pre className="text-sm">{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default UploadComponent;
