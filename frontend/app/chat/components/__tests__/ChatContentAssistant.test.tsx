import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import ChatContentAssistant from '../ChatContentAssistant'
import { AppThemeProvider } from '../../../ThemeProvider'
import { ChatMessage } from '@types'

describe('ChatContentAssistant', () => {
  it('renders message content and assistant icon correctly', () => {
    const message: ChatMessage = {
      role: 'assistant',
      content: 'Hello from assistant!',
    }
    render(
      <AppThemeProvider initialTheme="light">
        <ChatContentAssistant message={message} />
      </AppThemeProvider>
    )
    expect(screen.getByText('Hello from assistant!')).toBeInTheDocument()
    expect(screen.getByAltText('assistant_icon')).toBeInTheDocument()
  })
})
