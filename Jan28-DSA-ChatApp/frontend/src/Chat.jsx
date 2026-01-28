import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Send, Plus, Users, X, Trash2, MessageSquare } from 'lucide-react';
import Sidebar from './components/Sidebar';
import ChatBubble from './components/ChatBubble';
// import WoodyKey from './components/WoodyKey';

const Chat = () => {
  const [user, setUser] = useState(null);
  const [usersMap, setUsersMap] = useState({});
  const [allUsers, setAllUsers] = useState([]);
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const [showNewChatModal, setShowNewChatModal] = useState(false);
  const [selectedUsersForGroup, setSelectedUsersForGroup] = useState([]);
  const [groupName, setGroupName] = useState('');

  const navigate = useNavigate();
  const messagesEndRef = useRef(null);
  const wsRef = useRef(null); // Keep WS instance in ref
  const activeChatRef = useRef(null); // Keep track of active chat

  // Keep activeChatRef synced
  useEffect(() => {
    activeChatRef.current = activeChat;
  }, [activeChat]);

  // Initial Auth & Load
  useEffect(() => {
    const token = localStorage.getItem('token');
    const u_id = localStorage.getItem('user_id');
    const u_name = localStorage.getItem('username');

    if (!token || !u_id) {
      navigate('/');
      return;
    }
    setUser({ user_id: u_id, username: u_name });

    fetchAllUsers();
    fetchChats(u_id);

    // --- WebSocket Setup ---
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
    const socket = new WebSocket(`${wsUrl}/ws/${u_id}`);

    socket.onopen = () => console.log('WS Connected');
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'new_message') {
        const msg = data.message;

        // Instant Real-time Update
        console.log("WS Recv:", msg, "Active:", activeChatRef.current?.id);

        if (activeChatRef.current && activeChatRef.current.id === data.conversation_id) {
          console.log("MATCH! Updating messages.");
          setMessages(prev => [...prev, msg]);
        } else {
          console.log("NO MATCH. Active:", activeChatRef.current?.id, "Target:", data.conversation_id);
        }

        // Refresh chat list (reorder by recent)
        fetchChats(u_id);
      } else if (data.type === 'new_chat') {
        console.log("WS: New Chat Created!", data);
        fetchChats(u_id);
      }
    };
    socket.onclose = () => console.log('WS Disconnected');

    wsRef.current = socket;

    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []); // Run once

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const fetchAllUsers = async () => {
    try {
      const res = await axios.get(`${import.meta.env.VITE_API_URL}/users`);
      const map = {};
      res.data.forEach(u => map[u.id] = u.username);
      setUsersMap(map);
      setAllUsers(res.data);
    } catch (err) { console.error(err); }
  };

  const fetchChats = async (userId) => {
    try {
      const res = await axios.get(`${import.meta.env.VITE_API_URL}/chat/recent/${userId || user.user_id}`);
      setChats(res.data);
    } catch (err) { console.error("Failed to fetch chats", err); }
  };

  const fetchMessages = async (chatId) => {
    try {
      const res = await axios.get(`${import.meta.env.VITE_API_URL}/chat/${chatId}/messages`);
      setMessages(res.data);
    } catch (err) { console.error(err); }
  };

  const handleSelectChat = (chat) => {
    setActiveChat(chat);
    fetchMessages(chat.id);
  };

  const handleSendMessage = () => {
    if (!inputText.trim() || !activeChat || !wsRef.current) return;

    const payload = {
      type: 'message',
      conversation_id: activeChat.id,
      text: inputText,
      sender_id: user.user_id
    };
    wsRef.current.send(JSON.stringify(payload));
    setInputText('');
  };

  const handleCreateChat = async () => {
    if (selectedUsersForGroup.length === 0) return;

    try {
      const isGroup = selectedUsersForGroup.length > 1;

      if (isGroup && !groupName.trim()) {
        alert("Please enter a group name");
        return;
      }

      const participants = [user.user_id, ...selectedUsersForGroup];

      const payload = {
        participants,
        is_group: isGroup,
        group_name: isGroup ? groupName : null
      };

      const res = await axios.post(`${import.meta.env.VITE_API_URL}/chat/start`, payload);

      await fetchChats(user.user_id);
      setShowNewChatModal(false);
      setSelectedUsersForGroup([]);
      setGroupName('');

      // Find and select new chat
      const updatedChats = await axios.get(`${import.meta.env.VITE_API_URL}/chat/recent/${user.user_id}`);
      const exactChat = updatedChats.data.find(c => c.id === res.data.id);
      if (exactChat) handleSelectChat(exactChat);

    } catch (err) {
      console.error(err);
      alert("Error creating chat");
    }
  };

  const handleDeleteChat = async () => {
    if (!activeChat) return;
    if (!confirm("Are you sure you want to delete this chat history?")) return;

    try {
      await axios.delete(`${import.meta.env.VITE_API_URL}/chat/${activeChat.id}`);
      setActiveChat(null);
      setMessages([]);
      fetchChats(user.user_id);
    } catch (err) {
      console.error("Failed to delete", err);
    }
  };

  const toggleUserSelection = (uid) => {
    if (selectedUsersForGroup.includes(uid)) {
      setSelectedUsersForGroup(prev => prev.filter(id => id !== uid));
    } else {
      setSelectedUsersForGroup(prev => [...prev, uid]);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
    if (wsRef.current) wsRef.current.close();
  };

  const getChatName = (chat) => {
    if (chat.is_group) return chat.group_name;
    const otherId = chat.participants.find(p => p !== user.user_id);
    return usersMap[otherId] || "Unknown User";
  };

  return (
    <div className="flex h-screen bg-[#F4F1EA] overflow-hidden">
      <Sidebar
        user={user}
        chats={chats.map(c => ({ ...c, displayName: getChatName(c) }))}
        activeChatId={activeChat?.id}
        onSelectChat={handleSelectChat}
        onNewChat={() => setShowNewChatModal(true)}
        onLogout={handleLogout}
      />

      <div className="flex-1 flex flex-col relative bg-[#F4F1EA]">
        {/* Zen Background Texture */}
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none bg-[url('https://www.transparenttextures.com/patterns/rice-paper.png')]" />

        {activeChat ? (
          <>
            <div className="h-20 border-b border-[#E0Dcd0] flex items-center justify-between px-8 bg-white/80 backdrop-blur-sm z-10 sticky top-0">
              <div>
                <h3 className="font-bold text-xl text-[#2B2B2B] tracking-tight">
                  {getChatName(activeChat)}
                </h3>
                <p className="text-xs text-[#8FB359] font-medium flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-[#8FB359] inline-block animate-pulse"></span>
                  Online
                </p>
              </div>
              <button
                onClick={handleDeleteChat}
                className="text-[#9CA3AF] hover:text-[#EF4444] hover:bg-[#FEE2E2] transition-all p-2.5 rounded-xl"
                title="Delete Chat"
              >
                <Trash2 size={20} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-8 z-0 space-y-6">
              {messages.map(msg => (
                <ChatBubble
                  key={msg.id}
                  message={msg.text}
                  username={msg.sender_id === user.user_id ? "Me" : (usersMap[msg.sender_id] || "User")}
                  isMe={msg.sender_id === user.user_id}
                  timestamp={msg.timestamp}
                />
              ))}
              <div ref={messagesEndRef} />
            </div>

            <div className="p-6 bg-white border-t border-[#E0Dcd0] z-10">
              <div className="flex gap-4 max-w-5xl mx-auto">
                <input
                  className="zen-input h-14 text-base bg-[#F9F9F9] focus:bg-white shadow-sm"
                  placeholder="Type a mindful message..."
                  value={inputText}
                  onChange={e => setInputText(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
                />
                <button
                  onClick={handleSendMessage}
                  className="zen-button w-16 h-14 flex items-center justify-center rounded-xl"
                >
                  <Send size={20} />
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center flex-col text-[#9CA3AF] gap-6">
            <div className="w-24 h-24 bg-[#EAE7DF] rounded-full flex items-center justify-center mb-2">
              <MessageSquare size={40} className="text-[#8FB359] opacity-50" />
            </div>
            <h2 className="text-2xl font-bold text-[#2B2B2B]">Welcome to ChitChat</h2>
            <p className="text-sm">Select a conversation from the rail to begin.</p>
          </div>
        )}
      </div>

      {/* New Chat/Group Modal */}
      {showNewChatModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
          <div className="bg-white border border-[#E0Dcd0] p-6 rounded-2xl shadow-xl w-96 max-h-[80vh] flex flex-col">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold text-[#2B2B2B]">
                {selectedUsersForGroup.length > 1 ? "Create Group" : "Select Users"}
              </h3>
              <button onClick={() => { setShowNewChatModal(false); setSelectedUsersForGroup([]); setGroupName(''); }}><X className="text-[#9CA3AF]" /></button>
            </div>

            {selectedUsersForGroup.length > 1 && (
              <div className="mb-4">
                <input
                  placeholder="Group Name"
                  className="zen-input text-sm h-10"
                  value={groupName}
                  onChange={(e) => setGroupName(e.target.value)}
                />
              </div>
            )}

            <div className="overflow-y-auto flex-1 space-y-2 pr-2 custom-scrollbar mb-4">
              {allUsers.filter(u => u.id !== user.user_id).map(u => {
                const isSelected = selectedUsersForGroup.includes(u.id);
                return (
                  <button
                    key={u.id}
                    onClick={() => toggleUserSelection(u.id)}
                    className={`w-full text-left px-4 py-3 rounded-xl transition-all ${isSelected
                        ? 'bg-[#8FB359] text-white shadow-md'
                        : 'bg-[#F9F9F9] text-[#2B2B2B] hover:bg-[#EAE7DF]'
                      }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-bold">{u.username}</span>
                      {isSelected && <span className="text-xs bg-white/20 px-2 py-0.5 rounded-full">Selected</span>}
                    </div>
                  </button>
                );
              })}
              {allUsers.filter(u => u.id !== user.user_id).length === 0 && <p className="text-center text-[#9CA3AF] py-4">No other users found.</p>}
            </div>

            <button
              onClick={handleCreateChat}
              disabled={selectedUsersForGroup.length === 0 || (selectedUsersForGroup.length > 1 && !groupName.trim())}
              className="zen-button w-full py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {selectedUsersForGroup.length > 1 ? "Start Group Chat" : "Start Chat"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chat;