"use client"

import ReactMarkdown from "react-markdown"
import Image from "next/image"
import Stack from "@mui/material/Stack"
import Box from "@mui/material/Box"

import { ChatMessage } from "@types"


export interface ChatContentUserProps {
  message: ChatMessage
}


export default function ChatContentUser({ message }: ChatContentUserProps) {
  return (
    <Stack direction="row" sx={{ width: "100%", justifyContent: "flex-end" }}>
      <Stack direction="row" spacing={1} sx={{ p: 0.5 }}>
        <Box sx={{ border: 1, borderRadius: 1, p: 1 }}>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </Box>
        <Box>
          <Image src="/user.png" alt="user_icon" width={50} height={50} />
        </Box>
      </Stack>
    </Stack>
  )
}
