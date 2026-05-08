"use client"

import ReactMarkdown from "react-markdown"
import Image from "next/image"
import Stack from "@mui/material/Stack"
import Box from "@mui/material/Box"

import { ChatMessage } from "@types"


export interface ChatContentAssistantProps {
  message: ChatMessage
}


export default function ChatContentAssistant({ message }: ChatContentAssistantProps) {
  return (
    <Stack direction="row" sx={{ width: "100%", justifyContent: "flex-start" }}>
      <Stack direction="row" spacing={1} sx={{ p: 0.5 }}>
        <Box>
          <Image src="/assistant.png" alt="assistant_icon" width={50} height={50} />
        </Box>
        <Box sx={{ border: 1, borderRadius: 1, p: 1 }}>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </Box>
      </Stack>
    </Stack>
  )
}
