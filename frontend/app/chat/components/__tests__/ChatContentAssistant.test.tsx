import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import ChatContentAssistant from '../ChatContentAssistant'
import { AppThemeProvider } from '@AppThemeProvider'
import { ChatMessage } from '../chat-types'

describe('ChatContentAssistant', () => {
  it('renders message content and assistant icon correctly without metadata', () => {
    const message: ChatMessage = {
      role: 'assistant',
      content: 'Hello from assistant!',
    }
    render(
      <AppThemeProvider initialTheme="light">
        <ChatContentAssistant message={message} />
      </AppThemeProvider>,
    )
    expect(screen.getByText('Hello from assistant!')).toBeInTheDocument()
    expect(screen.getByAltText('assistant_icon')).toBeInTheDocument()
    expect(screen.queryByLabelText('metadata')).not.toBeInTheDocument()
  })

  it('renders metadata button when metadata is provided', () => {
    const message: ChatMessage = {
      role: 'assistant',
      content: 'Hello from assistant with metadata!',
      metadata: {
        modelName: 'gemini-3.5-flash-lite',
        tokensPerSecond: 50.5,
        elapsedTime: 1.23,
        executedAt: '2026-11-05 12:00:00',
      },
    }
    render(
      <AppThemeProvider initialTheme="light">
        <ChatContentAssistant message={message} />
      </AppThemeProvider>,
    )
    expect(screen.getByText('Hello from assistant with metadata!')).toBeInTheDocument()
    expect(screen.getByAltText('assistant_icon')).toBeInTheDocument()
    expect(screen.getByLabelText('metadata')).toBeInTheDocument()
  })
})
