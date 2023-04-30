<script setup>
import { NTabs, NTabPane, NForm, NFormItem,} from 'naive-ui'

const route = useRoute()
const useStore = useUserStore()
const project = reactive ({})

async function getProject () {
    console.log('getProject')
    for (const key in project) {
        delete project[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch(`/api/project/${route.params.id}`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data project',data.value)
            Object.assign(project, data.value)
            console.log('result project',project)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

onMounted(() => {
    getProject()
})

</script>
<!-- //v-if=useStore.is_superuser -->
<template> 
  <div class="py-2 px-2" v-if=useStore.isAuthenticated>
    專案：<span class="text-pink-600 font-semibold"> {{ project.name }} </span>
    順序碼：<span class="text-pink-600 font-semibold"> {{ project.turn }}</span>
    <div class="space-y-4">
        <n-tabs type="segment"
        default-value="projectStaff">
            <n-tab-pane name="projectStaff" tab="填班人員設定">
                <ProjectStaff :projectId="route.params.id" />
            </n-tab-pane>
            <n-tab-pane name="projectShift" tab="填班班種設定">
                {{ route.params.id }}
            </n-tab-pane>
        </n-tabs>
    </div>
  </div>
</template>

<style scoped>
</style>