import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import SettingButton from '../SettingButton'
import { AppThemeProvider } from '../../../ThemeProvider'
import { getRequest } from '@lib/fetchData'

vi.mock('@lib/fetchData', () => ({
  getRequest: vi.fn(),
}))

describe('SettingButton', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(getRequest).mockResolvedValue({
      success: true,
      data: {
        systemPrompt: { text: 'Test prompt' },
        chatModelInfoList: [
          { modelName: 'model-a', isSelected: true, isUse: true, parameters: { temperature: 0.5, thinking: 'low' } }
        ]
      }
    })
  })

  it('renders setting button and opens modal', async () => {
    render(
      <AppThemeProvider initialTheme="light">
        <SettingButton isRunning={false} />
      </AppThemeProvider>
    )
    
    const button = screen.getByRole('button', { name: '設定' })
    expect(button).toBeInTheDocument()
    
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText('設定', { selector: 'b' })).toBeInTheDocument()
    })
    
    expect(getRequest).toHaveBeenCalledWith('/settings')
  })
})
