import Box from '@mui/material/Box'
import { SxProps, Theme } from '@mui/material/styles'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
  sx?: SxProps<Theme>
}

export function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, sx, ...other } = props

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 2, ...sx }}>{children}</Box>}
    </div>
  )
}

export function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  }
}
