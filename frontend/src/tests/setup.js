import { vi } from 'vitest'
import { config } from '@vue/test-utils'

// Mock de localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
global.localStorage = localStorageMock

// Mock de fetch
global.fetch = vi.fn()

// Configuración global de Vue Test Utils
config.global.mocks = {
  $t: (key) => key, // Mock de i18n si se usa
}

// Mock de vue-router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    go: vi.fn(),
    back: vi.fn(),
  }),
  useRoute: () => ({
    params: {},
    query: {},
    path: '/',
  }),
}))
