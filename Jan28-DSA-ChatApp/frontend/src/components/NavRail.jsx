import React from 'react';
import { MessageSquare, Users, LogOut, Folder } from 'lucide-react';

const NavRail = ({ activeTab, onTabChange, onLogout }) => {
  return (
    <div className="nav-rail h-full flex flex-col items-center py-6 gap-6 shadow-[2px_0_10px_rgba(0,0,0,0.05)] z-20">
      <div className="mb-4">
        <div className="w-10 h-10 bg-[#8FB359] rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-md">
          CC
        </div>
      </div>

      <div className="flex-1 flex flex-col gap-4 w-full px-2">
        <button 
          onClick={() => onTabChange('all')}
          className={`nav-item w-full flex justify-center ${activeTab === 'all' ? 'active' : ''}`}
          title="All Chats"
        >
          <Folder size={24} />
        </button>
        <button 
          onClick={() => onTabChange('private')}
          className={`nav-item w-full flex justify-center ${activeTab === 'private' ? 'active' : ''}`}
          title="Private Chats"
        >
          <MessageSquare size={24} />
        </button>
        <button 
          onClick={() => onTabChange('group')}
          className={`nav-item w-full flex justify-center ${activeTab === 'group' ? 'active' : ''}`}
          title="Group Chats"
        >
          <Users size={24} />
        </button>
      </div>

      <div className="mt-auto mb-4">
        <button 
          onClick={onLogout}
          className="nav-item text-red-400 hover:bg-red-50 hover:text-red-500"
          title="Logout"
        >
          <LogOut size={24} />
        </button>
      </div>
    </div>
  );
};

export default NavRail;
