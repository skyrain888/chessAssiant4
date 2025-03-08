<template>
  <div class="profile-container">
    <a-card class="profile-card">
      <template #title>个人中心</template>
      
      <div class="profile-header">
        <a-avatar :size="80" class="profile-avatar">
          <template v-if="userStore.avatar">
            <img :src="userStore.avatar" alt="avatar" />
          </template>
          <template v-else>
            {{ userStore.name.charAt(0).toUpperCase() }}
          </template>
        </a-avatar>
        <div class="profile-info">
          <h2>{{ userStore.name }}</h2>
          <p>{{ userStore.email }}</p>
        </div>
      </div>
      
      <a-divider />
      
      <a-form :model="form" layout="vertical" @submit.prevent="handleSubmit">
        <a-form-item field="name" label="姓名">
          <a-input v-model="form.name" placeholder="请输入姓名" />
        </a-form-item>
        
        <a-form-item field="avatar" label="头像">
          <a-upload
            action="/api/user/avatar"
            :headers="{ Authorization: `Bearer ${userStore.token}` }"
            :show-file-list="false"
            accept="image/*"
            @success="handleAvatarSuccess"
            @error="handleAvatarError"
          >
            <template #upload-button>
              <div class="avatar-uploader">
                <a-avatar :size="64" class="avatar-preview">
                  <template v-if="form.avatar">
                    <img :src="form.avatar" alt="avatar" />
                  </template>
                  <template v-else-if="userStore.avatar">
                    <img :src="userStore.avatar" alt="avatar" />
                  </template>
                  <template v-else>
                    {{ form.name.charAt(0).toUpperCase() }}
                  </template>
                </a-avatar>
                <div class="avatar-upload-text">点击上传</div>
              </div>
            </template>
          </a-upload>
        </a-form-item>
        
        <a-form-item>
          <a-button type="primary" html-type="submit" :loading="loading">保存修改</a-button>
        </a-form-item>
      </a-form>
      
      <a-divider />
      
      <div class="change-password">
        <h3>修改密码</h3>
        <a-form :model="passwordForm" layout="vertical" @submit.prevent="handlePasswordSubmit">
          <a-form-item field="oldPassword" label="当前密码" :rules="[{ required: true, message: '请输入当前密码' }]">
            <a-input-password v-model="passwordForm.oldPassword" placeholder="请输入当前密码" />
          </a-form-item>
          
          <a-form-item field="newPassword" label="新密码" :rules="[
            { required: true, message: '请输入新密码' },
            { minLength: 6, message: '密码长度不能少于6个字符' }
          ]">
            <a-input-password v-model="passwordForm.newPassword" placeholder="请输入新密码" />
          </a-form-item>
          
          <a-form-item field="confirmPassword" label="确认新密码" :rules="[
            { required: true, message: '请确认新密码' },
            { validator: validateConfirmPassword, message: '两次输入的密码不一致' }
          ]">
            <a-input-password v-model="passwordForm.confirmPassword" placeholder="请确认新密码" />
          </a-form-item>
          
          <a-form-item>
            <a-button type="primary" html-type="submit" :loading="passwordLoading">修改密码</a-button>
          </a-form-item>
        </a-form>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { Message } from '@arco-design/web-vue'
import { useUserStore } from '@/stores/user'

// 用户状态
const userStore = useUserStore()

// 表单数据
const form = reactive({
  name: userStore.name || '',
  avatar: userStore.avatar || ''
})

// 密码表单数据
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 状态
const loading = ref(false)
const passwordLoading = ref(false)

// 验证确认密码
const validateConfirmPassword = (value: string) => {
  return value === passwordForm.newPassword
}

// 处理头像上传成功
const handleAvatarSuccess = (response: any) => {
  form.avatar = response.avatar
  Message.success('头像上传成功')
}

// 处理头像上传失败
const handleAvatarError = () => {
  Message.error('头像上传失败')
}

// 提交个人信息表单
const handleSubmit = async () => {
  loading.value = true
  
  try {
    const success = await userStore.updateUserInfo({
      name: form.name,
      avatar: form.avatar
    })
    
    if (success) {
      Message.success('个人信息更新成功')
    } else {
      Message.error('个人信息更新失败')
    }
  } catch (err) {
    console.error('更新个人信息错误:', err)
    Message.error('发生错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 提交密码表单
const handlePasswordSubmit = async () => {
  passwordLoading.value = true
  
  try {
    const success = await userStore.changePassword(
      passwordForm.oldPassword,
      passwordForm.newPassword
    )
    
    if (success) {
      // 清空表单
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
    }
  } catch (err) {
    console.error('修改密码错误:', err)
    Message.error('发生错误，请稍后重试')
  } finally {
    passwordLoading.value = false
  }
}

// 初始化
onMounted(async () => {
  // 如果用户信息不完整，尝试获取
  if (!userStore.name || !userStore.email) {
    await userStore.fetchUserInfo()
    
    // 更新表单数据
    form.name = userStore.name
    form.avatar = userStore.avatar
  }
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-card {
  margin-bottom: 24px;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.profile-avatar {
  margin-right: 24px;
  background-color: #165dff;
  color: #fff;
  font-size: 32px;
}

.profile-info h2 {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 600;
}

.profile-info p {
  margin: 0;
  color: #86909c;
}

.avatar-uploader {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.avatar-preview {
  background-color: #f2f3f5;
  margin-bottom: 8px;
  font-size: 24px;
}

.avatar-upload-text {
  color: #165dff;
  font-size: 14px;
}

.change-password {
  margin-top: 24px;
}

.change-password h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 600;
}
</style> 