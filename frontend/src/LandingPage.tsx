import React from 'react';
import { motion } from 'framer-motion';
import { Rocket, Zap, Box, ArrowRight } from 'lucide-react';
import { TubesBackground } from './TubesBackground';

interface LandingPageProps {
  onStart: () => void;
}

export function LandingPage({ onStart }: LandingPageProps) {
  return (
    <TubesBackground>
      <div className="flex flex-col items-center justify-center min-h-screen px-4 py-20">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl w-full text-center space-y-8"
        >
          <div className="space-y-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass border border-white/10 text-sm font-medium text-white/80 mb-4"
            >
              <Zap className="w-4 h-4 text-yellow-400" />
              Powered by Stability AI TRELLIS.2
            </motion.div>
            
            <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-white drop-shadow-2xl">
              SHOE<span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">AI</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-white/60 font-medium max-w-2xl mx-auto leading-relaxed">
              Transform your wildest footwear concepts into high-fidelity 3D models in seconds.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 py-12">
            {[
              { icon: Rocket, title: "Ultra Fast", desc: "Proprietary pipeline using Stable Fast 3D" },
              { icon: Box, title: "Production Ready", desc: "High resolution GLB assets for AR/Web" },
              { icon: Zap, title: "AI Driven", desc: "Just describe it, we build the mesh" }
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + i * 0.1 }}
                className="glass-card p-6 rounded-3xl border border-white/5 text-left group hover:border-white/20 transition-all"
              >
                <feature.icon className="w-10 h-10 text-purple-400 mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="text-white font-bold text-lg mb-2">{feature.title}</h3>
                <p className="text-white/40 text-sm leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onStart}
            className="group relative px-10 py-5 bg-white text-black rounded-full font-bold text-xl flex items-center gap-3 mx-auto overflow-hidden transition-all hover:bg-purple-500 hover:text-white"
          >
            <span className="relative z-10">Get Started</span>
            <ArrowRight className="w-6 h-6 relative z-10 group-hover:translate-x-1 transition-transform" />
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity" />
          </motion.button>
        </motion.div>
        
        <div className="absolute bottom-10 left-0 right-0 text-center text-white/20 text-xs uppercase tracking-widest font-bold">
          Click anywhere to randomize background energy
        </div>
      </div>
    </TubesBackground>
  );
}
