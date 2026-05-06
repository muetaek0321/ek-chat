"use client"

import React, { useState } from "react"
import Stack from "@mui/material/Stack"
import TextField from "@mui/material/TextField"
import IconButton from "@mui/material/IconButton"
import SendIcon from '@mui/icons-material/Send'

import { ApiResponse, postRequest } from "@modules/fetchData"
import { ChatMessage } from "@types"


export interface UserInputProps {
  setChatHistory: React.Dispatch<React.SetStateAction<ChatMessage[]>>
}


export default function UserInput({ setChatHistory }: UserInputProps) {
  const [inputText, setInputText] = useState<string>("")

  // 入力内容の送信時の処理
  const handleSendUserInput = async () => {
    const userInput = {
      role: "user", 
      content: inputText
    }
    await postRequest("/chat", userInput)
      .then((res: ApiResponse) => {
        if (res.success) {
          setChatHistory((prev) => [...prev, userInput, res.data])
          setInputText("")
        } else {
          alert("返答の生成に失敗しました。")
          console.log("Error:", res.error)
        }
      })
      .catch((err) => console.log("Error:", err))
  }

  // Enterキーで送信
  const handleEnterKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      if (inputText.trim() !== "") handleSendUserInput()
    }
  }
  
  return (
    <Stack direction="row" spacing={1} sx={{ p: 0.5, height: "100%" }}>
      <TextField 
        variant="outlined" size="small" fullWidth rows={2} value={inputText} 
        onChange={(e) => setInputText(e.target.value)}
        onKeyDown={handleEnterKeyPress}
      />
      <IconButton 
        color="primary"
        sx={{ height: "100%" }} 
        onClick={handleSendUserInput} 
        disabled={inputText.trim() === ""}
      >
        <SendIcon fontSize="large"/>
      </IconButton>
    </Stack>
  )
}
