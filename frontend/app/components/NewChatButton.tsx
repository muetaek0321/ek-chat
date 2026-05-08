"use client"

import Button from "@mui/material/Button"
import ChatIcon from '@mui/icons-material/Chat';


export interface NewChatButtonProps {
  createNewChat: () => void
  isRunning: boolean
}


export default function NewChatButton({ createNewChat, isRunning }: NewChatButtonProps) {
  return (
    <Button 
      variant="contained" 
      color="inherit" 
      startIcon={<ChatIcon fontSize="small"/>}
      fullWidth
      onClick={createNewChat}
      disabled={isRunning}
    >
      新しいチャット
    </Button>
  )
}