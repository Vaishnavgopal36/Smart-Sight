import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Camera } from "lucide-react";

import {
  Upload,
  Send,
  RefreshCw,
  Sun,
  Moon,
  ChevronUp,
  ChevronDown,
} from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import axios from "axios";
import { API_BASE_URL } from "./config";
import "./App.css";
import { CONFIG } from "./config";

interface Message {
  text: string | string[];
  inputImages?: string[];
  images?: { url: string; caption: string }[];
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [image, setImage] = useState<string[] | null>(null);
  const [backendStatus, setBackendStatus] = useState<string>("Idle");
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const [expandedImages, setExpandedImages] = useState<number | null>(null);
  const [useCamera, setUseCamera] = useState<boolean>(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    if (useCamera) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          streamRef.current = stream;
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch((err) => {
          console.error("Error accessing the camera", err);
          alert(
            "Could not access the camera. Please check your permissions and try again."
          );
          setUseCamera(false);
        });
    } else {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      }
    }
  }, [useCamera]);

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext("2d");
      if (context) {
        canvasRef.current.width = videoRef.current.videoWidth;
        canvasRef.current.height = videoRef.current.videoHeight;
        context.drawImage(
          videoRef.current,
          0,
          0,
          canvasRef.current.width,
          canvasRef.current.height
        );
        const dataUrl = canvasRef.current.toDataURL("image/jpeg");
        setImage((prev) => [...(prev || []), dataUrl]);
      }
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (input || (image && image.length > 0)) {
      const newMessage: Message = {
        text: input,
        inputImages: image || [],
        images: [],
      };

      setMessages((prev) => [...prev, newMessage]);
      setInput("");
      setImage(null);
      setBackendStatus("Processing...");

      const formData = new FormData();
      formData.append("query", input);

      if (image && image.length > 0) {
        for (let i = 0; i < image.length; i++) {
          const img = image[i];
          const byteCharacters = atob(img.split(",")[1]);
          const byteNumbers = new Array(byteCharacters.length);
          for (let j = 0; j < byteCharacters.length; j++) {
            byteNumbers[j] = byteCharacters.charCodeAt(j);
          }
          const byteArray = new Uint8Array(byteNumbers);
          const file = new Blob([byteArray], { type: "image/jpeg" });

          formData.append("file", file, `image_${i}.jpg`);
        }
      }

      try {
        const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        console.log("Response:", response.data);

        if (response.data) {
          const retrievedImages = response.data.similar_images || [];
          const retrievedCaptions = response.data.retrieved_captions || [];

          const formattedImages = retrievedImages.map(
            (url: string, index: number) => ({
              url,
              caption: retrievedCaptions[index] || "No caption available",
            })
          );

          const rawResponse = response.data.llm_response;
          const cleanedResponse = rawResponse.replace(/```json|```/g, "").trim();

          let responsePoints: string[] = [];

          try {
            const parsedResponse = JSON.parse(cleanedResponse);

            if (Array.isArray(parsedResponse)) {
              responsePoints = parsedResponse;
            } else if (
              typeof parsedResponse === "object" &&
              parsedResponse.response
            ) {
              responsePoints = [parsedResponse.response];
            } else {
              responsePoints = ["Invalid response format."];
            }
          } catch (error) {
            console.error("Error parsing AI response:", error);
            responsePoints = ["No internet connection."];
          }

          setMessages((prev) => [
            ...prev,
            {
              text: responsePoints,
              images: formattedImages,
            },
          ]);
        }

        setBackendStatus("Completed ✅");
      } catch (error) {
        console.error("Error sending request to backend", error);
        setBackendStatus("Error ❌");
      }
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const readFile = (file: File): Promise<string> => {
        return new Promise((resolve) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result as string);
          reader.readAsDataURL(file);
        });
      };

      Promise.all(Array.from(files).map(readFile)).then((imageUrls) => {
        setImage((prev) => [...(prev || []), ...imageUrls]);
      });

      e.target.value = "";
    }
  };

  const handleRemoveImage = (index: number) => {
    setImage((prev) => prev?.filter((_, i) => i !== index) || []);
  };

  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="text-xl font-bold p-4 bg-[var(--background)] shadow-md flex flex-wrap items-center justify-between gap-2 sm:gap-4">
        <div className="flex items-center gap-2">
          <img src={CONFIG.logoURL} alt="Logo" className="h-8 rounded-lg" />
          <span>{CONFIG.siteTitle}</span>
        </div>

        <div className="flex flex-wrap items-center gap-2 sm:gap-4">
          <div className="text-sm px-4 py-1 rounded-lg bg-[var(--card)]">
            Backend Status: {backendStatus}
          </div>

          <Button
            variant="outline"
            onClick={async () => {
              setMessages([]);
              setInput("");
              setImage(null);

              try {
                const response = await fetch(`${API_BASE_URL}/reset/`, {
                  method: "POST",
                });
                const data = await response.json();
                console.log(data.message);
              } catch (error) {
                console.error("Error resetting backend:", error);
              }
            }}
            className="flex items-center gap-2 hover:bg-[var(--muted)] active:scale-95 transition"
          >
            <RefreshCw className="h-4 w-4 text-gray-400" /> New Chat
          </Button>

          <Button
            variant="outline"
            onClick={toggleTheme}
            className="flex items-center gap-2 hover:bg-[var(--muted)] active:scale-95 transition"
          >
            {theme === "dark" ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
            <span>{theme === "dark" ? "Light Mode" : "Dark Mode"}</span>
          </Button>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 flex flex-col">
          <div className="flex-1 overflow-y-auto p-4 space-y-2 max-h-[calc(100vh-120px)]">
            {messages.map((msg, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`p-3 rounded-lg border shadow-xl ${
                  index % 2 === 0 ? "bg-[var(--sender)]" : "bg-[var(--response)]"
                }`}
              >
                {Array.isArray(msg.text) ? (
                  <ul className="list-disc list-inside text-sm text-foreground">
                    {msg.text.length > 0 ? (
                      msg.text.map((point, index) => <li key={index}>{point}</li>)
                    ) : (
                      <li>No relevant insights available.</li>
                    )}
                  </ul>
                ) : (
                  <p className="text-sm text-foreground">{msg.text}</p>
                )}

                {msg.inputImages && msg.inputImages.length > 0 && (
                  <div className="mt-2 grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {msg.inputImages.map((img, imgIndex) => (
                      <div key={imgIndex} className="text-center">
                        <p className="text-xs text-gray-400">Uploaded Image:</p>
                        <img
                          src={img}
                          alt={`Uploaded ${imgIndex + 1}`}
                          className="w-32 h-32 rounded-md mx-auto mt-1"
                        />
                      </div>
                    ))}
                  </div>
                )}

                {msg.images && msg.images.length > 0 && (
                  <div className="mt-3">
                    <button
                      onClick={() =>
                        setExpandedImages(expandedImages === index ? null : index)
                      }
                      className="flex items-center gap-2 text-xs font-bold px-3 py-1 rounded-md transition-all duration-200 
             bg-[var(--muted)] text-[var(--foreground)] hover:bg-[var(--card)]"
                    >
                      {expandedImages === index ? (
                        <>
                          <ChevronUp className="w-4 h-4 text-[var(--foreground)]" />
                          Hide
                        </>
                      ) : (
                        <>
                          <ChevronDown className="w-4 h-4 text-[var(--foreground)]" />
                          See My Brain
                        </>
                      )}
                    </button>

                    {expandedImages === index && (
                      <div className="grid grid-cols-2 gap-3 mt-2 p-2 bg-[var(--card)] rounded-lg shadow-md">
                        {msg.images.map((img, imgIndex) => (
                          <div key={imgIndex} className="text-center">
                            <img
                              src={img.url}
                              alt="Retrieved"
                              className="w-32 h-32 rounded-md mx-auto border border-[var(--muted)]"
                            />
                            <p className="text-xs text-[var(--foreground)] opacity-80 mt-1">
                              {img.caption}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </motion.div>
            ))}
            <div ref={chatEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 bg-background flex flex-col gap-4">
            {/* Camera Section */}
            {useCamera && (
              <div className="flex flex-col items-start gap-2">
                <video
                  ref={videoRef}
                  autoPlay
                  className="rounded-xl w-full max-w-xs"
                />
                <div className="flex gap-2 w-full max-w-xs">
                  <Button
                    onClick={captureImage}
                    className="bg-white text-black border border-gray-300 hover:bg-gray-100 flex-1"
                  >
                    Capture
                  </Button>
                  <Button
                    onClick={() => setUseCamera(false)}
                    className="bg-red-500 hover:bg-red-600 flex-1"
                  >
                    Close
                  </Button>
                </div>
                <canvas ref={canvasRef} style={{ display: "none" }} />
              </div>
            )}

            {/* Combined Image Preview Section */}
            {image && image.length > 0 && (
              <div className="flex flex-wrap gap-2 p-2">
                {image.map((img, index) => (
                  <div key={index} className="relative w-16 h-16">
                    <img
                      src={img}
                      alt={`Image ${index + 1}`}
                      className="w-full h-full object-cover rounded-lg border border-gray-500"
                    />
                    {/* Remove Button */}
                    <button
                      onClick={() => handleRemoveImage(index)}
                      className="absolute top-0 right-0 bg-black bg-opacity-50 text-white rounded-full p-1 text-xs hover:bg-opacity-70 active:scale-90 transition"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Buttons and Input Row */}
            <div className="flex flex-wrap items-center gap-2">
              {/* Image Upload */}
              <Button
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
                className="px-4 py-2 text-sm flex items-center gap-2 hover:bg-[var(--muted)] active:scale-95 transition"
              >
                <Upload className="h-5 w-5 text-gray-400" />
              </Button>

              {/* Camera Toggle/Capture */}
              <Button
                variant="outline"
                onClick={() => {
                  if (useCamera) {
                    captureImage(); // Capture image if camera is already open
                  } else {
                    setUseCamera(true); // Open camera if it's not already open
                  }
                }}
                className="px-4 py-2 text-sm flex items-center gap-2 hover:bg-[var(--muted)] active:scale-95 transition"
              >
                <Camera className="h-5 w-5 text-gray-400" />
              </Button>

              <input
                type="file"
                ref={fileInputRef}
                accept="image/*"
                multiple
                hidden
                onChange={handleFileUpload}
              />

              {/* Text Input */}
              <Input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                placeholder="Let's find out..."
                className="flex-1 bg-[var(--background)] text-[var(--foreground)] border border-[var(--muted)] rounded-lg px-3 py-2"
              />

              {/* Send Button */}
              <Button
                onClick={handleSend}
                className="text-[var(--muted)] hover:bg-[var(--muted)]/30 active:scale-95 transition"
              >
                <Send className="h-5 w-5 text-gray-400" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}