"use client"

import Button from "@mui/material/Button"
import ChatIcon from '@mui/icons-material/Chat';


export interface NewChatButtonProps {
  createNewChat: () => Promise<void>
}


export default function NewChatButton({ createNewChat }: NewChatButtonProps) {
  return (
    <Button 
      variant="contained" 
      color="inherit" 
      startIcon={<ChatIcon fontSize="small"/>}
      fullWidth
      onClick={createNewChat}
    >
      新しいチャット
    </Button>
  )
}