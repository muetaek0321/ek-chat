import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'
import Stack from '@mui/material/Stack'

import YoutubeVideoPanel from './YoutubeVideoPanel'
import { SongData } from './database-types'

// セクションタイトル用のヘルパーコンポーネント
function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 'bold', color: 'text.secondary' }}>
      {children}
    </Typography>
  )
}

export interface SongsInfoPanelProps {
  songInfo?: SongData
  onBackOutlineList: () => void
}

// ラベルセルの共通スタイル
const labelCellSx = {
  fontWeight: 'bold',
  whiteSpace: 'nowrap',
  width: '160px',
  verticalAlign: 'top',
} as const

export default function SongsInfoPanel({ songInfo, onBackOutlineList }: SongsInfoPanelProps) {
  if (!songInfo) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="text.secondary">楽曲を選択してください</Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ p: 3, overflow: 'auto', height: '100%' }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
        {songInfo.title}
      </Typography>

      {/* 基本情報 */}
      <SectionTitle>基本情報</SectionTitle>
      <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
        <Table size="small">
          <TableBody>
            <TableRow>
              <TableCell sx={labelCellSx}>タイトル</TableCell>
              <TableCell>{songInfo.title}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={labelCellSx}>アーティスト</TableCell>
              <TableCell>{songInfo.artist}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={labelCellSx}>リリース日</TableCell>
              <TableCell>{songInfo.releaseDate}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={labelCellSx}>作詞</TableCell>
              <TableCell>{songInfo.lyrics.join('、')}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={labelCellSx}>作曲</TableCell>
              <TableCell>{songInfo.music.join('、')}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      {/* 収録作品 */}
      {songInfo.includedIn.length > 0 && (
        <>
          <SectionTitle>収録作品</SectionTitle>
          <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
            <Table size="small">
              <TableBody>
                {songInfo.includedIn.map((item, index) => (
                  <TableRow key={index}>
                    <TableCell sx={labelCellSx}>{item.type}</TableCell>
                    <TableCell>{item.title}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      {/* 制作背景 */}
      {songInfo.details.background && (
        <>
          <SectionTitle>制作背景</SectionTitle>
          <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
            <Table size="small">
              <TableBody>
                <TableRow>
                  <TableCell sx={labelCellSx}>概要</TableCell>
                  <TableCell sx={{ whiteSpace: 'pre-wrap' }}>
                    {songInfo.details.background.description}
                  </TableCell>
                </TableRow>
                {songInfo.details.background.artistComment && (
                  <TableRow>
                    <TableCell sx={labelCellSx}>アーティストコメント</TableCell>
                    <TableCell sx={{ whiteSpace: 'pre-wrap' }}>
                      {songInfo.details.background.artistComment}
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      {/* 音楽的特徴 */}
      {songInfo.details.musicalFeatures && (
        <>
          <SectionTitle>音楽的特徴</SectionTitle>
          <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
            <Table size="small">
              <TableBody>
                <TableRow>
                  <TableCell sx={labelCellSx}>ジャンル</TableCell>
                  <TableCell>{songInfo.details.musicalFeatures.genre.join('、')}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell sx={labelCellSx}>概要</TableCell>
                  <TableCell sx={{ whiteSpace: 'pre-wrap' }}>
                    {songInfo.details.musicalFeatures.description}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      {/* 評価・受容 */}
      {songInfo.details.reception && (
        <>
          <SectionTitle>評価・受容</SectionTitle>
          <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
            <Table size="small">
              <TableBody>
                <TableRow>
                  <TableCell sx={labelCellSx}>概要</TableCell>
                  <TableCell sx={{ whiteSpace: 'pre-wrap' }}>
                    {songInfo.details.reception.description}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      {/* 関連情報 */}
      {songInfo.details.relatedInformation.length > 0 && (
        <>
          <SectionTitle>関連情報</SectionTitle>
          <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
            <Table size="small">
              <TableBody>
                {songInfo.details.relatedInformation.map((item, index) => (
                  <TableRow key={index}>
                    <TableCell sx={labelCellSx}>
                      {item.type}：{item.title}
                    </TableCell>
                    <TableCell sx={{ whiteSpace: 'pre-wrap' }}>{item.description}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      <Stack direction="row" spacing={1} sx={{ width: '100%', overflowX: 'auto' }}>
        {songInfo.youtubeVideoId.map((id) => (
          <YoutubeVideoPanel key={id} videoId={id} />
        ))}
      </Stack>

      <Button variant="outlined" color="inherit" onClick={onBackOutlineList}>
        戻る
      </Button>
    </Box>
  )
}
