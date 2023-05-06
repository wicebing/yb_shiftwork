<script setup>
import { NInput, NButton, NForm, NFormItemRow,NFormItem, NDatePicker, NSwitch, NDrawer, NDrawerContent, NTransfer } from 'naive-ui'
import { NTabs, NTabPane } from 'naive-ui'

const route = useRoute()
const useStore = useUserStore()

const props = defineProps({
    projectId: {
        type: String,
        required: true
    }
})

const dateRange = ref()
const paneName = ref('selectDate')
const startDate = ref()
const endDate = ref()
const resultShift = reactive ({})
const optionsSelectShift = ref([]);
const result = reactive ({})
const errors = ref([])
const daysOfWeek = ref(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
const weekStartsOn = ref(0) // 0 for Sunday, 1 for Monday
const activeDrawerScheduleEdit = ref(false)
const editScheduleDate = ref()
const editScheduleItem = reactive([])
const editingItem = reactive([])


const columnsScheduleItem = ref([
    {
      title: 'id',
      key: 'id'
    },
    {
      title: 'shift_name',
      key: 'shift_name'
    },
    {
      title: 'date',
      key: 'date'
    },
    {
      title: 'shift',
      key: 'shift'
    },
    {
      title: 'project',
      key: 'project'
    },
    {
      title: 'Delete',
      key: '刪',
    }
])

const optionsShift = computed(() => {
    console.log('optionsShift', resultShift);

    return Object.values(resultShift).map((Group) => {
        return {
            label: Group.name,
            value: Group.id,
        };
    });
});

const transformedResult = computed(() => {
    const calendar = [];
    const sortedDates = Object.keys(result);

    for (const key of sortedDates) {
        const item = result[key];
        const dateObj = new Date(item.date_name);
        const dayOfWeek = dateObj.getDay();
        const firstDayOfMonth = new Date(dateObj.getFullYear(), dateObj.getMonth(), 1).getDay();
        const adjustedDay = (dayOfWeek - weekStartsOn.value + 7) % 7
        const weekOfMonth = Math.floor((dateObj.getDate() + firstDayOfMonth - weekStartsOn.value - 1) / 7);

        if (!calendar[weekOfMonth]) {
        calendar[weekOfMonth] = new Array(7).fill(null);
        }

        if (!calendar[weekOfMonth][adjustedDay]) {
        calendar[weekOfMonth][adjustedDay] = {
            date_name: item.date_name,
            items: []
        };
        }
        calendar[weekOfMonth][adjustedDay].items.push(item);
    }
    return calendar;
})

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function editSchedule(day) {
    console.log('editSchedule')
    activeDrawerScheduleEdit.value = true
    Object.assign(editScheduleItem, day.items)
    editScheduleDate.value = day.date_name
}

async function submitDateRange() { 
    [startDate.value, endDate.value] = dateRange.value.map(date => formatDate(new Date(date)))
    console.log('start',startDate)
    console.log('end',endDate)
    try {
        const { data, pending, refresh, error } = await useFetch('/api/date/', {
            method: 'POST',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
            },
            body: JSON.stringify({
                start_date: startDate.value,
                end_date: endDate.value
            })
        })
        paneName.value = 'selecShift'
    } catch (error) {
        console.error('Error submitting date range:', error)
    }
}

async function submitShiftDate() {
    try {
        const { data, pending, refresh, error } = await useFetch('/api/createProjectSchedules/', {
            method: 'POST',
            baseURL: 'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}`,
            },
            body: JSON.stringify({
                start_date: startDate.value,
                end_date: endDate.value,
                shift_ids: optionsSelectShift.value,
                project: props.projectId
            })
        });

        console.log('Shift dates submitted', data);
        paneName.value = 'showProjectShift'
        getSchedule()
    } catch (error) {
        console.error('Error submitting shift dates:', error);
    }
}



async function getShift () {
    console.log('getShift')
    for (const key in resultShift) {
        delete resultShift[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch('/api/shift/', {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data shift',data.value)
            Object.assign(resultShift, data.value.results)
            console.log('result shift',resultShift)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

async function getSchedule () {
    console.log('getSchedule')
    for (const key in result) {
        delete result[key];
    }
    try{
        const { data, pending, refresh, error } = await useFetch(`/api/schedule/?project_id=${props.projectId}`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data getSchedule',data.value)
            Object.assign(result, data.value.results)
            console.log('result getSchedule',result)
        } else {
            console.log('error',error)
        }
    } catch (err) {
        console.log('err',err)
    }
}

async function deleteData(row) {
    try {
        console.log('deleteData', row)
        const { data, pending, refresh, error } = await useFetch(`/api/project/${row.id}`, {
        method: 'DELETE',
        baseURL: 'http://localhost:8000',
        headers: {
            Authorization: `JWT ${useStore.token}`,
        },
        })

        console.log('deleteData', row)
        console.log('Deleted successfully')
        console.log('Error: ', error.value)
    } catch (error) {
        console.error('Error deleting data:', error);
    }
    getProject()
}

onMounted(() => {
    getShift()
    getSchedule()
})

</script>

<template>
    <div v-if="startDate">
        專案起訖日期：<span class="text-pink-600 font-semibold"> {{ startDate }} </span> ~ 
        <span class="text-pink-600 font-semibold"> {{ endDate }} </span>
    </div>
    
    <n-tabs
    :default-value="result ? 'showProjectShift' : 'selectDate'"
    v-model:value="paneName">
        <n-tab-pane name="selectDate" tab="Step 1 日期範圍">
            <n-form>
                日期起迄日：
                <n-date-picker
                v-model:value="dateRange"
                update-value-on-close
                panel
                type="daterange"
                :on-confirm="submitDateRange"
                />        
            </n-form>
        </n-tab-pane>
        <n-tab-pane name="selecShift" tab="Step 2 班種" v-if="startDate">
            {{ optionsSelectShift }}
            <n-transfer ref="transfer"
                    :options="optionsShift" v-model:value="optionsSelectShift"
                    source-filterable
                    />
            <n-button type="info" @click="submitShiftDate">
                確認班種
            </n-button>
        </n-tab-pane>
        <n-tab-pane name="showProjectShift" tab="Step 3 班表" v-if="result">
            <table class="table-auto min-w-full border border-slate-300">
                <thead class="bg-gray-50 border border-slate-300">
                    <tr>
                        <th v-for="day in daysOfWeek" :key="day" class="bg-gray-50 border border-slate-300"> 
                            {{ day }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="week in transformedResult" class="bg-gray-50 border border-slate-300">
                        <td v-for="day in week" :key="day?.date_name" class="bg-gray-50 border border-slate-300">
                            <div v-if="day" class="date">
                                {{ day.date_name }}
                                <n-button @click=editSchedule(day)>Edit</n-button>
                            </div>
                            <ul v-if="day">
                                <li v-for="item in day.items" :key="item.id">
                                    {{ item.shift_name }}
                                    <div>{{ item.holiday }}</div>
                                </li>
                            </ul>
                        </td>
                    </tr>
                </tbody>
            </table>
            {{ result }}
        </n-tab-pane>
    </n-tabs>
    <n-drawer v-model:show="activeDrawerScheduleEdit" :width="502" :placement="placementDrawer">
        <n-drawer-content title="調整當日班種" closable>
            <n-form>
                <n-button type="error" block secondary strong @click=null>
                刪除 <span class="text-pink-600 font-semibold"> {{ editScheduleDate }} </span> 班表
                </n-button>
                <table class="table-auto min-w-full">
                        <thead class="bg-gray-50">
                            <tr>
                                <th v-for="col in columnsScheduleItem" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="(res, rowIndex) in editScheduleItem">
                                <td v-for="col in columnsScheduleItem" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                                    <n-button 
                                    v-if="!res[col.key] && col.title === 'Edit'"
                                    secondary
                                    type='info'
                                    @click= null
                                    >
                                        {{ col.key }}
                                    </n-button>

                                    <n-button 
                                    v-if="!res[col.key]  && col.title === 'Delete'"
                                    secondary strong type='error'
                                    @click=null
                                    :disabled="!editingItem[rowIndex]"
                                    >
                                        {{ col.key }}
                                    </n-button>

                                    <n-switch v-if="col.title==='Delete'" v-model:value="editingItem[rowIndex]" />

                                    <div v-if="res[col.key] !== null && res[col.key] !== undefined ">
                                        {{ res[col.key] }}
                                    </div>                       
                                </td>
                            </tr>
                        </tbody>
                    </table>
                <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 rounded-xl">
                    <p v-for="error in errors" :key="error">
                        {{ error }}
                    </p>
                </div>

            </n-form>
        </n-drawer-content>
    </n-drawer>
</template>