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

  const chatBubbleStyle = {
    position: "relative",
    border: 1.5,
    borderRadius: 1,
    borderColor: "#505050",
    p: 1,
    bgcolor: "background.paper",

    "&::before": {
      content: '""',
      position: "absolute",
      top: 12,
      left: -8,
      width: 0,
      height: 0,
      borderTop: "8px solid transparent",
      borderBottom: "8px solid transparent",
      borderRight: (theme: any) =>
        `8px solid ${theme.palette.background.paper}`,
    },

    "&::after": {
      content: '""',
      position: "absolute",
      top: 11,
      left: -10,
      width: 0,
      height: 0,
      borderTop: "9px solid transparent",
      borderBottom: "9px solid transparent",
      borderRight: "9px solid",
      borderRightColor: "#505050",
      zIndex: -1,
    },
  }

  return (
    <Stack direction="row" sx={{ width: "100%", justifyContent: "flex-start" }}>
      <Stack direction="row" spacing={1} sx={{ p: 0.5 }}>
        <Box>
          <Image src="/assistant.png" alt="assistant_icon" width={50} height={50} />
        </Box>
        <Box sx={chatBubbleStyle}>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </Box>
      </Stack>
    </Stack>
  )
}
