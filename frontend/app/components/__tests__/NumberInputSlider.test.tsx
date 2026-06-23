import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import NumberInputSlider from '../NumberInputSlider'
import { AppThemeProvider } from '../../ThemeProvider'

describe('NumberInputSlider', () => {
  it('renders correctly with label', () => {
    render(
      <AppThemeProvider initialTheme="light">
        <NumberInputSlider
          value={50}
          setValue={() => {}}
          min={0}
          max={100}
          step={1}
          label="Test Label"
        />
      </AppThemeProvider>
    )
    expect(screen.getByText('Test Label')).toBeInTheDocument()
    expect(screen.getByRole('spinbutton')).toHaveValue(50)
    expect(screen.getByRole('slider')).toHaveValue('50')
  })

  it('calls setValue when input changes', () => {
    const setValueMock = vi.fn()
    render(
      <AppThemeProvider initialTheme="light">
        <NumberInputSlider
          value={50}
          setValue={setValueMock}
          min={0}
          max={100}
          step={1}
        />
      </AppThemeProvider>
    )
    
    const input = screen.getByRole('spinbutton')
    fireEvent.change(input, { target: { value: '60' } })
    
    expect(setValueMock).toHaveBeenCalledWith(60)
  })
})
