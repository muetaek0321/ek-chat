"use client"

import Button from "@mui/material/Button"
import ChatIcon from '@mui/icons-material/Chat';

import { ApiResponse, putRequest } from "@modules/fetchData"
import { ChatInfo } from "@types"


export interface NewChatButtonProps {
  chatInfoList: ChatInfo[]
  setChatInfoList: React.Dispatch<React.SetStateAction<ChatInfo[]>>
  setCurrentChatId: React.Dispatch<React.SetStateAction<string>>
}


export default function NewChatButton({ 
  chatInfoList, setChatInfoList, setCurrentChatId 
}: NewChatButtonProps) {

  // 新しいチャットの作成
  const handleCreateNewChat = async () => {
    await putRequest("/new")
      .then((res: ApiResponse) => {
        if (res.success) {
          const newChatInfo: ChatInfo = res.data
          setChatInfoList((prev) => [...prev, newChatInfo])
          setCurrentChatId(newChatInfo.chatId)
        } else {
          alert("新しいチャットの作成に失敗しました。")
          console.log("Error:", res.error)
        }
      })
      .catch((err) => console.log("Error:", err))
  }
  
  return (
    <Button 
      variant="contained" 
      color="inherit" 
      startIcon={<ChatIcon fontSize="small"/>}
      fullWidth
      onClick={handleCreateNewChat}
    >
      新しいチャット
    </Button>
  )
}