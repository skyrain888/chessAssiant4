import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, register, logout, getCurrentUser } from '@/services/authService'
import { useNotification } from '@/composables/useNotification'

// 用户信息接口
interface UserInfo {
  id: number
  username: string
  email: string
  name?: string
  avatar?: string
}

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<UserInfo | null>(null)
  const isLoggedIn = ref(!!token.value)
  const loading = ref(false)

  // 通知
  const { success, error } = useNotification()

  // 设置token
  const setToken = (newToken: string | null) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      isLoggedIn.value = true
    } else {
      localStorage.removeItem('token')
      isLoggedIn.value = false
    }
  }

  // 设置用户信息
  const setUserInfo = (user: UserInfo | null) => {
    userInfo.value = user
  }

  // 登录
  const loginAction = async (username: string, password: string) => {
    try {
      loading.value = true
      const res = await login({ username, password })
      setToken(res.data.token)
      setUserInfo(res.data.user)
      success('登录成功')
      return true
    } catch (err) {
      error('登录失败')
      return false
    } finally {
      loading.value = false
    }
  }

  // 注册
  const registerAction = async (username: string, password: string, email: string, name?: string) => {
    try {
      loading.value = true
      const res = await register({ username, password, email, name })
      setToken(res.data.token)
      setUserInfo(res.data.user)
      success('注册成功')
      return true
    } catch (err) {
      error('注册失败')
      return false
    } finally {
      loading.value = false
    }
  }

  // 退出登录
  const logoutAction = async () => {
    try {
      loading.value = true
      await logout()
      setToken(null)
      setUserInfo(null)
      success('退出登录成功')
      return true
    } catch (err) {
      error('退出登录失败')
      return false
    } finally {
      loading.value = false
    }
  }

  // 获取当前用户信息
  const fetchUserInfo = async () => {
    if (!token.value) return false

    try {
      loading.value = true
      const res = await getCurrentUser()
      setUserInfo(res.data.user)
      return true
    } catch (err) {
      setToken(null)
      setUserInfo(null)
      error('获取用户信息失败')
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    loading,
    loginAction,
    registerAction,
    logoutAction,
    fetchUserInfo
  }
})

export default useUserStore 