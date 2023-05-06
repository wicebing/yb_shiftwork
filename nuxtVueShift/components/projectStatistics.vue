<script setup>
import { NInput, NButton, NForm, NFormItemRow, NFormItem, NDatePicker, NSwitch, NDrawer, NDrawerContent, NTransfer, NTabs, NTabPane, NCard, NGrid, NGridItem } from "naive-ui";

const route = useRoute()
const useStore = useUserStore()

const props = defineProps({
    projectId: {
        type: String,
        required: true
    }
})

const result = reactive ({})

async function getProject () {
    console.log('getProject')
    for (const key in result) {
        delete result[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch(`/api/scheduleStatistic/?project_id=${props.projectId}`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data project',data.value)
            Object.assign(result, data.value)
            console.log('result project',result)
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

<template>
  <n-grid>
    <n-grid-item span="24">
      <n-card>
        <template #header>
          <span>總班數： {{ result.total_count }}</span>
        </template>
      </n-card>
    </n-grid-item>
    <n-grid-item span="6">
      <n-card>
        <template #header>
          <span>Character count</span>
        </template>
        <div v-for="item in result.character_count" :key="item.shift__charactor">
          {{ item.shift__charactor }}: {{ item.count }}
        </div>
      </n-card>
    </n-grid-item>
    <n-grid-item span="6">
      <n-card>
        <template #header>
          <span>Holiday count</span>
        </template>
        <div v-for="item in result.holiday_count" :key="item.date__holiday">
          {{ item.date__holiday ? "假日" : "平日" }}: {{ item.count }}
        </div>
      </n-card>
    </n-grid-item>
    <n-grid-item span="6">
      <n-card>
        <template #header>
          <span>Name count</span>
        </template>
        <div v-for="item in result.name_count" :key="item.shift__name">
          {{ item.shift__name }}: {{ item.count }}
        </div>
      </n-card>
    </n-grid-item>
    <n-grid-item span="6">
      <n-card>
        <template #header>
          <span>Intersection counts</span>
        </template>
        <div v-for="item in result.intersection_counts" :key="item.shift__charactor + '_' + item.date__holiday">
          {{ item.shift__charactor }} - {{ item.date__holiday ?  "假日" : "平日" }} : {{ item.count }}
        </div>
      </n-card>
    </n-grid-item>
  </n-grid>
</template>

