import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'

import { Category, OutlineLists } from './database-types'

export interface OutlineListPanelProps {
  category: Category
  outlineLists: OutlineLists
}

export default function OutlineListPanel({ category, outlineLists }: OutlineListPanelProps) {
  return (
    <Box sx={{ width: '100%', height: '100%', p: 1, display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h5">{category}</Typography>
      <Box sx={{ overflowY: 'auto', width: '100%', flex: 1, minHeight: 0 }}>
        {outlineLists[category].map((e, i) => (
          <Box key={i} sx={{ p: 0.5 }}>
            <Button variant="outlined" color="inherit" sx={{ width: '100%' }}>
              <Typography variant="h6">{e.title}</Typography>
            </Button>
          </Box>
        ))}
      </Box>
    </Box>
  )
}
