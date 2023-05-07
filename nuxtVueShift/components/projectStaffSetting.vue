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
      title: '備註',
      key: 'footnote'
    },
])

const result = reactive ({})
const errors = ref([])
const resultStaff = reactive ({})
const resultGroupsCC = reactive ({})
const resultGroupsTT = reactive ({})
const resultGroupsMM = reactive ({})
const resultGroupsICU0 = reactive ({})
const resultGroupsICU1 = reactive ({})
const switchRefs = reactive ({})

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

function compareAge(birthdayString, threshold) {
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
    const boolAge = age > threshold
    return boolAge
}

function isStaffInResultGroups(staffToCheck, resultGroups) {
  for (const key in resultGroups) {
    const staff = resultGroups[key];
    if (staff.staff === staffToCheck) {
      return true;
    }
  }
  return false;
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

async function getGroup (groupname_name, resultGroups) {
    console.log('getGroup')
    errors.value = []
    for (const key in resultGroups) {
        delete resultGroups[key];
    }
    try {
        const { data, pending, refresh, error } = await useFetch(`/api/group/?groupname_name=${groupname_name}`, {
            method: 'GET',
            baseURL:'http://localhost:8000',
            headers: {
                Authorization: `JWT ${useStore.token}` 
            }
        })

        if (data.value) {
            console.log('data resultGroups',data.value)
            Object.assign(resultGroups, data.value.results)        
        } else {
            console.log('error resultGroups',error)
            errors.value.push(error)
            errors.value.push(data.value.results)
        }
    } catch {
        console.log('error Group',error)
        errors.value.push(error)
    }
}

onMounted(() => {
    getProjectAttend()
    getGroup('CC', resultGroupsCC)
    getGroup('TT', resultGroupsTT)
    getGroup('MM', resultGroupsMM)
    getGroup('ICU0', resultGroupsICU0)
    getGroup('ICU1', resultGroupsICU1)
})

</script>

<template>
    <table class="table-auto min-w-full">
        <thead>
            <tr>
                <th v-for="col in columns" class="px-2 py-4 text-xs font-bold text-gray-500 text-left" scope="col">{{ col.title }}</th>
            </tr>
        </thead>
        <tbody>
            <template v-for="(res, rowOuterIndex) in resultStaff" >
                <tr v-for="(resmb, rowIndex) in res.group_members" class="border border-slate-300">
                    <td v-for="(col, colIndex) in columns" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                        <div v-if="col.key==='name'">
                            {{res.sequence}} - 
                            <span :class="{'bg-red-200':res.groupname_name==='A', 'bg-red-100':res.groupname_name==='B'}">
                                {{res.groupname_name}}</span> - 
                            <span :class="{'bg-green-200':isStaffInResultGroups(resmb.staff,resultGroupsCC),
                                            'bg-green-400':isStaffInResultGroups(resmb.staff,resultGroupsTT),
                                            'bg-green-600':isStaffInResultGroups(resmb.staff,resultGroupsMM),
                                            'bg-green-800':isStaffInResultGroups(resmb.staff,resultGroupsICU0),
                                            'bg-green-700':isStaffInResultGroups(resmb.staff,resultGroupsICU1),}">
                            {{ resmb.staff_name }}</span> - 
                            <span>{{ resmb.staff }}</span>
                        </div>
                        <div v-if="col.key==='age'" 
                        :class="{'bg-yellow-200':compareAge(resmb.staff_birthday, 50)}">
                            {{ calculateAge(resmb.staff_birthday) }}
                        </div>
                        <div v-if="col.key==='footnote'">
                            <li v-if="isStaffInResultGroups(resmb.staff,resultGroupsTT)">教學組不超排</li>
                            <li v-if="isStaffInResultGroups(resmb.staff,resultGroupsCC)">重症組</li>
                            <li v-if="isStaffInResultGroups(resmb.staff,resultGroupsMM)">行政組不超排</li>
                            <li v-if="isStaffInResultGroups(resmb.staff,resultGroupsICU0)">ICU不超排</li>
                            <li v-if="isStaffInResultGroups(resmb.staff,resultGroupsICU1)">ICU不超排</li>
                            <li v-if="compareAge(resmb.staff_birthday, 50)">年齡超過50歲</li>
                            <template v-for="rule in res.related_rules">
                                <li>{{rule.description}}</li>
                            </template>                        
                        </div>
                    </td>
                </tr>
            </template >
        </tbody>
    </table>
</template>

