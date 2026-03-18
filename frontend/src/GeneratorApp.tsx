import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Loader2, Download, RefreshCw, ChevronLeft, Box, Image as ImageIcon, Maximize2 } from 'lucide-react';
import axios from 'axios';
import '@google/model-viewer';

// Use environment variable for production, fallback to local for dev
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8001";

// Extend JSX for model-viewer custom element
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'model-viewer': any;
    }
  }
}

export function GeneratorApp({ onBack }: { onBack: () => void }) {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<any>(null);
  const [viewMode, setViewMode] = useState<'3d' | 'image'>('3d');

  useEffect(() => {
    let interval: any;
    if (taskId && (status?.status !== "SUCCEEDED" && status?.status !== "FAILED")) {
      interval = setInterval(async () => {
        try {
          const res = await axios.get(`${API_BASE}/tasks/${taskId}`);
          setStatus(res.data);
          if (res.data.status === "SUCCEEDED" || res.data.status === "FAILED") {
            clearInterval(interval);
            setLoading(false);
            setViewMode('3d');
          }
        } catch (e) {
          console.error("Error polling task:", e);
        }
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [taskId, status]);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setTaskId(null);
    setStatus(null);
    try {
      const res = await axios.post(`${API_BASE}/generate`, { prompt });
      setTaskId(res.data.task_id);
    } catch (e) {
      console.error("Error generating:", e);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-4 md:p-8 flex flex-col">
      {/* Header */}
      <nav className="flex items-center justify-between mb-12 relative z-10">
        <button 
          onClick={onBack}
          className="flex items-center gap-2 text-white/50 hover:text-white transition-colors group"
        >
          <ChevronLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          Back to Landing
        </button>
        <div className="text-2xl font-black tracking-tighter">
          SHOE<span className="text-purple-500">AI</span>
        </div>
        <div className="w-24"></div> {/* Spacer */}
      </nav>

      <div className="max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-12 flex-grow">
        {/* Left: Input */}
        <div className="space-y-8">
          <div className="space-y-4">
            <h2 className="text-4xl md:text-5xl font-bold tracking-tight">Design your <br /><span className="text-white/40 italic">Masterpiece</span></h2>
            <p className="text-white/50 text-lg">Describe the materials, style, and silhouette of your dream shoe.</p>
          </div>

          <div className="glass rounded-[40px] p-8 space-y-6 relative overflow-hidden">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g. A futuristic cyber-punk high-top sneaker with glowing neon strips and translucent sole..."
              className="w-full h-40 bg-transparent border-none text-xl resize-none focus:ring-0 placeholder:text-white/20"
            />
            
            <div className="flex items-center justify-between">
              <div className="text-xs text-white/30 font-bold uppercase tracking-widest">
                Stability AI 3D Pipeline
              </div>
              <button
                onClick={handleGenerate}
                disabled={loading || !prompt.trim()}
                className="bg-white text-black px-8 py-4 rounded-2xl font-bold flex items-center gap-2 hover:bg-purple-500 hover:text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />}
                Generate
              </button>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="glass-card p-6 rounded-3xl space-y-2 hover:bg-white/5 transition-colors cursor-default">
              <Box className="w-6 h-6 text-purple-400" />
              <div className="font-bold text-sm text-white/90">3D Interactive Mesh</div>
              <div className="text-xs text-white/40 leading-relaxed">High-fidelity GLB format compatible with Blender and Unity.</div>
            </div>
            <div className="glass-card p-6 rounded-3xl space-y-2 hover:bg-white/5 transition-colors cursor-default">
              <ImageIcon className="w-6 h-6 text-pink-400" />
              <div className="font-bold text-sm text-white/90">PBR Textures</div>
              <div className="text-xs text-white/40 leading-relaxed">Includes professional lighting and physics-based materials.</div>
            </div>
          </div>
        </div>

        {/* Right: Results Display */}
        <div className="relative min-h-[500px] flex flex-col">
          <AnimatePresence mode="wait">
            {!taskId && !loading ? (
              <motion.div 
                key="empty"
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                className="flex-grow border-2 border-dashed border-white/10 rounded-[40px] flex flex-col items-center justify-center text-white/20 space-y-4"
              >
                <Box className="w-16 h-16" />
                <p className="font-medium tracking-wide text-center px-8">Your 3D model will appear here once you start the generation process.</p>
              </motion.div>
            ) : (
              <motion.div 
                key="content"
                initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
                className="flex-grow glass rounded-[40px] overflow-hidden flex flex-col relative"
              >
                {/* Status Overlay for Loading */}
                {(status?.status !== "SUCCEEDED" && status?.status !== "FAILED") && (
                   <div className="absolute inset-0 z-20 bg-black/40 backdrop-blur-sm flex items-center justify-center text-center p-8">
                      <div className="space-y-6">
                        <div className="relative">
                          <Loader2 className="w-20 h-20 text-purple-500 animate-spin mx-auto" />
                          <div className="absolute inset-0 flex items-center justify-center font-bold text-xs">
                            {status?.progress || 0}%
                          </div>
                        </div>
                        <div className="space-y-2">
                          <h3 className="text-xl font-bold uppercase tracking-widest">{status?.status || "Starting..."}</h3>
                          <p className="text-white/40 max-w-[250px] mx-auto text-sm leading-relaxed">Our AI is hand-crafting your 3D geometry. This typically takes 30-60 seconds.</p>
                        </div>
                      </div>
                   </div>
                )}

                {/* Main Content Area */}
                <div className="flex-grow relative bg-neutral-900/50">
                  {status?.status === "SUCCEEDED" && (
                    <>
                      {viewMode === '3d' ? (
                        <model-viewer
                          src={status.model_url}
                          camera-controls
                          auto-rotate
                          shadow-intensity="1"
                          exposure="1"
                          environment-image="neutral"
                          alt="3D shoe model"
                          style={{ width: '100%', height: '100%', outline: 'none' }}
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center p-12">
                           <img 
                            src={status.thumbnail_url} 
                            alt="Generated Preview" 
                            className="max-h-full rounded-2xl shadow-2xl border border-white/10"
                          />
                        </div>
                      )}

                      {/* View Mode Toggle */}
                      <div className="absolute top-6 left-6 flex p-1 glass rounded-2xl border border-white/10 z-10">
                        <button 
                          onClick={() => setViewMode('3d')}
                          className={cn(
                            "px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-tighter transition-all flex items-center gap-2",
                            viewMode === '3d' ? "bg-white text-black shadow-lg" : "text-white/50 hover:text-white"
                          )}
                        >
                          <Box className="w-4 h-4" />
                          3D View
                        </button>
                        <button 
                          onClick={() => setViewMode('image')}
                          className={cn(
                            "px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-tighter transition-all flex items-center gap-2",
                            viewMode === 'image' ? "bg-white text-black shadow-lg" : "text-white/50 hover:text-white"
                          )}
                        >
                          <ImageIcon className="w-4 h-4" />
                          Image
                        </button>
                      </div>
                    </>
                  )}
                </div>
                
                {/* Result Actions */}
                {status?.status === "SUCCEEDED" && (
                  <div className="p-8 bg-white/5 border-t border-white/10">
                    <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
                      <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-2xl glass flex items-center justify-center group cursor-pointer hover:bg-purple-500/20 transition-all border border-white/5">
                          <RefreshCw className="w-6 h-6 text-white/50 group-hover:text-purple-400 group-hover:rotate-180 transition-all duration-500" />
                        </div>
                        <div>
                          <div className="text-sm font-bold text-white/90">Production Asset</div>
                          <div className="text-xs text-white/30 uppercase tracking-widest font-bold">Ready for Export</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-3 w-full sm:w-auto">
                        <button 
                          onClick={() => {setTaskId(null); setStatus(null); setPrompt("");}} 
                          className="flex-1 sm:flex-none px-6 py-4 rounded-2xl text-white/40 hover:text-white font-bold text-xs uppercase tracking-widest border border-white/10 hover:border-white/20 transition-all"
                        >
                          New Project
                        </button>
                        <a 
                          href={status.model_url}
                          target="_blank"
                          rel="noreferrer"
                          className="flex-1 sm:flex-none flex items-center justify-center gap-3 bg-white text-black px-8 py-4 rounded-2xl font-black text-sm uppercase tracking-wider hover:bg-purple-600 hover:text-white transition-all shadow-[0_0_30px_rgba(255,255,255,0.2)]"
                        >
                          <Download className="w-5 h-5" />
                          Download .GLB
                        </a>
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <footer className="mt-16 py-8 border-t border-white/5 text-center flex flex-col items-center gap-4">
        <div className="text-white/20 text-xs uppercase tracking-[0.3em] font-black">
          Industrial 3D Design &bull; Powered by Stability AI &bull; Rendered with WebGL
        </div>
      </footer>
    </div>
  );
}
