"use client"

import { useState, useEffect } from "react"
import Stack from "@mui/material/Stack"
import Box from "@mui/material/Box"

import ChatContentUser from "@components/ChatContentUser"
import ChatContentAssistant from "@components/ChatContentAssistant"
import UserInput from "@components/UserInput"
import { getRequest } from "@modules/fetchData"
import { ChatInfo, ChatMessage } from "@types"

export default function Chat() {
  const chatListWidth = 250
  const userInputHeight = 50

  const [chatInfoList, setChatInfoList] = useState<ChatInfo[]>([])
  const [currentChatId, setCurrentChatId] = useState<string>("")
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])

  // チャット履歴の取得
  const getChatHistory = async () => {
    const query = new URLSearchParams({
      chatId: currentChatId
    }).toString()
    await getRequest(`/history?${query}`)
      .then((res) => {
        if (res.success) {
          setChatHistory(res.data)
        } else {
          alert("チャット履歴の取得に失敗しました。")
          console.log("Error:", res.error)
        }
      })
      .catch((err) => console.log("Error:", err))
  }

  // 立ち上げ時にチャット一覧の初期化
  useEffect(() => {
    // TODO: 一時的に固定のチャットIDをセット
    setCurrentChatId("20260505173536_18d1874a-bc13-4481-8eea-908ebbde75e7")
  }, [])

  // チャットIDがセットされるたびに対応するチャット履歴を取得
  useEffect(() => {
    if (currentChatId !== "") getChatHistory()
  }, [currentChatId])

  return (
    <Stack direction="row" sx={{ height: "100vh" }}>

      {/* チャット一覧 */}
      <Box sx={{ width: chatListWidth, borderRight: 1, borderColor: "divider" }}>

      </Box>

      {/* 入力とチャット履歴 */}
      <Box sx={{ width: `calc(100vw - ${chatListWidth}px)`}}>
        <Box sx={{ height: `calc(100vh - ${userInputHeight}px)`, width: "100%" , overflowY: "auto", p: 1 }}>
          {chatHistory.map((message, index) => (
            <Box key={index} sx={{ width: "100%" }}>
              {message.role === "user" ? 
                <ChatContentUser message={message}/>
                :
                <ChatContentAssistant message={message}/>
              }
            </Box>
          ))}
        </Box>
        <Box sx={{ height: userInputHeight, borderTop: 1, borderColor: "divider" }}>
          <UserInput setChatHistory={setChatHistory}/>
        </Box>

      </Box>
      
    </Stack>
  )
}

