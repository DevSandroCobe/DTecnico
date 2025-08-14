# 🌐 Frontend de Actas de Despacho (Vue 3 + Vite)

Este frontend permite gestionar y visualizar la migración y generación de actas de despacho, integrándose con el backend en Python para automatizar procesos y descargar PDFs.

---

## 🚀 Tecnologías principales

- [Vue 3](https://vuejs.org/) (Composition API, `<script setup>`)
- [Vite](https://vitejs.dev/) (desarrollo ultrarrápido)
- [Axios](https://axios-http.com/) (peticiones HTTP)
- [Pinia](https://pinia.vuejs.org/) (gestión de estado, si aplica)

---

## ⚡ Instalación y uso

1. Instala dependencias:
	```bash
	npm install
	```

2. Ejecuta en modo desarrollo:
	```bash
	npm run dev
	```

3. Accede a la app en [http://localhost:5173](http://localhost:5173) (o el puerto que indique Vite).

---

## 📁 Estructura principal

- `src/` — Código fuente principal
  - `components/` — Componentes reutilizables (formularios, tablas, etc.)
  - `views/` — Vistas principales (ActaDespachoTraslado, ActaDespachoVenta, Home, etc.)
  - `router/` — Rutas de la SPA
  - `assets/` — Imágenes y estilos
- `public/` — Archivos estáticos

---

## 🔗 Conexión con el backend

Configura la URL base de la API en los servicios o variables de entorno según tu entorno local o de producción.

---

## 📝 Notas

- El frontend está optimizado para trabajar con el backend de migración y generación de PDFs.
- Puedes personalizar estilos y componentes según la identidad visual de tu empresa.

---

¿Dudas o sugerencias? ¡Contribuye o abre un issue!
