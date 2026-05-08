"use client"

import Box from "@mui/material/Box"

import { ChatInfo } from "@types"


export interface ChatListProps {
  chatInfoList: ChatInfo[]
  getChatHistory: (chatId: string) => void
  isRunning: boolean
}


export default function ChatList({ chatInfoList, getChatHistory, isRunning }: ChatListProps) {
  
  // チャットの切り替え
  const handleChatSwitch = (chatId: string) => {
    // 生成中はチャットの切り替えを無効化する
    if (isRunning) return
    // チャット履歴の取得
    getChatHistory(chatId)
  }

  return (
    <Box sx={{ height: "70vh", overflowY: "auto" }}>
      {chatInfoList.map((chatInfo, i) => (
        <Box 
          key={i} 
          sx={{ border: 1, borderRadius: 1, borderColor: "#e0e0e0", my: 0.5 }}
          onClick={() => handleChatSwitch(chatInfo.chatId)}
        >
          <Box sx={{ 
            py: 0.5, px: 1, cursor: "pointer", 
            pointerEvents: isRunning ? "none" : "auto",
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
