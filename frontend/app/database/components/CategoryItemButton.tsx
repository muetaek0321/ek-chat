'use client'

import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import LibraryMusicTwoToneIcon from '@mui/icons-material/LibraryMusicTwoTone'
import AlbumTwoToneIcon from '@mui/icons-material/AlbumTwoTone'

import { useTheme } from '../../ThemeProvider'
import { Category } from './database-types'

export interface CategoryItemButtonProps {
  category: Category
  title: string
  handleDatabaseCategorySwitch: React.Dispatch<React.SetStateAction<Category>>
}

export default function CategoryItemButton({
  category,
  title,
  handleDatabaseCategorySwitch,
}: CategoryItemButtonProps) {
  const { fontSize } = useTheme()

  const categoryIcons: { [key: string]: React.ReactNode } = {
    songs: <LibraryMusicTwoToneIcon />,
    releases: <AlbumTwoToneIcon />,
  }

  return (
    <Box
      sx={{ border: 1, borderRadius: 1, borderColor: '#e0e0e0', my: 0.5 }}
      onClick={() => handleDatabaseCategorySwitch(category)}
    >
      <Box
        sx={(theme) => ({
          py: 0.5,
          px: 1,
          cursor: 'pointer',
          pointerEvents: 'auto',
          '&:hover': { backgroundColor: theme.palette.custom.hover },
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          fontSize: `${fontSize}px`,
        })}
      >
        {title}
        <Stack direction="row" sx={{ justifyContent: 'flex-end' }}>
          {categoryIcons[category]}
        </Stack>
      </Box>
    </Box>
  )
}
