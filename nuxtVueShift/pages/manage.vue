<script setup>
import { NTabs, NTabPane } from 'naive-ui'

const useStore = useUserStore()
</script>
<!-- //v-if=useStore.is_superuser -->
<template> 
  <div class="py-2 px-2">
    <div class="space-y-4">
        <n-tabs type="segment">
            <n-tab-pane name="UserStaff" tab="員工資料">
                <manageStaff />
            </n-tab-pane>
            <n-tab-pane name="the beatles" tab="the Beatles">
            Hey Jude
            </n-tab-pane>
            <n-tab-pane name="jay chou" tab="Jay Chou">
            Qilixiang
            </n-tab-pane>
        </n-tabs>
    </div>
  </div>
</template>

<style scoped>
.n-layout-sider {
  background: rgba(214, 213, 132, 0.342);
}
.n-layout-content {
  background: rgba(255, 254, 184, 0.308);
}
</style>