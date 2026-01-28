import React, { useState } from 'react';
// import WoodyKey from './components/WoodyKey'; // Removed unused import to prevent errors
import NavRail from './NavRail';
import { MessageSquare, Plus, Users, Search } from 'lucide-react';

const Sidebar = ({ user, chats, activeChatId, onSelectChat, onNewChat, onLogout }) => {
  const [activeTab, setActiveTab] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredChats = chats.filter(chat => {
    // Tab Filter
    if (activeTab === 'private' && chat.is_group) return false;
    if (activeTab === 'group' && !chat.is_group) return false;
    
    // Search Filter
    if (searchTerm) {
        const name = chat.displayName || chat.group_name || "Chat";
        return name.toLowerCase().includes(searchTerm.toLowerCase());
    }
    return true;
  });

  return (
    <div className="flex h-full bg-white z-20 shadow-[5px_0_20px_rgba(0,0,0,0.03)]">
      {/* 1. Mini Navigation Rail */}
      <NavRail activeTab={activeTab} onTabChange={setActiveTab} onLogout={onLogout} />

      {/* 2. Chat List Area */}
      <div className="w-72 flex flex-col zen-sidebar">
        {/* Header */}
        <div className="p-5 border-b border-[#E0Dcd0]">
          <h1 className="text-xl font-bold text-[#2B2B2B] tracking-wide mb-1">Messages</h1>
          <p className="text-xs text-[#9CA3AF] font-medium">
             Welcome, <span className="text-[#8FB359]">{user?.username}</span>
          </p>
        </div>

        {/* Search & New Chat */}
        <div className="p-4 space-y-3">
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9CA3AF]" size={16} />
                <input 
                    className="zen-input pl-10 py-2.5 text-sm bg-[#F9F9F9]" 
                    placeholder="Search chats..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            
            <button 
                onClick={onNewChat} 
                className="zen-button w-full py-2.5 flex items-center justify-center gap-2 text-sm"
            >
                <Plus size={18} />
                <span>New Chat</span>
            </button>
        </div>

        {/* List */}
        <div className="flex-1 overflow-y-auto w-full">
            <div className="px-2 pb-2 space-y-1">
                {filteredChats.length === 0 ? (
                    <div className="text-center py-10 opacity-40 text-sm">
                        <p>No chats found.</p>
                    </div>
                ) : (
                    filteredChats.map(chat => (
                        <div 
                            key={chat.id}
                            onClick={() => onSelectChat(chat)}
                            className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all duration-200 
                                ${activeChatId === chat.id 
                                    ? 'bg-[#F4F1EA] border border-[#E0Dcd0]' 
                                    : 'hover:bg-[#F9F9F9] border border-transparent'
                                }`}
                        >
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0
                                ${chat.is_group ? 'bg-[#EAE7DF] text-[#4A5D23]' : 'bg-[#E3E8F0] text-[#475569]'}
                            `}>
                                {chat.is_group ? <Users size={18} /> : <MessageSquare size={18} />}
                            </div>
                            
                            <div className="flex-1 overflow-hidden">
                                <h4 className={`text-sm font-bold truncate ${activeChatId === chat.id ? 'text-[#2B2B2B]' : 'text-[#4B5563]'}`}>
                                    {chat.displayName || chat.group_name || "Chat"}
                                </h4>
                                <p className="text-xs text-[#9CA3AF] truncate">
                                    {chat.last_message_at ? "Active recently" : "New chat"}
                                </p>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
      </div>
    </div>
  );
};
export default Sidebar;
