import React, { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { LandingPage } from './LandingPage';
import { GeneratorApp } from './GeneratorApp';

function App() {
  const [showGenerator, setShowGenerator] = useState(false);

  return (
    <div className="min-h-screen bg-black overflow-x-hidden">
      <AnimatePresence mode="wait">
        {!showGenerator ? (
          <motion.div
            key="landing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, scale: 1.1, filter: "blur(20px)" }}
            transition={{ duration: 0.8 }}
          >
            <LandingPage onStart={() => setShowGenerator(true)} />
          </motion.div>
        ) : (
          <motion.div
            key="generator"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <GeneratorApp onBack={() => setShowGenerator(false)} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
