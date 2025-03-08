/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string;
  readonly VITE_API_BASE_URL: string;
  readonly VITE_UPLOAD_URL: string;
  readonly VITE_AI_MODEL: string;
  readonly VITE_MAX_UPLOAD_SIZE: string;
  readonly VITE_ALLOWED_IMAGE_FORMATS: string;
  // 更多环境变量...
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
} 