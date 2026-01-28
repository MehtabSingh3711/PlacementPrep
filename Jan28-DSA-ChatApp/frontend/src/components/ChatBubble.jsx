import React from 'react';
import { cn } from '../lib/utils';

const ChatBubble = ({ message, isMe, username, timestamp }) => {
  return (
    <div className={`flex w-full mb-4 ${isMe ? 'justify-end' : 'justify-start'}`}>
      <div 
        className={`max-w-[70%] rounded-2xl p-4 shadow-sm text-sm leading-relaxed
        ${isMe 
            ? 'bg-[#8FB359] text-white rounded-br-none' 
            : 'bg-white text-[#2B2B2B] rounded-bl-none border border-[#E0Dcd0]'}`}
      >
         {/* Texture-lite */}
         <div className="absolute inset-0 opacity-5 pointer-events-none bg-[url('https://www.transparenttextures.com/patterns/wood-pattern.png')]" />

        <div className="relative z-10">
          {!isMe && <p className="text-xs font-bold mb-1 opacity-70">{username}</p>}
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message}</p>
          <p className="text-[10px] text-right mt-2 opacity-60">
            {new Date(timestamp * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatBubble;
