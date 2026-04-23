<script setup lang="js">
// @ts-nocheck
import AppLayout from '@/layouts/AppLayout.vue';
import { Head } from '@inertiajs/vue3';
import 'ant-design-vue/dist/reset.css';
import moment from 'moment';
import { computed, h, ref } from 'vue';
import { usePagination } from 'vue-request';
import { Button as AButton, Input as AInput, Select as ASelect, Table as ATable, Tooltip as ATooltip } from 'ant-design-vue';

moment.locale('id');

const breadcrumbs = [
    {
        title: 'Device',
        href: '/devices',
    },
];

const props = defineProps({
    organizations: {
        type: Array,
        required: false,
        default: () => [],
    },
    statuses: {
        type: Array,
        required: false,
        default: () => [],
    },
});

const lastParams = ref({});
const tableKey = ref(0);
const searchInput = ref();
const selectedOrganization = ref([]);
const selectedStatus = ref(null);
const selectedBitdefenderId = ref(null);
const selectedLastUpdate = ref(null);

function formatDateTime(value) {
    if (!value) {
        return '-';
    }

    const parsed = moment(value);
    if (!parsed.isValid()) {
        return '-';
    }

    return parsed.format('DD MMM YYYY HH:mm:ss');
}

function fromNow(value) {
    if (!value) {
        return '-';
    }

    const parsed = moment(value);
    if (!parsed.isValid()) {
        return '-';
    }

    return parsed.fromNow();
}

const textFilter = {
    customFilterDropdown: true,
    onFilterDropdownOpenChange: (visible) => {
        if (visible) {
            setTimeout(() => {
                searchInput.value?.focus();
            }, 100);
        }
    },
};

const columns = [
    {
        title: 'Satker',
        key: 'organization_name',
        width: 120,
        sorter: true,
    },
    {
        title: 'ID Bitdefender',
        dataIndex: 'id_bitdefender',
        width: 150,
        sorter: true,
        ...textFilter,
    },
    {
        title: 'Device Name',
        dataIndex: 'device_name',
        width: 150,
        sorter: true,
        ...textFilter,
    },
    {
        title: 'NUP',
        dataIndex: 'nup',
        width: 140,
        sorter: true,
        ...textFilter,
    },
    {
        title: 'User',
        dataIndex: 'user',
        width: 110,
        sorter: true,
        ...textFilter,
    },
    {
        title: 'Last Update',
        key: 'last_update_at',
        dataIndex: 'last_update_at',
        width: 100,
        sorter: true,
    },
    {
        title: 'Status',
        key: 'status_name',
        width: 100,
        customRender: ({ record }) => {
            const status = record?.status?.name;
            return h(
                'span',
                {
                    class: status ? 'rounded bg-blue-100 px-2 py-1 text-xs text-blue-800' : 'text-slate-400',
                },
                status || '-',
            );
        },
    },
    {
        title: 'Created By',
        dataIndex: 'created_by',
        width: 120,
        sorter: true,
        ...textFilter,
    },
];

const normalizeTableFilters = (filters) => {
    const normalized = {};

    Object.entries(filters ?? {}).forEach(([key, value]) => {
        if (!Array.isArray(value) || value.length === 0) {
            return;
        }

        normalized[key] = value
            .filter((v) => v !== null && v !== undefined)
            .map((v) => String(v));
    });

    return normalized;
};

const buildQueryString = (params = {}) => {
    const query = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (value === null || value === undefined || value === '') {
            return;
        }

        if (Array.isArray(value)) {
            value.forEach((item) => query.append(`${key}[]`, String(item)));
            return;
        }

        query.append(key, String(value));
    });

    return query.toString();
};

const queryData = async (params = {}) => {
    lastParams.value = params;

    const {
        current = 1,
        pageSize = 50,
        sortField,
        sortOrder,
        ...filterQuery
    } = params;

    const size = Number(pageSize);
    const page = Number(current);

    const queryString = buildQueryString({
        start: Math.max(0, (page - 1) * size),
        length: size,
        sortField,
        sortOrder,
        ...filterQuery,
    });

    const response = await fetch(`/devices/data?${queryString}`, {
        headers: { Accept: 'application/json' },
        credentials: 'same-origin',
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.status}`);
    }

    const payload = await response.json();

    return {
        list: payload.data || [],
        total: payload.total || 0,
    };
};

const {
    data: dataSource,
    run,
    loading,
    current,
    pageSize,
    total,
} = usePagination(queryData, {
    defaultParams: [{
        current: 1,
        pageSize: 50,
    }],
    pagination: {
        currentKey: 'current',
        pageSizeKey: 'pageSize',
    },
});

const pagination = computed(() => ({
    total: total.value,
    current: current.value,
    pageSize: pageSize.value,
    showSizeChanger: true,
    pageSizeOptions: ['10', '20', '50'],
}));

const handleTableChange = (pag, filters, sorter) => {
    const filterQuery = normalizeTableFilters(filters);

    run({
        current: pag.current,
        pageSize: pag.pageSize,
        sortField: sorter.field ?? sorter.columnKey,
        sortOrder: sorter.order,
        ...filterQuery,
        ...(selectedOrganization.value?.length > 0 ? { organization: selectedOrganization.value } : {}),
        ...(selectedStatus.value ? { status: selectedStatus.value } : {}),
        ...(selectedBitdefenderId.value ? { bitdefender_id: selectedBitdefenderId.value } : {}),
        ...(selectedLastUpdate.value ? { last_update: selectedLastUpdate.value } : {}),
    });
};

const handleFilter = () => {
    const rest = { ...lastParams.value };
    delete rest.organization;
    delete rest.status;
    delete rest.bitdefender_id;
    delete rest.last_update;

    run({
        ...rest,
        current: 1,
        ...(selectedOrganization.value?.length > 0 ? { organization: selectedOrganization.value } : {}),
        ...(selectedStatus.value ? { status: selectedStatus.value } : {}),
        ...(selectedBitdefenderId.value ? { bitdefender_id: selectedBitdefenderId.value } : {}),
        ...(selectedLastUpdate.value ? { last_update: selectedLastUpdate.value } : {}),
    });
};

const handleResetAll = () => {
    tableKey.value += 1;
    selectedOrganization.value = [];
    selectedStatus.value = null;
    selectedBitdefenderId.value = null;
    selectedLastUpdate.value = null;
    run({
        current: 1,
        pageSize: pageSize.value,
    });
};

const handleSearch = (_selectedKeys, confirm, _dataIndex) => {
    confirm();
};

const handleReset = (clearFilters) => {
    clearFilters({ confirm: true });
};

const organizationOptions = computed(() =>
    [
        { label: 'Tanpa Satker', value: '__NULL__' },
        ...(props.organizations || []).map((organization) => ({
            label: `[${organization.short_code || '-'}] ${organization.name || '-'}`,
            value: organization.id,
        })),
    ],
);

const statusOptions = computed(() =>
    (props.statuses || []).map((status) => ({
        label: status.name,
        value: status.id,
    })),
);

const bitdefenderIdOptions = [
    { label: 'All', value: '' },
    { label: 'Has ID', value: 'has' },
    { label: 'No ID', value: 'no' },
];

const lastUpdateOptions = [
    { label: 'All', value: '' },
    { label: 'More than 10 days ago', value: 'over_10_days' },
    { label: 'More than 1 month ago', value: 'over_1_month' },
    { label: 'More than 3 months ago', value: 'over_3_months' },
    { label: 'More than 6 months ago', value: 'over_6_months' },
];
</script>

<template>
    <Head title="Device" />

    <AppLayout :breadcrumbs="breadcrumbs">
        <div class="flex h-full flex-1 flex-col gap-4 rounded-xl p-4">
            <div class="mb-2 flex flex-wrap items-center gap-3 rounded-lg border p-3">
                <ASelect
                    v-model:value="selectedOrganization"
                    mode="multiple"
                    max-tag-count="responsive"
                    placeholder="Semua Satker"
                    class="w-60"
                    :options="organizationOptions"
                    allow-clear
                    @change="handleFilter"
                />

                <ASelect
                    v-model:value="selectedStatus"
                    placeholder="Semua Status"
                    class="w-44"
                    :options="statusOptions"
                    allow-clear
                    @change="handleFilter"
                />

                <ASelect
                    v-model:value="selectedBitdefenderId"
                    placeholder="ID Bitdefender"
                    class="w-40"
                    :options="bitdefenderIdOptions"
                    @change="handleFilter"
                />

                <ASelect
                    v-model:value="selectedLastUpdate"
                    placeholder="Last Update"
                    class="w-40"
                    :options="lastUpdateOptions"
                    @change="handleFilter"
                />

                <ATooltip title="Reset Semua Filter">
                    <AButton @click="handleResetAll">Reset</AButton>
                </ATooltip>
            </div>

            <ATable
                :key="tableKey"
                :scroll="{ y: 620 }"
                :columns="columns"
                :row-key="(record) => record.id"
                :data-source="dataSource?.list ?? []"
                :pagination="pagination"
                :loading="loading"
                size="small"
                @change="handleTableChange"
            >
                <template #bodyCell="{ column, text, record }">
                    <template v-if="column.key === 'organization_name'">
                        <span>{{ record.organization?.long_code ? `[${record.organization?.long_code}] ${record.organization?.name}` : '' }}</span>
                    </template>

                    <template v-else-if="column.key === 'last_update_at'">
                        <span :title="formatDateTime(text)">{{ fromNow(text) }}</span>
                    </template>

                    <template v-else-if="column.key === 'created_at'">
                        <span :title="formatDateTime(text)">{{ fromNow(text) }}</span>
                    </template>

                    <template v-else-if="column.key === 'updated_at'">
                        <span :title="formatDateTime(text)">{{ fromNow(text) }}</span>
                    </template>
                </template>

                <template #customFilterDropdown="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }">
                    <div style="padding: 8px">
                        <AInput
                            ref="searchInput"
                            :placeholder="`Search ${column.dataIndex}`"
                            :value="selectedKeys[0]"
                            style="width: 220px; margin-bottom: 8px; display: block"
                            @change="(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])"
                            @pressEnter="handleSearch(selectedKeys, confirm, column.dataIndex)"
                        />
                        <AButton
                            type="primary"
                            size="small"
                            style="width: 90px; margin-right: 8px"
                            @click="handleSearch(selectedKeys, confirm, column.dataIndex)"
                        >
                            Search
                        </AButton>
                        <AButton size="small" style="width: 90px" @click="handleReset(clearFilters)">
                            Reset
                        </AButton>
                    </div>
                </template>
            </ATable>
        </div>
    </AppLayout>
</template>