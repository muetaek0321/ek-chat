import Box from '@mui/material/Box'

export interface YoutubeVideoPanelProps {
  videoId: string
  width?: number
  height?: number
}

export default function YoutubeVideoPanel({
  videoId,
  width = 560,
  height = 315,
}: YoutubeVideoPanelProps) {
  return (
    <Box>
      <iframe
        width={width}
        height={height}
        src={`https://www.youtube.com/embed/${videoId}`}
        title="YouTube video player"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerPolicy="strict-origin-when-cross-origin"
        allowFullScreen
      />
    </Box>
  )
}
