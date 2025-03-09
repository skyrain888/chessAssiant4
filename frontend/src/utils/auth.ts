/**
 * 认证工具类
 */

// 获取token
export function getToken(): string | null {
  return localStorage.getItem('token')
}

// 设置token
export function setToken(token: string): void {
  localStorage.setItem('token', token)
}

// 移除token
export function removeToken(): void {
  localStorage.removeItem('token')
}

// 获取刷新token
export function getRefreshToken(): string | null {
  return localStorage.getItem('refreshToken')
}

// 设置刷新token
export function setRefreshToken(token: string): void {
  localStorage.setItem('refreshToken', token)
}

// 移除刷新token
export function removeRefreshToken(): void {
  localStorage.removeItem('refreshToken')
}

// 检查是否已登录
export function isLoggedIn(): boolean {
  return !!getToken()
}

// 清除所有认证信息
export function clearAuth(): void {
  removeToken()
  removeRefreshToken()
}

export default {
  getToken,
  setToken,
  removeToken,
  getRefreshToken,
  setRefreshToken,
  removeRefreshToken,
  isLoggedIn,
  clearAuth
} 