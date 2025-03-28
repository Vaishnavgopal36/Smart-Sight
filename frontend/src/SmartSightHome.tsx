import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

interface Star {
  x: number;
  y: number;
  size: number;
  duration: number;
}

const generateStars = (count: number): Star[] => {
  return Array.from({ length: count }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    size: Math.random() * 3 + 1,
    duration: Math.random() * 5 + 2,
  }));
};

const SmartSightHome = () => {
  const navigate = useNavigate();
  const [stars, setStars] = useState<Star[]>([]);

  useEffect(() => {
    setStars(generateStars(100)); // Generate 100 stars dynamically
  }, []);

  return (
    <div className="relative w-full h-screen overflow-x-hidden overflow-y-auto bg-black text-white">
      {/* Floating Stars Animation */}
      {stars.map((star, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0 }}
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{
            duration: star.duration,
            repeat: Infinity,
            repeatType: "mirror",
          }}
          className="absolute bg-gray-300 rounded-full"
          style={{
            width: star.size,
            height: star.size,
            top: star.y,
            left: star.x,
            boxShadow: "0px 0px 6px rgba(255,255,255,0.6)",
          }}
        />
      ))}

      {/* Header */}
      <header className="sticky top-0 left-0 w-full flex justify-between items-center p-6 bg-black bg-opacity-75 z-10">
        <h1 className="text-2xl font-bold">Smart Sight</h1>
        <nav className="space-x-6">
          <a href="#features" className="hover:underline">
            Features
          </a>
          {/* <a href="#about" className="hover:underline">
            About
          </a> */}
          <a href="#video" className="hover:underline">
            Video
          </a>
          <a href="#team" className="hover:underline">
            Team
          </a>
        </nav>
      </header>

      {/* Main Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
        className="h-screen flex flex-col justify-center items-center text-center px-4"
      >
        <motion.h1
          className="text-7xl font-extrabold tracking-wider"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 1 }}
        >
          Smart Sight
        </motion.h1>
        <p className="mt-4 text-xl font-bold text-gray-300 max-w-2xl">
        Discover, Search, and Navigate
        </p>

        {/* Try Smart Sight Button */}
        <Button
          className="mt-6 bg-yellow-500 text-black p-3 rounded-lg text-lg font-semibold"
          onClick={() => navigate("/app")}
        >
          Let me see...
        </Button>
      </motion.div>

      {/* Features Section */}
      <section
        id="features"
        className="py-20 flex flex-col items-center min-h-screen"
      >
        <h2 className="text-4xl font-bold mb-6">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6 px-10">
          {[
            {
              title: "Multimodal Input",
              description: "Accepts image, text, or image + text.",
            },
            {
              title: "CLIP Model Integration",
              description:
                "Generates shared vector embeddings for images and text. Enables cross-modal search.",
            },
            {
              title: "FAISS Vector Database",
              description:
                "Stores and retrieves embeddings quickly for large datasets.",
            },
            {
              title: "LLM Refinement",
              description:
                "Uses a Large Language Model to refine results into human-like, context-aware answers.",
            },
          ].map((feature, index) => (
            <motion.div
              key={index}
              className="bg-gray-800 p-6 rounded-xl shadow-lg text-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2, duration: 0.5 }}
            >
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-300">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

{/* Team Section */}
<section id="team" className="py-20 flex flex-col items-center min-h-screen">
  <h2 className="text-4xl font-bold mb-12">Our Team</h2>
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-12 gap-y-12 px-16">
    {["Member 1", "Member 2", "Member 3", "Member 4"].map((member, index) => (
      <motion.div
        key={index}
        className="bg-gray-800 p-6 rounded-xl shadow-lg text-center flex flex-col items-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.2, duration: 0.5 }}
      >
        <div className="w-32 h-32 bg-gray-600 rounded-full mb-6"></div>
        <h3 className="text-xl font-semibold">{member}</h3>
      </motion.div>
    ))}
  </div>
</section>


      {/* Video Section */}
      <section
        id="video"
        className="py-20 flex flex-col items-center min-h-screen"
      >
        <h2 className="text-4xl font-bold mb-6">Project Introduction</h2>
        <div className="relative w-3/4">
          <iframe
            className="w-full h-[400px] rounded-xl"
            src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
            title="Smart Sight Introduction"
            allowFullScreen
          ></iframe>
        </div>
      </section>
    </div>
  );
};

export default SmartSightHome;
