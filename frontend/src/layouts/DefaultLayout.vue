<template>
  <div class="default-layout">
    <a-layout>
      <a-layout-header class="header">
        <div class="header-content">
          <div class="logo">
            <router-link to="/">家长助手</router-link>
          </div>
          
          <div class="nav-menu">
            <a-menu mode="horizontal" :selected-keys="[activeKey]">
              <a-menu-item key="home">
                <router-link to="/">首页</router-link>
              </a-menu-item>
              
              <a-menu-item key="tools">
                <router-link to="/tools">工具中心</router-link>
              </a-menu-item>
              
              <a-menu-item key="chess">
                <router-link to="/chess">国际象棋工具</router-link>
              </a-menu-item>
            </a-menu>
          </div>
          
          <div class="user-actions">
            <template v-if="userStore.isLoggedIn">
              <a-dropdown trigger="click">
                <a-avatar class="user-avatar">
                  <template v-if="userStore.avatar">
                    <img :src="userStore.avatar" alt="avatar" />
                  </template>
                  <template v-else>
                    {{ userStore.name.charAt(0).toUpperCase() }}
                  </template>
                </a-avatar>
                
                <template #content>
                  <a-doption>
                    <router-link to="/profile" class="dropdown-item">
                      <icon-user /> 个人中心
                    </router-link>
                  </a-doption>
                  
                  <a-doption>
                    <div class="dropdown-item" @click="handleLogout">
                      <icon-export /> 退出登录
                    </div>
                  </a-doption>
                </template>
              </a-dropdown>
            </template>
            
            <template v-else>
              <router-link to="/login">
                <a-button type="text">登录</a-button>
              </router-link>
              
              <router-link to="/register">
                <a-button type="primary">注册</a-button>
              </router-link>
            </template>
          </div>
        </div>
      </a-layout-header>
      
      <a-layout-content class="content">
        <router-view />
      </a-layout-content>
      
      <a-layout-footer class="footer">
        <div class="footer-content">
          <p>© {{ new Date().getFullYear() }} 家长助手 - 面向学生家长的工具集合平台</p>
        </div>
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { IconUser, IconExport } from '@arco-design/web-vue/es/icon'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 当前激活的菜单项
const activeKey = computed(() => {
  const path = route.path
  
  if (path === '/') return 'home'
  if (path.startsWith('/tools')) return 'tools'
  if (path.startsWith('/chess')) return 'chess'
  
  return ''
})

// 处理退出登录
const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 100%;
}

.logo {
  font-size: 20px;
  font-weight: 600;
}

.logo a {
  color: #165dff;
  text-decoration: none;
}

.nav-menu {
  flex: 1;
  margin: 0 20px;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  cursor: pointer;
  background-color: #165dff;
  color: #fff;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  color: #1d2129;
  text-decoration: none;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f2f3f5;
}

.content {
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px - 64px);
}

.footer {
  background-color: #fff;
  padding: 20px 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
  color: #86909c;
}
</style> 