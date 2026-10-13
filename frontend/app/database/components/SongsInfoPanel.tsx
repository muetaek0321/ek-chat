import Box from '@mui/material/Box'

import { SongData } from './database-types'

export interface SongsInfoPanelProps {
  songId: string
  songInfo: SongData
  setSongInfo: React.Dispatch<React.SetStateAction<SongData>>
}

export default function SongsInfoPanel({ songId, songInfo, setSongInfo }: SongsInfoPanelProps) {
  return <Box>楽曲情報</Box>
}
