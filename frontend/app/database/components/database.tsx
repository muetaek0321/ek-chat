'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'
import IconButton from '@mui/material/IconButton'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import MenuIcon from '@mui/icons-material/Menu'

import CategoryItemButton from './CategoryItemButton'
import YoutubeVideoPanel from './YoutubeVideoPanel'
import { ApiResponse, getRequest } from '@lib/fetchData'
import { SongDataOutline, DatabaseListResponse } from './database-types'

export default function Database() {
  const chatListWidth = 250
  const collapsedWidth = 48

  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(true)

  // データベースの一覧データ
  const [category, setCategory] = useState<string>('songs')
  const [songsList, setSongsList] = useState<SongDataOutline[]>([])

  // 楽曲DBの表示データ
  const [videoIds, setVideoIds] = useState<string[]>(['0melyLHqP-s', 'T1gBpKHwqQY', 'EfPFG23UZ4c'])

  // サイドバーの開閉切り替え
  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev)
  }

  // 現在のサイドバー幅
  const currentSidebarWidth = isSidebarOpen ? chatListWidth : collapsedWidth

  const isInitialized = useRef(true)

  // ページを開いた時にデータベースの情報を取得
  const getDatabaseInfoList = useCallback(async () => {
    await getRequest<DatabaseListResponse>('/database/list')
      .then((res: ApiResponse<DatabaseListResponse>) => {
        if (res.success && res.data !== undefined) {
          setSongsList(res.data.songs)
        } else {
          alert('データベースの取得に失敗しました。')
          console.log('Error:', res.error)
        }
      })
      .catch((err) => console.log('Error:', err))
  }, [])

  // ページを開いた時にチャット一覧の初期化
  useEffect(() => {
    if (isInitialized.current) {
      isInitialized.current = false
      getDatabaseInfoList()
    }
  }, [getDatabaseInfoList])

  return (
    <Stack direction="row" sx={{ height: '100vh' }}>
      {/* サイドバー */}
      <Box
        sx={{
          width: currentSidebarWidth,
          minWidth: currentSidebarWidth,
          borderRight: 1,
          borderColor: 'divider',
          transition: 'width 0.3s ease, min-width 0.3s ease',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* サイドバー閉じる/開くボタン */}
        <Box
          sx={{
            display: 'flex',
            justifyContent: isSidebarOpen ? 'flex-end' : 'center',
            p: 0.5,
          }}
        >
          <IconButton onClick={toggleSidebar} size="small">
            {isSidebarOpen ? <ChevronLeftIcon /> : <MenuIcon />}
          </IconButton>
        </Box>

        {/* サイドバーのコンテンツ（開いているときのみ表示） */}
        <Box
          sx={{
            opacity: isSidebarOpen ? 1 : 0,
            visibility: isSidebarOpen ? 'visible' : 'hidden',
            transition: 'opacity 0.2s ease, visibility 0.2s ease',
            display: 'flex',
            flexDirection: 'column',
            gap: 1,
            flex: 1,
            overflow: 'hidden',
          }}
        >
          <Box sx={{ py: 1 }}>
            <CategoryItemButton
              category="songs"
              title="楽曲"
              handleDatabaseCategorySwitch={setCategory}
            />
            <CategoryItemButton
              category="releases"
              title="リリース"
              handleDatabaseCategorySwitch={setCategory}
            />
          </Box>
        </Box>
      </Box>

      {/* 表示データ一覧 */}
      <Box
        sx={{
          width: `calc(100vw - ${currentSidebarWidth}px)`,
          transition: 'width 0.3s ease',
        }}
      >
        {videoIds.map((videoId, index) => (
          <YoutubeVideoPanel key={index} videoId={videoId} />
        ))}
      </Box>
    </Stack>
  )
}
