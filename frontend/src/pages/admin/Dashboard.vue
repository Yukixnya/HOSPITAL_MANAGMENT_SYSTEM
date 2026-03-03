<script setup>
import { ref } from 'vue';
import { 
  Stethoscope, User, DollarSign, Calendar, 
  CheckCircle2, AlertTriangle, PlusCircle, 
  LayoutGrid // Added for consistent icons
} from 'lucide-vue-next';

import StatCard from '../../components/StateCard.vue';
import AppointmentTrendsChart from '../../components/AppointmentTrendsChart.vue';

const stats = [
    { title: 'Total Doctors', value: '154', trend: '+2.4%', isUp: true, icon: Stethoscope, iconBg: 'bg-blue-50', iconColor: 'text-blue-600' },
    { title: 'Active Patients', value: '12,840', trend: '+5.1%', isUp: true, icon: User, iconBg: 'bg-indigo-50', iconColor: 'text-indigo-600' },
    { title: 'Monthly Revenue', value: '$45,200', trend: '+12.8%', isUp: true, icon: DollarSign, iconBg: 'bg-emerald-50', iconColor: 'text-emerald-600' },
    { title: "Today's Appointments", value: '84', trend: '-3.2%', isUp: false, icon: Calendar, iconBg: 'bg-orange-50', iconColor: 'text-orange-600' },
];

const activity = [
    { id: 1, title: 'New appointment', detail: 'scheduled for John Doe', time: '10 minutes ago', icon: PlusCircle, color: 'text-blue-500', bg: 'bg-blue-50' },
    { id: 2, title: 'Surgery completed', detail: 'by Dr. Michael Chen', time: '45 minutes ago', icon: CheckCircle2, color: 'text-emerald-500', bg: 'bg-emerald-50' },
    { id: 3, title: 'Critical alert', detail: 'Low stock for insulin in pharmacy', time: '2 hours ago', icon: AlertTriangle, color: 'text-orange-500', bg: 'bg-orange-50' },
];
</script>

<template>
    <div class="p-8 bg-slate-50 min-h-screen">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatCard v-for="stat in stats" :key="stat.title" v-bind="stat" />
        </div>

        <div class="grid grid-cols-12 gap-8">
            
            <div class="col-span-12 lg:col-span-8 space-y-8">
                <AppointmentTrendsChart />

                <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
                    <div class="p-6 flex justify-between items-center border-b border-gray-50">
                        <h3 class="font-bold text-slate-800">Active Staff</h3>
                        <button class="text-blue-600 text-sm font-bold hover:underline">View All</button>
                    </div>
                    <div class="divide-y divide-gray-50">
                        <div v-for="staff in 2" :key="staff"
                            class="p-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                            <div class="flex items-center gap-4">
                                <div class="w-12 h-12 rounded-full bg-slate-200 overflow-hidden border border-gray-100">
                                    <img :src="`https://i.pravatar.cc/150?u=${staff}`" alt="avatar" />
                                </div>
                                <div>
                                    <p class="font-bold text-slate-800">Dr. Sarah Johnson</p>
                                    <p class="text-xs text-slate-400">Cardiology • <span class="text-emerald-500">On Duty</span></p>
                                </div>
                            </div>
                            <div class="w-2.5 h-2.5 rounded-full bg-emerald-500 ring-4 ring-emerald-50"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-span-12 lg:col-span-4">
                <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full flex flex-col">
                    <h3 class="font-bold text-slate-800 text-lg mb-8">Recent Activity</h3>

                    <div class="flex-1 space-y-8 relative">
                        <div class="absolute left-5 top-2 bottom-2 w-0.5 bg-slate-100"></div>

                        <div v-for="item in activity" :key="item.id" class="relative flex gap-4">
                            <div :class="[item.bg, item.color, 'z-10 p-2.5 rounded-full h-10 w-10 flex items-center justify-center ring-4 ring-white shadow-sm']">
                                <component :is="item.icon" :size="18" />
                            </div>
                            <div class="pt-1">
                                <p class="text-sm text-slate-600 leading-snug">
                                    <span class="font-bold text-slate-800">{{ item.title }}</span> {{ item.detail }}
                                </p>
                                <p class="text-xs text-slate-400 mt-1">{{ item.time }}</p>
                            </div>
                        </div>
                    </div>

                    <button class="w-full mt-8 py-3 bg-slate-50 text-slate-500 font-bold text-sm rounded-xl hover:bg-slate-100 transition-colors">
                        View Full Logs
                    </button>
                </div>
            </div>

        </div>
    </div>
</template>