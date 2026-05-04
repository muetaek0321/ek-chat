"use client"

import { useState } from "react"
import Stack from "@mui/material/Stack"
import Box from "@mui/material/Box"

import UserInput from "@components/UserInput"
import { ChatMessage } from "@types"

export default function Chat() {
  const chatListWidth = 250
  const userInputHeight = 50

  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])

  return (
    <Stack direction="row" sx={{ height: "100vh" }}>

      {/* 履歴 */}
      <Box sx={{ width: chatListWidth, borderRight: 1, borderColor: "divider" }}>

      </Box>

      {/* チャット */}
      <Box sx={{ width: `calc(100vw - ${chatListWidth}px)`}}>
        <Box sx={{ height: `calc(100vh - ${userInputHeight}px)`, overflowY: "auto" }}>

        </Box>
        <Box sx={{ height: userInputHeight, borderTop: 1, borderColor: "divider" }}>
          <UserInput setChatHistory={setChatHistory}/>
        </Box>

      </Box>
      
    </Stack>
  )
}

