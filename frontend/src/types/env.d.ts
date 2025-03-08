/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_GPT4_VISION_API_KEY: string
  readonly VITE_GEMINI_API_KEY: string
  readonly VITE_CLAUDE_API_KEY: string
  // 更多环境变量...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
} 