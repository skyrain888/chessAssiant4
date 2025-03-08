import { post } from '@/utils/request'

// 定义接口类型
interface LoginParams {
  username: string
  password: string
}

interface RegisterParams {
  username: string
  password: string
  email: string
  name?: string
}

interface ResetPasswordParams {
  email: string
}

interface AuthResponse {
  code: number
  message: string
  data: {
    token: string
    user: {
      id: number
      username: string
      email: string
      name?: string
      avatar?: string
    }
  }
}

/**
 * 用户登录
 * @param params 登录参数
 */
export function login(params: LoginParams) {
  return post<AuthResponse>('/auth/login', params)
}

/**
 * 用户注册
 * @param params 注册参数
 */
export function register(params: RegisterParams) {
  return post<AuthResponse>('/auth/register', params)
}

/**
 * 重置密码
 * @param params 重置密码参数
 */
export function resetPassword(params: ResetPasswordParams) {
  return post<{ code: number; message: string }>('/auth/reset-password', params)
}

/**
 * 退出登录
 */
export function logout() {
  return post<{ code: number; message: string }>('/auth/logout')
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser() {
  return post<AuthResponse>('/auth/me')
} 