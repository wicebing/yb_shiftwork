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

const columns = ref([
    {
      title: '人員',
      key: 'name'
    },
    {
      title: '年齡',
      key: 'age'
    },
    {
      title: '行政',
      key: 'manage'
    },
    {
      title: 'ICU',
      key: 'icu'
    },
    {
      title: '超排',
      key: 'extra'
    },
    {
      title: '減班',
      key: 'relax'
    },
    {
      title: '半百',
      key: 'yo50'
    },
    {
      title: 'Edit',
      key: 'Edit',
    },
])

const result = reactive ({})
const resultStaff = reactive ({})

function calculateAge(birthdayString) {
    const birthday = new Date(birthdayString);
    const today = new Date();

    let years = today.getFullYear() - birthday.getFullYear();
    let months = today.getMonth() - birthday.getMonth();

    // Adjust years and months if the birthday hasn't occurred yet this year
    if (today.getDate() < birthday.getDate()) {
    months--;
    }
    if (months < 0) {
    years--;
    months += 12;
    }
    const age =  years+months/12
    const roundedAge = Math.floor(age * 10) / 10;
    return roundedAge
}

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

async function getProjectAttend () {
    console.log('getProjectAttend')
    for (const key in resultStaff) {
        delete resultStaff[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch(`/api/projectAttend/?project_id=${props.projectId}&ordering=sequence`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data getProjectAttend',data.value)
            Object.assign(resultStaff, data.value.results)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

onMounted(() => {
    getProject()
    getProjectAttend()
})

</script>

<template>
    <n-tabs default-value="shiftCount">
        <n-tab-pane name="shiftCount" tab="應填班數">
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
        </n-tab-pane>
        <n-tab-pane name="shiftShare" tab="分配班數">
            <table class="table-auto min-w-full">
                <thead>
                    <tr>
                        <th v-for="col in columns" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
                    </tr>
                </thead>
                <tbody>
                    <template  v-for="(res, rowIndex) in resultStaff" >
                        <tr v-for="(resmb, rowIndex) in res.group_members">
                            <td class="border px-4 py-2">{{res.groupname_name}} - {{ resmb.staff_name }} - {{ resmb.staff }} </td>
                            <td class="border px-4 py-2">{{ calculateAge(resmb.staff_birthday) }}</td>
                            {{ resmb.staff_birthday }}
                        </tr>
                    </template >
                </tbody>
            </table>
        </n-tab-pane> 
    </n-tabs>
  
</template>

