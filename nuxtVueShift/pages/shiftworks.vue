<script setup>
import { NTabs, NTabPane, } from 'naive-ui'

const useStore = useUserStore()

onMounted(() => {

})

</script>
<!-- //v-if=useStore.is_superuser -->
<template> 
  <div class="py-2 px-2" v-if=useStore.isAuthenticated>
    <div class="space-y-4">
        <n-tabs type="segment"
        default-value="allGroup">
            <n-tab-pane name="allGroup" tab="填班組別">
                <Groupname />
            </n-tab-pane>
            <n-tab-pane name="allPositionCharactor" tab="班種性質設定">
                <PositionCharactor />
            </n-tab-pane>
            <n-tab-pane name="allPosition" tab="班種總覽">
                <PositionProjects />
            </n-tab-pane>
            <n-tab-pane name="allRules" tab="填班規則">
                <rules />
            </n-tab-pane>
            <n-tab-pane name="allExtra" tab="超排控制項目">
                <extra />
            </n-tab-pane>
            <n-tab-pane name="allRelax" tab="減班控制項目">
                <relax />
            </n-tab-pane>
        </n-tabs>
    </div>
  </div>
</template>

<style scoped>
</style>