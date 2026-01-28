import React from 'react';
import { cn } from '../lib/utils';
import { motion } from 'framer-motion';

const WoodyKey = ({ 
  children, 
  onClick, 
  className, 
  active = false,
  disabled = false,
  ...props 
}) => {
  return (
    <motion.div
      whileTap={!disabled ? { scale: 0.98, translateY: 2 } : {}}
      onClick={!disabled ? onClick : undefined}
      className={cn(
        "woody-key relative flex items-center justify-center cursor-pointer select-none overflow-hidden p-4",
        active && "pressed opacity-90",
        disabled && "opacity-50 cursor-not-allowed",
        className
      )}
      {...props}
    >
      {/* Glass effect handled by CSS class 'woody-key' now */}

      
      <div className="relative z-10 flex items-center gap-2">
        {children}
      </div>
    </motion.div>
  );
};

export default WoodyKey;
