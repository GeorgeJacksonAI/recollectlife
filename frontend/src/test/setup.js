/**
 * Vitest global setup for React component testing
 */
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

// Extend Vitest expect with jest-dom matchers (optional, requires @testing-library/jest-dom)
// expect.extend(matchers)

// Cleanup after each test
afterEach(() => {
    cleanup()
})
