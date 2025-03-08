import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { post, get, put } from '@/utils/http';
import { Message } from '@arco-design/web-vue';

// 用户状态接口
interface UserState {
  id: number | null;
  username: string;
  email: string;
  name: string;
  avatar: string;
  token: string;
  refreshToken: string;
  isLoggedIn: boolean;
}

// 创建用户状态存储
export const useUserStore = defineStore('user', () => {
  // 状态
  const id = ref<number | null>(null);
  const username = ref('');
  const email = ref('');
  const name = ref('');
  const avatar = ref('');
  const token = ref(localStorage.getItem('token') || '');
  const refreshToken = ref(localStorage.getItem('refreshToken') || '');
  const isLoggedIn = ref(!!localStorage.getItem('token'));

  // 计算属性
  const userInfo = computed(() => {
    return {
      id: id.value,
      username: username.value,
      email: email.value,
      name: name.value,
      avatar: avatar.value
    };
  });

  const hasToken = computed(() => !!token.value);

  // 方法
  function setUserInfo(userData: any) {
    id.value = userData.id;
    username.value = userData.username;
    email.value = userData.email;
    name.value = userData.name || userData.username;
    avatar.value = userData.avatar || '';
  }

  function setToken(tokenValue: string, refreshTokenValue: string) {
    token.value = tokenValue;
    refreshToken.value = refreshTokenValue;
    isLoggedIn.value = true;
    
    // 保存到本地存储
    localStorage.setItem('token', tokenValue);
    localStorage.setItem('refreshToken', refreshTokenValue);
  }

  function clearToken() {
    token.value = '';
    refreshToken.value = '';
    isLoggedIn.value = false;
    
    // 从本地存储中移除
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  }

  async function login(emailValue: string, password: string) {
    try {
      // 调用登录API
      const response: any = await post('/auth/login', {
        email: emailValue,
        password
      });
      
      // 设置用户信息
      setUserInfo(response.user);
      setToken(response.access_token, response.refresh_token);
      
      Message.success(`欢迎回来，${name.value}`);
      
      return true;
    } catch (error) {
      console.error('登录失败:', error);
      Message.error('登录失败，请检查您的邮箱和密码');
      return false;
    }
  }

  async function register(userData: { username: string; email: string; password: string; name?: string }) {
    try {
      // 调用注册API
      const response: any = await post('/auth/register', userData);
      
      // 设置用户信息
      setUserInfo(response.user);
      setToken(response.access_token, response.refresh_token);
      
      Message.success('注册成功，欢迎加入！');
      
      return true;
    } catch (error) {
      console.error('注册失败:', error);
      Message.error('注册失败，请检查您的输入并重试');
      return false;
    }
  }

  async function logout() {
    try {
      if (token.value) {
        await post('/auth/logout');
      }
    } catch (error) {
      console.error('登出失败:', error);
    } finally {
      clearToken();
      id.value = null;
      username.value = '';
      email.value = '';
      name.value = '';
      avatar.value = '';
      
      Message.info('您已成功退出登录');
    }
  }

  async function refreshAccessToken() {
    try {
      if (!refreshToken.value) {
        return false;
      }
      
      const response: any = await post('/auth/refresh', {
        refresh_token: refreshToken.value
      });
      
      token.value = response.access_token;
      localStorage.setItem('token', response.access_token);
      
      return true;
    } catch (error) {
      console.error('刷新令牌失败:', error);
      clearToken();
      return false;
    }
  }

  async function fetchUserInfo() {
    try {
      if (!token.value) {
        return false;
      }
      
      const userData: any = await get('/user/profile');
      setUserInfo(userData);
      
      return true;
    } catch (error) {
      console.error('获取用户信息失败:', error);
      return false;
    }
  }

  async function updateUserInfo(userData: { name?: string; avatar?: string }) {
    try {
      const response: any = await put('/user/profile', userData);
      
      setUserInfo({
        ...userInfo.value,
        ...userData
      });
      
      return response;
    } catch (error) {
      console.error('更新用户信息失败:', error);
      throw error;
    }
  }

  async function changePassword(oldPassword: string, newPassword: string) {
    try {
      await put('/user/password', {
        old_password: oldPassword,
        new_password: newPassword
      });
      
      Message.success('密码修改成功');
      return true;
    } catch (error) {
      console.error('修改密码失败:', error);
      throw error;
    }
  }

  return {
    // 状态
    id,
    username,
    email,
    name,
    avatar,
    token,
    refreshToken,
    isLoggedIn,
    
    // 计算属性
    userInfo,
    hasToken,
    
    // 方法
    setUserInfo,
    setToken,
    clearToken,
    login,
    register,
    logout,
    refreshAccessToken,
    fetchUserInfo,
    updateUserInfo,
    changePassword
  };
}); 