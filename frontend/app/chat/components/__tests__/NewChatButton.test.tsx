import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import NewChatButton from '../NewChatButton'
import { AppThemeProvider } from '../../../ThemeProvider'

describe('NewChatButton', () => {
  it('renders button and calls createNewChat on click', () => {
    const createNewChatMock = vi.fn()
    render(
      <AppThemeProvider initialTheme="light">
        <NewChatButton createNewChat={createNewChatMock} isRunning={false} />
      </AppThemeProvider>
    )
    const button = screen.getByRole('button', { name: '新しいチャット' })
    expect(button).toBeInTheDocument()
    expect(button).not.toBeDisabled()

    fireEvent.click(button)
    expect(createNewChatMock).toHaveBeenCalledTimes(1)
  })

  it('is disabled when isRunning is true', () => {
    const createNewChatMock = vi.fn()
    render(
      <AppThemeProvider initialTheme="light">
        <NewChatButton createNewChat={createNewChatMock} isRunning={true} />
      </AppThemeProvider>
    )
    const button = screen.getByRole('button', { name: '新しいチャット' })
    expect(button).toBeDisabled()
  })
})
