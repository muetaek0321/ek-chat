import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import ChatContentUser from '../ChatContentUser'
import { AppThemeProvider } from '../../../ThemeProvider'
import { ChatMessage } from '@types'

describe('ChatContentUser', () => {
  it('renders message content and user icon correctly', () => {
    const message: ChatMessage = {
      role: 'user',
      content: 'Hello from user!',
    }
    render(
      <AppThemeProvider initialTheme="light">
        <ChatContentUser message={message} />
      </AppThemeProvider>
    )
    expect(screen.getByText('Hello from user!')).toBeInTheDocument()
    expect(screen.getByAltText('user_icon')).toBeInTheDocument()
  })
})
