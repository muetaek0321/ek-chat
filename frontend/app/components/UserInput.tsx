"use client"

import React, { useState } from "react"
import Stack from "@mui/material/Stack"
import TextField from "@mui/material/TextField"
import IconButton from "@mui/material/IconButton"
import SendIcon from '@mui/icons-material/Send'

import { ChatMessage } from "@types"


export interface UserInputProps {
  setChatHistory: React.Dispatch<React.SetStateAction<ChatMessage[]>>
}


export default function UserInput({ setChatHistory }: UserInputProps) {
  const [inputText, setInputText] = useState<string>("")

  return (
    <Stack direction="row" spacing={1} sx={{ p: 0.5, height: "100%" }}>
      <TextField 
        variant="outlined" size="small" fullWidth rows={2}
        value={inputText} onChange={(e) => setInputText(e.target.value)}
      />
      <IconButton sx={{ height: "100%" }} onClick={() => alert(inputText)}>
        <SendIcon fontSize="large"/>
      </IconButton>
    </Stack>
  )
}
