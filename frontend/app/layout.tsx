import type { Metadata } from 'next'
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter'
import { Geist, Geist_Mono } from 'next/font/google'
import { AppThemeProvider } from './ThemeProvider'
import './globals.css'

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
})

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
})

export const metadata: Metadata = {
  title: 'ek-chat',
  description: 'チャットボット（試作）',
  icons: {
    icon: [
      { url: '/favicon/favicon.ico' },
      { url: '/favicon/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
    ],
    apple: [
      {
        url: '/favicon/apple-touch-icon.png',
        sizes: '180x180',
        type: 'image/png',
      },
    ],
  },
  manifest: '/favicon/site.webmanifest',
}

const defaultTheme = process.env.DEFAULT_THEME === 'dark' ? 'dark' : 'light'
const defaultFontSize = parseInt(process.env.DEFAULT_FONT_SIZE || '14', 10)

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="ja"
      data-theme={defaultTheme}
      style={{ colorScheme: defaultTheme }}
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <AppRouterCacheProvider>
          <AppThemeProvider initialTheme={defaultTheme} initialFontSize={defaultFontSize}>
            {children}
          </AppThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  )
}
