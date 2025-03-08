<template>
  <div class="profile-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="profile-header">
          <template #title>
            <div class="flex items-center">
              <icon-user class="mr-2" />
              <span>个人中心</span>
            </div>
          </template>
          <p class="text-gray-500">查看和管理您的个人信息。</p>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="mt-4">
      <a-col :span="8">
        <a-card>
          <template #title>
            <div class="flex items-center">
              <icon-user-group class="mr-2" />
              <span>基本信息</span>
            </div>
          </template>
          <div class="user-info">
            <div class="avatar-container">
              <a-avatar :size="100" :style="{ backgroundColor: '#165DFF' }">
                <template #icon>
                  <icon-user />
                </template>
              </a-avatar>
            </div>
            <div class="user-details mt-4">
              <h3 class="text-lg font-medium">{{ userInfo?.name || userInfo?.username || '用户' }}</h3>
              <p class="text-gray-500">{{ userInfo?.email || '未设置邮箱' }}</p>
            </div>
            <a-divider />
            <a-button type="outline" long @click="showEditModal">
              <template #icon>
                <icon-edit />
              </template>
              编辑个人信息
            </a-button>
          </div>
        </a-card>
      </a-col>
      <a-col :span="16">
        <a-card>
          <template #title>
            <div class="flex items-center">
              <icon-dashboard class="mr-2" />
              <span>使用统计</span>
            </div>
          </template>
          <a-row :gutter="[16, 16]">
            <a-col :span="8">
              <a-statistic title="已上传棋谱" :value="statistics.notationCount" />
            </a-col>
            <a-col :span="8">
              <a-statistic title="练习次数" :value="statistics.practiceCount" />
            </a-col>
            <a-col :span="8">
              <a-statistic title="使用天数" :value="statistics.useDays" />
            </a-col>
          </a-row>
          <a-divider />
          <div class="chart-container">
            <div class="chart-placeholder">
              <p>此处应显示使用统计图表</p>
              <p class="text-gray-500">实际项目中应集成ECharts等图表组件</p>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="mt-4">
      <a-col :span="24">
        <a-card>
          <template #title>
            <div class="flex items-center">
              <icon-settings class="mr-2" />
              <span>账号设置</span>
            </div>
          </template>
          <a-space direction="vertical" style="width: 100%">
            <a-card hoverable>
              <div class="flex justify-between items-center">
                <div>
                  <h4 class="font-medium">修改密码</h4>
                  <p class="text-gray-500">定期更新密码可以提高账号安全性</p>
                </div>
                <a-button @click="showPasswordModal">
                  <template #icon>
                    <icon-lock />
                  </template>
                  修改密码
                </a-button>
              </div>
            </a-card>
            <a-card hoverable>
              <div class="flex justify-between items-center">
                <div>
                  <h4 class="font-medium">退出登录</h4>
                  <p class="text-gray-500">安全退出当前账号</p>
                </div>
                <a-button status="danger" @click="confirmLogout">
                  <template #icon>
                    <icon-export />
                  </template>
                  退出登录
                </a-button>
              </div>
            </a-card>
          </a-space>
        </a-card>
      </a-col>
    </a-row>

    <!-- 编辑个人信息弹窗 -->
    <a-modal
      v-model:visible="editModalVisible"
      title="编辑个人信息"
      @ok="handleEditSubmit"
      @cancel="editModalVisible = false"
      :ok-loading="submitting"
      ok-text="保存"
      cancel-text="取消"
    >
      <a-form :model="editForm" layout="vertical">
        <a-form-item field="username" label="用户名" :rules="[{ required: true, message: '请输入用户名' }]">
          <a-input v-model="editForm.username" placeholder="请输入用户名" allow-clear disabled />
        </a-form-item>
        <a-form-item field="email" label="邮箱" :rules="[
          { required: true, message: '请输入邮箱' },
          { type: 'email', message: '请输入有效的邮箱地址' }
        ]">
          <a-input v-model="editForm.email" placeholder="请输入邮箱" allow-clear />
        </a-form-item>
        <a-form-item field="name" label="姓名">
          <a-input v-model="editForm.name" placeholder="请输入姓名" allow-clear />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 修改密码弹窗 -->
    <a-modal
      v-model:visible="passwordModalVisible"
      title="修改密码"
      @ok="handlePasswordSubmit"
      @cancel="passwordModalVisible = false"
      :ok-loading="submitting"
      ok-text="保存"
      cancel-text="取消"
    >
      <a-form :model="passwordForm" layout="vertical">
        <a-form-item field="oldPassword" label="当前密码" :rules="[{ required: true, message: '请输入当前密码' }]">
          <a-input-password v-model="passwordForm.oldPassword" placeholder="请输入当前密码" allow-clear />
        </a-form-item>
        <a-form-item field="newPassword" label="新密码" :rules="[
          { required: true, message: '请输入新密码' },
          { minLength: 6, message: '密码长度不能少于6位' }
        ]">
          <a-input-password v-model="passwordForm.newPassword" placeholder="请输入新密码" allow-clear />
        </a-form-item>
        <a-form-item field="confirmPassword" label="确认新密码" :rules="[
          { required: true, message: '请确认新密码' },
          { validator: validateConfirmPassword, message: '两次输入的密码不一致' }
        ]">
          <a-input-password v-model="passwordForm.confirmPassword" placeholder="请确认新密码" allow-clear />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useChessStore } from '@/stores/chessStore'
import { useNotification } from '@/composables/useNotification'
import {
  IconUser,
  IconUserGroup,
  IconDashboard,
  IconSettings,
  IconEdit,
  IconLock,
  IconExport
} from '@arco-design/web-vue/es/icon'

// 路由
const router = useRouter()

// 状态管理
const userStore = useUserStore()
const chessStore = useChessStore()
const { success, error, confirm } = useNotification()

// 用户信息
const userInfo = computed(() => userStore.userInfo)

// 模态框状态
const editModalVisible = ref(false)
const passwordModalVisible = ref(false)
const submitting = ref(false)

// 编辑表单
const editForm = reactive({
  username: '',
  email: '',
  name: ''
})

// 密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 使用统计数据（示例数据，实际应从API获取）
const statistics = reactive({
  notationCount: 0,
  practiceCount: 0,
  useDays: 0
})

// 验证确认密码
const validateConfirmPassword = (value: string) => {
  return passwordForm.newPassword === value
}

// 显示编辑个人信息弹窗
const showEditModal = () => {
  if (!userInfo.value) return
  
  // 初始化编辑表单
  editForm.username = userInfo.value.username
  editForm.email = userInfo.value.email
  editForm.name = userInfo.value.name || ''
  
  // 显示编辑弹窗
  editModalVisible.value = true
}

// 提交编辑个人信息
const handleEditSubmit = async () => {
  if (!editForm.username || !editForm.email) {
    error('请填写必填字段')
    return
  }
  
  try {
    submitting.value = true
    // 这里应该调用更新用户信息的API
    // 由于当前没有实现该API，仅做模拟
    setTimeout(() => {
      success('个人信息更新成功')
      editModalVisible.value = false
      submitting.value = false
    }, 1000)
  } catch (err) {
    error('更新失败')
    submitting.value = false
  }
}

// 显示修改密码弹窗
const showPasswordModal = () => {
  // 重置密码表单
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  
  // 显示密码弹窗
  passwordModalVisible.value = true
}

// 提交修改密码
const handlePasswordSubmit = async () => {
  if (!passwordForm.oldPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
    error('请填写所有密码字段')
    return
  }
  
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    error('两次输入的密码不一致')
    return
  }
  
  try {
    submitting.value = true
    // 这里应该调用修改密码的API
    // 由于当前没有实现该API，仅做模拟
    setTimeout(() => {
      success('密码修改成功')
      passwordModalVisible.value = false
      submitting.value = false
    }, 1000)
  } catch (err) {
    error('密码修改失败')
    submitting.value = false
  }
}

// 确认退出登录
const confirmLogout = () => {
  confirm({
    title: '确认退出',
    content: '确定要退出登录吗？',
    onOk: async () => {
      try {
        await userStore.logoutAction()
        success('退出登录成功')
        router.push('/auth/login')
      } catch (err) {
        error('退出登录失败')
      }
    }
  })
}

// 获取统计数据
const fetchStatistics = async () => {
  try {
    // 这里应该调用获取统计数据的API
    // 由于当前没有实现该API，使用棋谱数量作为示例
    await chessStore.fetchNotations()
    statistics.notationCount = chessStore.notations.length
    statistics.practiceCount = Math.floor(Math.random() * 50) // 随机示例数据
    statistics.useDays = Math.floor(Math.random() * 30) // 随机示例数据
  } catch (err) {
    console.error('获取统计数据失败', err)
  }
}

// 页面加载时获取用户信息和统计数据
onMounted(async () => {
  if (!userInfo.value) {
    await userStore.fetchUserInfo()
  }
  await fetchStatistics()
})
</script>

<style scoped>
.profile-container {
  padding: 16px;
}

.profile-header {
  margin-bottom: 16px;
}

.user-info {
  text-align: center;
}

.avatar-container {
  display: flex;
  justify-content: center;
}

.chart-container {
  margin-top: 16px;
  height: 300px;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: var(--color-fill-2);
  border-radius: 4px;
}
</style> 