"use client"

import Link from "next/link"
import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography"
import Button from "@mui/material/Button"

export default function Home() {
  const url = "https://www.elephantkashimashi.com/"

  return (
    <Box sx={{ p: 1, border: 1 }}>
      <Typography variant="h5">TODO：チャットUI実装予定</Typography>
      <Link href={url} target="_blank" rel="noopener noreferrer">
        <Button variant="contained" color="primary">
          Button
        </Button>
      </Link>
    </Box>
  )
}
