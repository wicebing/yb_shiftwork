<script setup>
import { NInput, NButton, NForm, NFormItemRow,NFormItem, NDatePicker, NSwitch, NDrawer, NDrawerContent } from 'naive-ui'

const route = useRoute()
const useStore = useUserStore()

const result = reactive ({})


const props = defineProps({
    projectId: {
        type: String,
        required: true
    }
})


const columns = ref([
    {
      title: 'project',
      key: 'project'
    },
    {
      title: 'groupname',
      key: 'groupname'
    },
    {
      title: 'constraint',
      key: 'constraint'
    },
    {
      title: 'sequence',
      key: 'sequence'
    },
    {
      title: 'Edit',
      key: 'Edit',
    },
    {
      title: 'Delete',
      key: '刪',
    }
])

async function getProject () {
    console.log('getProject')
    for (const key in result) {
        delete result[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch('/api/projectAttend/?ordering=sequence', {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })
        console.log('data',data.value)
        console.log('error',error)

        Object.assign(result, data.value.results)
        console.log('result',result)
    } catch (err) {
        console.log('err',err)
    }
}


onMounted(() => {
})

</script>
<!-- //v-if=useStore.is_superuser -->
<template> 
    <table class="table-auto min-w-full">
        <thead class="bg-gray-50">
            <tr>
                <th v-for="col in columns" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            <tr v-for="(res, rowIndex) in result">
                <td v-for="col in columns" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                    <n-button 
                    v-if="!res[col.key] && col.title === 'Edit'"
                    secondary
                    type='info'
                    @click= editData(res)
                    >
                        {{ col.key }}
                    </n-button>

                    <n-button 
                    v-if="!res[col.key]  && col.title === 'Delete'"
                    secondary strong type='error'
                    @click=deleteData(res)
                    :disabled="!editing[rowIndex]"
                    >
                        {{ col.key }}
                    </n-button>

                    <n-switch v-if="col.title==='Delete'" v-model:value="editing[rowIndex]" />

                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key !== 'name'">
                        {{ res[col.key] }}
                    </div>
                    <div v-if="res[col.key] !== null && res[col.key] !== undefined && col.key === 'name'">
                        <n-button dashed
                        @click="toProjectID(res.id)">
                            {{ res[col.key] }}
                        </n-button>
                    </div>                          
                </td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
</style>