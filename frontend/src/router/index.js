import { createRouter, createWebHistory } from "vue-router";
import landing from "../pages/landing.vue";

const routes = [
    // Public Pages
    {
        path: "/",
        component: landing
    },

    // Auth Pages
    {
        path: "/auth",
        component: () => import("../layout/AuthLayout.vue"),
        children: [
            {
                path:"login", component: () => import("../pages/auth/Login.vue")
            },
            {
                path:"register", component: () => import("../pages/auth/Register.vue")
            },
            {
            path: "",
            redirect: "/auth/login"
            }
        ]
    }
]

  // Auth Pages
  {
    path: "/auth",
    component: () => import("../layout/AuthLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("../pages/auth/Login.vue"),
      },
      {
        path: "register",
        component: () => import("../pages/auth/Register.vue"),
      },
    ],
  },

  // Admin Pages
  {
    path: "/admin",
    component: () => import("../layout/AdminLayout.vue"),
    meta: { role: "admin" },
    children: [
      {
        path: "",
        component: () => import("../pages/admin/Dashboard.vue"),
      },
      {
        path: "doctors",
        component: () => import("../pages/admin/Doctor.vue"),
      },
      {
        path: "patients",
        component: () => import("../pages/admin/Patient.vue"),
      },
      {
        path: "appointments",
        component: () => import("../pages/admin/Appointments.vue"),
      },
    ],
  },

  // Doctor
  {
    path: "/doctor",
    component: () => import("../layout/DoctorLayout.vue"),
    meta: { role: "doctor"},
    children: [
      {
        path: "",
        component: () => import("../pages/doctor/Dashboard.vue")
      },
      {
        path: "patients",
        component: () => import("../pages/doctor/Patient.vue"),
      },
      {
        path: "patients/:id",
        component: () => import("../pages/doctor/PatientDetails.vue"),
      },
      {
        path:"appointments",
        component: () => import("../pages/doctor/Appointments.vue"),
      },
      {
        path: "appointments/:id",
        component: () => import("../pages/doctor/PatientAppointmentReport.vue"),
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// router.beforeEach((to, from, next) => {
//   const user = JSON.parse(localStorage.getItem('user'))

//   // 🌐 Public routes
//   if (to.path === '/' || to.path.startsWith('/auth')) {
//     return next()
//   }

//   // 🔐 Protected routes
// //   if (to.meta.role) {
// //     if (!user) return next('/auth/login')

// //     if (user.role !== to.meta.role) {
// //       return next('/')
// //     }
// //   }

//   next()
// })

export default router;
