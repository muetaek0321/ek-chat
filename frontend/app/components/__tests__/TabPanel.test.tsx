import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { CustomTabPanel, a11yProps } from '../TabPanel'

describe('CustomTabPanel', () => {
  it('renders children when value matches index', () => {
    render(
      <CustomTabPanel value={0} index={0}>
        <div>Tab Content</div>
      </CustomTabPanel>
    )
    expect(screen.getByText('Tab Content')).toBeInTheDocument()
  })

  it('does not render children when value does not match index', () => {
    render(
      <CustomTabPanel value={1} index={0}>
        <div>Tab Content</div>
    </CustomTabPanel>
    )
    expect(screen.queryByText('Tab Content')).not.toBeInTheDocument()
  })
})

describe('a11yProps', () => {
  it('returns correct accessibility props', () => {
    const props = a11yProps(2)
    expect(props).toEqual({
      id: 'simple-tab-2',
      'aria-controls': 'simple-tabpanel-2',
    })
  })
})
