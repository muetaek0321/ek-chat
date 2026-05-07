"use client"

import Box from "@mui/material/Box"

import { ChatInfo } from "@types"


export interface ChatListProps {
  chatInfoList: ChatInfo[]
  setCurrentChatId: React.Dispatch<React.SetStateAction<string>>
}


export default function ChatList({ chatInfoList, setCurrentChatId }: ChatListProps) {
  
  return (
    <Box sx={{ height: "70vh", overflowY: "auto" }}>
      {chatInfoList.map((chatInfo, i) => (
        <Box 
          key={i} 
          sx={{ border: 1, borderRadius: 1, borderColor: "#e0e0e0", my: 0.5}}
          onClick={() => setCurrentChatId(chatInfo.chatId)}
        >
          <Box sx={{ 
            py: 0.5, px: 1, cursor: "pointer", 
            "&:hover": { backgroundColor: "#f0f0f0" },
            whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}
          >
            {chatInfo.title}
          </Box>
        </Box>
      ))}
      
    </Box>
  )
}
