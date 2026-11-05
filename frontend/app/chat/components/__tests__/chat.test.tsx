import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Chat from '../chat'
import { AppThemeProvider } from '@AppThemeProvider'
import { getRequest, putRequest } from '@lib/fetchData'

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
    refresh: vi.fn(),
  }),
}))

vi.mock('@lib/fetchData', () => ({
  getRequest: vi.fn(),
  putRequest: vi.fn(),
}))

// Mock scrollIntoView because jsdom doesn't support it
window.HTMLElement.prototype.scrollIntoView = vi.fn()

describe('Chat Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()

    // Mock getRequest for init
    vi.mocked(getRequest).mockImplementation((url: string) => {
      if (url === '/chat/init') {
        return Promise.resolve({
          success: true,
          data: [{ chatId: '1', title: 'Test Chat' }],
        })
      }
      if (url.startsWith('/chat/history')) {
        return Promise.resolve({
          success: true,
          data: [{ role: 'user', content: 'Hello' }],
        })
      }
      return Promise.resolve({ success: true, data: [] })
    })

    vi.mocked(putRequest).mockResolvedValue({
      success: true,
      data: { chatId: 'new', title: 'New Chat' },
    })
  })

  it('renders chat layout and fetches initial data', async () => {
    render(
      <AppThemeProvider initialTheme="light">
        <Chat />
      </AppThemeProvider>,
    )

    // Wait for the initial getRequest to resolve and components to render
    await waitFor(() => {
      expect(getRequest).toHaveBeenCalledWith('/chat/init')
    })

    await waitFor(() => {
      expect(getRequest).toHaveBeenCalledWith('/chat/history?chatId=1')
    })

    // Assert that the fetched chat history is rendered
    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument()
    })

    // Assert that sidebar items are rendered
    expect(screen.getByText('Test Chat')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '新しいチャット' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '設定' })).toBeInTheDocument()
  })
})
