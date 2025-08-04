<template>
  <div class="migracion-container">
    <h1>🚚 Migrador De Base de Datos</h1>

    <label for="fecha">Fecha de migración:</label>
    <input type="date" v-model="fecha" id="fecha" />
    <br />
    <button :disabled="cargando" @click="migrarDatos">
      {{ cargando ? 'Migrando...' : 'Migrar Datos' }}
    </button>
    <br />
    <router-link to="/"><button>Volver</button></router-link>

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

    // Formatea la fecha manualmente por seguridad
    const fechaFormateada = new Date(this.fecha).toISOString().split('T')[0];

    this.cargando = true;

    try {
      console.log("Fecha para enviar:", this.fecha);

      const response = await fetch('http://localhost:8000/api/importar/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ 
          fecha: fechaFormateada,
          tabla: "*"
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error en la migración');
      }

      Swal.fire({
        icon: 'success',
        title: '¡Migración exitosa!',
        html: `
          <p>${data.message}</p>
          <p>Fecha: ${data.fecha}</p>
          <p>Tabla: ${data.tabla}</p>
        `,
        confirmButtonColor: '#8bb915'
      });

    } catch (error) {
      console.error('Error detallado:', error);
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
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  border: 2px solid #8bb915;
  border-radius: 15px;
  background-color: #fefefe;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  text-align: center;
  font-family: 'Rubik', sans-serif;
}

.migracion-container h1 {
  color: #4c4c4c;
  margin-bottom: 25px;
  font-weight: bold;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

input[type="date"] {
  padding: 10px 15px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
  transition: border 0.3s;
  width: 100%;
  max-width: 300px;
  margin: 0 auto 20px;
}

input[type="date"]:focus {
  border-color: #8bb915;
}

button {
  padding: 10px 18px;
  font-size: 1rem;
  margin: 10px 8px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background-color: #8bb915;
  color: #fff;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover:not(:disabled) {
  background-color: #7aa512;
  transform: scale(1.03);
}

button:disabled {
  background-color: #c1d892;
  cursor: not-allowed;
}

.router-link button {
  background-color: #555;
}

.router-link button:hover {
  background-color: #333;
}

/* Loader animado */
.loader {
  height: 60px;
  aspect-ratio: 1;
  position: relative;
  margin: 20px auto;
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
    radial-gradient(at 75% 15%, #fffb, #0000 35%),
    radial-gradient(at 80% 40%, #0000, #0008),
    radial-gradient(circle 5px, #fff 94%, #0000),
    radial-gradient(circle 10px, #000 94%, #0000),
    linear-gradient(#F93318 0 0) top / 100% calc(50% - 5px),
    linear-gradient(#fff 0 0) bottom / 100% calc(50% - 5px)
    #000;
  background-repeat: no-repeat;
  animation: l20 1s infinite cubic-bezier(0.5, 120, 0.5, -120);
}
.loader::before {
  background: #ddd;
  filter: blur(8px);
  transform: scaleY(0.4) translate(-13px, 0px);
}
@keyframes l20 {
  30%, 70% { transform: rotate(0deg) }
  49.99%  { transform: rotate(0.2deg) }
  50%     { transform: rotate(-0.2deg) }
}

/* Responsivo */
@media (max-width: 600px) {
  .migracion-container {
    padding: 20px;
    border-radius: 10px;
  }

  input[type="date"],
  button {
    width: 100%;
    max-width: 100%;
  }
}

</style>
