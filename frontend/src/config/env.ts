/**
 * 环境配置
 * 包含应用程序的全局配置信息
 */

// 环境配置

interface EnvConfig {
  apiBaseUrl: string;
  uploadUrl: string;
  aiModel: string;
  maxUploadSize: number;
  allowedImageFormats: string[];
}

/**
 * 获取环境配置
 * @returns 环境配置对象
 */
export function getEnvConfig(): EnvConfig {
  return {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api',
    uploadUrl: import.meta.env.VITE_UPLOAD_URL || 'http://localhost:5001/uploads',
    aiModel: import.meta.env.VITE_AI_MODEL || 'openai',
    maxUploadSize: Number(import.meta.env.VITE_MAX_UPLOAD_SIZE || 5242880), // 5MB
    allowedImageFormats: (import.meta.env.VITE_ALLOWED_IMAGE_FORMATS || 'jpg,jpeg,png').split(',')
  };
}

/**
 * 获取API基础URL
 * @returns API基础URL
 */
export function getApiBaseUrl(): string {
  return getEnvConfig().apiBaseUrl;
}

/**
 * 获取上传URL
 * @returns 上传URL
 */
export function getUploadUrl(): string {
  return getEnvConfig().uploadUrl;
}

/**
 * 获取AI模型
 * @returns AI模型
 */
export function getAiModel(): string {
  return getEnvConfig().aiModel;
}

/**
 * 获取最大上传大小
 * @returns 最大上传大小（字节）
 */
export function getMaxUploadSize(): number {
  return getEnvConfig().maxUploadSize;
}

/**
 * 获取允许的图片格式
 * @returns 允许的图片格式数组
 */
export function getAllowedImageFormats(): string[] {
  return getEnvConfig().allowedImageFormats;
}

export default {
  getEnvConfig,
  getApiBaseUrl,
  getUploadUrl,
  getAiModel,
  getMaxUploadSize,
  getAllowedImageFormats
}; 