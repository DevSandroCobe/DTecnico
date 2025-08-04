<template>
  <div class="truncate-view">
    <h2>🧪 Truncar tabla en SQL Server</h2>

    <select v-model="tabla">
      <option disabled value="">Selecciona una tabla</option>
      <option v-for="t in tablas" :key="t" :value="t">{{ t }}</option>
    </select>

    <button @click="truncarTabla">Truncar</button>

    <p v-if="mensaje">{{ mensaje }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      tabla: '',
      tablas: ['OITM', 'DLN1', 'OBTW'], // Puedes modificar esta lista
      mensaje: ''
    }
  },
  methods: {
    async truncarTabla() {
      if (!this.tabla) {
        this.mensaje = '⚠️ Debes seleccionar una tabla primero.'
        return
      }

      try {
        const res = await axios.post(`http://localhost:8000/api/truncate/${this.tabla}`)

        this.mensaje = res.data.message || '✅ Truncado exitoso.'
      } catch (error) {
        this.mensaje = error.response?.data?.message || '❌ Error al truncar tabla.'
      }
    }
  }
}
</script>

<style scoped>
.truncate-view {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 10px;
}
select, button {
  display: block;
  margin: 1rem auto;
  padding: 0.5rem 1rem;
}
</style>
