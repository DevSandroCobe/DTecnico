<template>
  <div class="migracion-container">
    <h1>🚚 Migrador de Base de Datos</h1>
    <p class="subtitulo">Migre los datos antes de generar reportes. Seleccione la fecha a migrar:</p>
    <div class="formulario">
      <label for="fecha">Fecha de migración:</label>
      <input type="date" v-model="fecha" id="fecha" />
      <button :disabled="cargando" @click="migrarDatos">
        {{ cargando ? 'Migrando...' : 'Migrar Datos' }}
      </button>
    </div>
    <router-link to="/">
      <button class="volver">🔙 Volver</button>
    </router-link>
    <div v-if="cargando" class="loader"></div>
  </div>
</template>

<script>
import Swal from 'sweetalert2';

export default {
  name: 'MigracionView',
  data() {
    return {
      fecha: '',
      cargando: false
    };
  },
  methods: {
    async migrarDatos() {
      if (!this.fecha) {
        this.mostrarError('Fecha requerida', 'Debes seleccionar una fecha para migrar.');
        return;
      }
      const fechaFormateada = new Date(this.fecha).toISOString().split('T')[0];
      this.cargando = true;
      try {
        const response = await fetch('http://localhost:8000/api/importar_traslados/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ fecha: fechaFormateada })
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'Error en la migración');
        }
        Swal.fire({
          icon: 'success',
          title: '✅ ¡Migración finalizada!',
          text: 'Datos migrados correctamente',
          confirmButtonColor: '#8bb915'
        });
      } catch (error) {
        this.mostrarError('Error en la migración', error.message);
      } finally {
        this.cargando = false;
      }
    },
    mostrarError(titulo, mensaje) {
      Swal.fire({
        icon: 'error',
        title: titulo,
        text: mensaje,
        confirmButtonColor: '#8bb915'
      });
    }
  }
};
</script>

<style scoped>
.migracion-container {
  max-width: 420px;
  margin: 3.5rem auto 0 auto;
  padding: 2.2rem 2rem 2.5rem 2rem;
  background: #fff;
  border: 2px solid #4caf50;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(44, 62, 80, 0.10);
  text-align: center;
  font-family: 'Rubik', Arial, sans-serif;
}

.migracion-container h1 {
  color: #2e7d32;
  font-size: 1.5rem;
  margin-bottom: 0.7rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.subtitulo {
  color: #444;
  font-size: 1.08rem;
  margin-bottom: 1.5rem;
}

.formulario {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  align-items: center;
  margin-bottom: 1.7rem;
}

label {
  font-weight: 600;
  color: #388e3c;
  margin-bottom: 0.2rem;
}

input[type="date"] {
  padding: 0.7rem 1.1rem;
  border-radius: 8px;
  border: 1px solid #bdbdbd;
  font-size: 1.08rem;
  width: 100%;
  max-width: 220px;
  background: #f8fafc;
  transition: border 0.2s;
}

input[type="date"]:focus {
  border-color: #4caf50;
}

button {
  background: linear-gradient(90deg, #43a047 0%, #8bc34a 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 1.6rem;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
  margin-top: 0.2rem;
}

button:hover:not(:disabled) {
  background: linear-gradient(90deg, #388e3c 0%, #689f38 100%);
  transform: scale(1.04);
}

button:disabled {
  background: #c1d892;
  cursor: not-allowed;
}

button.volver {
  background: #e0e0e0;
  color: #333;
  margin-top: 1.2rem;
  font-weight: 500;
}

button.volver:hover {
  background: #c2c2c2;
}

/* Loader animado */
.loader {
  height: 60px;
  aspect-ratio: 1;
  position: relative;
  margin: 1.5rem auto 0 auto;
}
.loader::before,
.loader::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  transform-origin: bottom;
}
.loader::after {
  background:
    radial-gradient(at 75% 15%,#fffb,#0000 35%),
    radial-gradient(at 80% 40%,#0000,#0008),
    radial-gradient(circle  5px,#fff 94%,#0000),
    radial-gradient(circle 10px,#000 94%,#0000),
    linear-gradient(#F93318 0 0) top   /100% calc(50% - 5px),
    linear-gradient(#fff    0 0) bottom/100% calc(50% - 5px)
    #000;
  background-repeat: no-repeat;
  animation: l20 1s infinite cubic-bezier(0.5,120,0.5,-120);
}
.loader::before {
  background:#ddd;
  filter: blur(8px);
  transform: scaleY(0.4) translate(-13px, 0px);
}
@keyframes l20 { 
 30%,70% {transform:rotate(0deg)}
 49.99%  {transform:rotate(0.2deg)}
 50%     {transform:rotate(-0.2deg)}
}

/* Responsivo */
@media (max-width: 600px) {
  .migracion-container {
    padding: 1.2rem;
    border-radius: 10px;
  }
  .formulario { gap: 0.7rem; }
  input[type="date"], button { max-width: 100%; }
}
</style>
