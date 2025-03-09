<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from './stores/user'
import { Message } from '@arco-design/web-vue'
import { getToken, getRefreshToken } from './utils/auth'

// 初始化用户状态
onMounted(async () => {
  const userStore = useUserStore()
  
  // 检查localStorage中的token
  const token = getToken()
  const refreshToken = getRefreshToken()
  
  console.log('应用初始化，检查认证状态')
  console.log('访问令牌:', token ? token.substring(0, 15) + '...' : '无')
  console.log('刷新令牌:', refreshToken ? refreshToken.substring(0, 15) + '...' : '无')
  
  // 如果有token，尝试获取用户信息
  if (token) {
    console.log('应用初始化，检测到token，尝试恢复用户状态')
    try {
      const success = await userStore.fetchUserInfo()
      if (success) {
        console.log('用户状态恢复成功')
      } else {
        console.log('用户状态恢复失败，尝试刷新token')
        // 尝试刷新token
        if (refreshToken) {
          const refreshSuccess = await userStore.refreshAccessToken()
          if (refreshSuccess) {
            console.log('token刷新成功，再次尝试获取用户信息')
            const retrySuccess = await userStore.fetchUserInfo()
            if (retrySuccess) {
              console.log('用户状态恢复成功')
            } else {
              console.log('用户状态恢复失败，清除登录状态')
              userStore.clearToken()
              Message.warning('登录已过期，请重新登录')
            }
          } else {
            console.log('token刷新失败，清除登录状态')
            userStore.clearToken()
          }
        } else {
          console.log('没有刷新token，清除登录状态')
          userStore.clearToken()
        }
      }
    } catch (error) {
      console.error('恢复用户状态时发生错误:', error)
      userStore.clearToken()
    }
  } else {
    console.log('应用初始化，未检测到token')
  }
})
</script>

<style>
/* 全局样式 */
html, body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
}
</style> 