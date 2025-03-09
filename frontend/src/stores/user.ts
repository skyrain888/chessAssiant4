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
      console.log('开始登录，邮箱:', emailValue)
      
      // 调用登录API
      const response: any = await post('/api/auth/login', {
        email: emailValue,
        password
      });
      
      console.log('登录响应:', response)
      
      // 检查响应格式
      if (response && response.access_token && response.refresh_token && response.user) {
        // 设置用户信息
        setUserInfo(response.user);
        setToken(response.access_token, response.refresh_token);
        
        console.log('登录成功，已设置token和用户信息')
        console.log('访问令牌:', response.access_token.substring(0, 15) + '...')
        console.log('刷新令牌:', response.refresh_token.substring(0, 15) + '...')
        
        Message.success(`欢迎回来，${name.value}`);
        
        return true;
      } else if (response && response.code === 200 && response.data) {
        // 标准响应格式
        const data = response.data
        if (data.access_token && data.refresh_token && data.user) {
          setUserInfo(data.user)
          setToken(data.access_token, data.refresh_token)
          
          console.log('登录成功，已设置token和用户信息(标准格式)')
          console.log('访问令牌:', data.access_token.substring(0, 15) + '...')
          console.log('刷新令牌:', data.refresh_token.substring(0, 15) + '...')
          
          Message.success(`欢迎回来，${name.value}`)
          return true
        }
      }
      
      console.error('登录响应格式不正确:', response)
      Message.error('登录失败，服务器响应格式不正确')
      return false
    } catch (error: any) {
      console.error('登录失败:', error)
      
      if (error.response && error.response.data && error.response.data.message) {
        Message.error(error.response.data.message)
      } else {
        Message.error('登录失败，请检查您的邮箱和密码')
      }
      
      return false
    }
  }

  async function register(userData: { username: string; email: string; password: string; name?: string }) {
    try {
      // 调用注册API
      const response: any = await post('/api/auth/register', userData);
      
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
        await post('/api/auth/logout');
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

  async function fetchUserInfo() {
    try {
      if (!token.value) {
        console.log('没有token，无法获取用户信息');
        return false;
      }
      
      console.log('开始获取用户信息，当前token:', token.value.substring(0, 10) + '...');
      
      const response: any = await get('/api/user/profile');
      
      console.log('获取用户信息响应:', response);
      
      // 检查响应格式
      if (response && response.code === 200 && response.data) {
        // 标准响应格式
        setUserInfo(response.data);
        console.log('用户信息设置成功(标准格式)');
      } else if (response && response.id) {
        // 直接返回用户数据的格式
        setUserInfo(response);
        console.log('用户信息设置成功(直接格式)');
      } else {
        console.error('获取用户信息响应格式不正确:', response);
        return false;
      }
      
      return true;
    } catch (error: any) {
      console.error('获取用户信息失败:', error);
      
      // 如果是401错误，可能是token过期，尝试刷新token
      if (error.response && error.response.status === 401) {
        console.log('Token已过期，尝试刷新Token');
        const refreshSuccess = await refreshAccessToken();
        if (refreshSuccess) {
          // 刷新token成功，重新获取用户信息
          console.log('Token刷新成功，重新获取用户信息');
          return fetchUserInfo();
        } else {
          // 刷新token失败，清除登录状态
          console.log('Token刷新失败，清除登录状态');
          clearToken();
        }
      } else if (error.response && error.response.status === 422) {
        // 422错误可能是请求验证失败，尝试刷新token
        console.log('请求验证失败，尝试刷新Token');
        const refreshSuccess = await refreshAccessToken();
        if (refreshSuccess) {
          // 刷新token成功，重新获取用户信息
          console.log('Token刷新成功，重新获取用户信息');
          return fetchUserInfo();
        } else {
          // 刷新token失败，清除登录状态
          console.log('Token刷新失败，清除登录状态');
          clearToken();
        }
      }
      
      return false;
    }
  }

  async function updateUserInfo(userData: { name?: string; avatar?: string }) {
    try {
      const response: any = await put('/api/user/profile', userData);
      
      // 检查响应格式
      if (response && response.code === 200 && response.data && response.data.user) {
        // 标准响应格式
        setUserInfo(response.data.user);
      } else if (response && response.user) {
        // 直接返回user字段的格式
        setUserInfo(response.user);
      } else {
        console.error('更新用户信息响应格式不正确:', response);
        throw new Error('更新用户信息响应格式不正确');
      }
      
      return true;
    } catch (error: any) {
      console.error('更新用户信息失败:', error);
      
      // 如果是401错误，可能是token过期
      if (error.response && error.response.status === 401) {
        Message.error('登录已过期，请重新登录');
        clearToken();
      } else if (error.response && error.response.data && error.response.data.message) {
        // 显示服务器返回的错误消息
        Message.error(error.response.data.message);
      } else {
        Message.error('更新用户信息失败');
      }
      
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

  async function refreshAccessToken() {
    try {
      if (!refreshToken.value) {
        console.log('没有刷新令牌，无法刷新访问令牌');
        return false;
      }
      
      console.log('开始刷新访问令牌，当前刷新令牌:', refreshToken.value.substring(0, 10) + '...');
      
      const response: any = await post('/api/auth/refresh', {
        refresh_token: refreshToken.value
      });
      
      console.log('刷新令牌响应:', response);
      
      if (response && response.access_token) {
        token.value = response.access_token;
        localStorage.setItem('token', response.access_token);
        console.log('访问令牌刷新成功');
        return true;
      } else {
        console.error('刷新令牌响应格式不正确:', response);
        clearToken();
        return false;
      }
    } catch (error: any) {
      console.error('刷新令牌失败:', error);
      
      // 如果是401错误，说明刷新令牌也过期了
      if (error.response && error.response.status === 401) {
        console.log('刷新令牌已过期，清除登录状态');
        Message.error('登录已过期，请重新登录');
      }
      
      clearToken();
      return false;
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
    fetchUserInfo,
    updateUserInfo,
    changePassword,
    refreshAccessToken
  };
}); 