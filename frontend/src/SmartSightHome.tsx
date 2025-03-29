import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import vaisakhImg from "@/assets/vaisakh.jpg";
import sreejithImg from "@/assets/sreejith.jpg";
import vaishnavImg from "@/assets/vaishnav.jpg";
import rayhanaImg from "@/assets/rayhana.jpg";
import { ArrowDown } from "lucide-react";
import { ArrowUpRight } from "lucide-react"; // Import the icon


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
    setStars(generateStars(100));
  }, []);

  return (
    <div className="relative w-full min-h-screen overflow-x-hidden overflow-y-auto bg-black text-white">
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
        <h1 className="text-5xl font-bold">Smart Sight</h1>
        <nav className="space-x-6">
          <a href="#features" className="text-2xl hover:underline">Features</a>
          <a href="#about" className="text-2xl hover:underline">About</a>
          {/* <a href="#video" className="text-2xl hover:underline">Video</a> */}
          <a href="#team" className="text-2xl hover:underline">Team</a>
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

  {/* Animated Arrow Icon */}
  <motion.div
    initial={{ y: 0 }}
    animate={{ y: 10 }}
    transition={{
      repeat: Infinity,
      repeatType: "reverse",
      duration: 1.2,
      ease: "easeInOut",
    }}
    className="mt-4"
  >
    <ArrowDown size={40} className="text-gray-300" />
  </motion.div>

  {/* Try Smart Sight Button with ArrowUpRight Icon */}
  <Button
    className="mt-6 bg-yellow-500 text-black p-3 rounded-lg text-lg font-semibold flex items-center gap-2"
    onClick={() => navigate("/app")}
  >
    Let me see
    <ArrowUpRight size={24} /> {/* Added ArrowUpRight Icon */}
  </Button>
</motion.div>



{/* Features Section */}
<section id="features" className="py-24 flex flex-col items-center text-center w-full">
  <motion.h2
    className="text-7xl font-extrabold mb-10"
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 1 }}
  >
    Features
  </motion.h2>

  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-10 px-12 w-full max-w-10xl">
    {[
      { title: "Multimodal Input", description: "Accepts image, text, or image + text." },
      { title: "CLIP Model Integration", description: "Generates shared vector embeddings for images and text. Enables cross-modal search." },
      { title: "FAISS Vector Database", description: "Stores and retrieves embeddings quickly for large datasets." },
      { title: "LLM Refinement", description: "Uses a Large Language Model to refine results into human-like, context-aware answers." }
    ].map((feature, index) => (
      <motion.div
        key={index}
        className="bg-gray-800 p-10 lg:p-12 rounded-2xl shadow-xl text-center w-full"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.2, duration: 0.5 }}
      >
        <h3 className="text-2xl lg:text-3xl font-semibold mb-4">{feature.title}</h3>
        <p className="text-lg lg:text-xl text-gray-300">{feature.description}</p>
      </motion.div>
    ))}
  </div>
</section>



{/* About & Video Section */}
<section id="about" className="py-24 bg-gray-900 text-white px-6 flex flex-col lg:flex-row items-center text-center lg:text-left">
  
  {/* Left Side - About Section */}
  <div className="lg:w-1/2 flex flex-col items-center lg:items-start lg:mx-auto lg:pl-24">
    <h2 className="text-6xl font-bold mb-6">About</h2>
    <p className="text-3xl max-w-10xl leading-relaxed">
      Traditional search tools struggle to integrate text and image inputs, limiting their functionality. 
      High-cost AI solutions make advanced search capabilities inaccessible to small teams. 
      <strong> SmartSight</strong> bridges this gap with an AI-powered multi-modal search system, 
      delivering accurate and efficient results while remaining cost-effective.
    </p>
  </div>

  {/* Right Side - Video Section */}
  <div className="lg:w-1/2 flex justify-center mt-10 lg:mt-0">
    <div className="relative w-full max-w-3xl">
      <iframe 
        className="w-full h-[450px] lg:h-[550px] rounded-xl" 
        src="https://www.youtube.com/embed/YOUR_VIDEO_ID" 
        title="Smart Sight Introduction" 
        allowFullScreen
      ></iframe>
    </div>
  </div>

</section>

  
<section id="team" className="py-24 flex flex-col items-center text-center">
  <h2 className="text-6xl font-bold mb-8">Our Team</h2>
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 px-10">
    {[
      { name: "Vaisakh V", imageUrl: vaisakhImg },
      { name: "Sreejith M Varma", imageUrl: sreejithImg },
      { name: "Vaishnav Gopal", imageUrl: vaishnavImg },
      { name: "Rayhana S", imageUrl: rayhanaImg }
    ].map((member, index) => (
      <motion.div 
        key={index} 
        className="bg-gray-800 p-6 rounded-xl shadow-lg text-center flex flex-col items-center"
      > 
        <img 
          src={member.imageUrl} 
          alt={member.name} 
          className="w-32 h-32 object-cover rounded-full mb-4"
        />
        <h3 className="text-xl font-semibold">{member.name}</h3>
      </motion.div>
    ))}
  </div>
</section>
</div>

  );
};
export default SmartSightHome;