<template>
  <div class="contenedor">
    <h2>🧾 ACTAS DE DESPACHO - VENTAS</h2>

    <p>Ingrese la fecha de los documentos por exportar</p>

    <label for="fecha">Fecha:</label>
    <input type="date" v-model="fecha" id="fecha" />

    <div class="botones">
      <button :disabled="cargando" @click="generarPDF">
        📄 Generar PDF
      </button>
      <router-link to="/">
        <button class="volver">🔙 Volver</button>
      </router-link>
    </div>

    <div v-if="cargando" class="loader"></div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  name: "ActaDespachoVentas",
  data() {
    return {
      fecha: "",
      cargando: false
    };
  },
  mounted() {
    Swal.fire({
      icon: 'warning',
      title: '⚠️ Atención',
      text: 'Primero migre la base de datos. Si ya lo hizo, puede continuar.',
      confirmButtonColor: '#8bb915'
    });
  },
  methods: {
    async generarPDF() {
      if (!this.fecha) {
        Swal.fire({
          icon: 'info',
          title: 'Fecha requerida',
          text: 'Por favor seleccione una fecha para generar el PDF.',
          confirmButtonColor: '#8bb915'
        });
        return;
      }

      this.cargando = true;

      try {
        const response = await fetch("http://localhost:8000/api/generar_pdf/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            fecha: this.fecha,
            tipo: "venta"
          })
        });

        if (!response.ok) {
          throw new Error('Respuesta inválida del servidor');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `Acta_Despacho_Venta_${this.fecha}.pdf`;
        a.click();
        window.URL.revokeObjectURL(url);

        Swal.fire({
          icon: 'success',
          title: 'PDF generado',
          text: 'El PDF se ha descargado correctamente.',
          confirmButtonColor: '#8bb915'
        });

      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Error al generar PDF',
          text: error.message,
          confirmButtonColor: '#e74c3c'
        });
      } finally {
        this.cargando = false;
      }
    }
  }
};
</script>

<style scoped>
.contenedor {
  max-width: 480px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #f9fff9;
  border: 2px solid #8bb915;
  border-radius: 10px;
  box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);
  text-align: center;
  font-family: 'Rubik', sans-serif;
}

h2 {
  color: #444;
  margin-bottom: 1rem;
}

p {
  margin-bottom: 1rem;
  font-size: 15px;
  color: #333;
}

label {
  font-weight: 600;
  color: #555;
}

input[type="date"] {
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin: 1rem 0;
  width: 100%;
  max-width: 240px;
}

.botones {
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
  gap: 0.5rem;
}

button {
  background-color: #8bb915;
  border: none;
  color: white;
  padding: 0.6rem 1.2rem;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #779e12;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button.volver {
  background-color: #e0e0e0;
  color: #333;
}

button.volver:hover {
  background-color: #c9c9c9;
}

.loader {
  height: 60px;
  aspect-ratio: 1;
  position: relative;
  margin: 1rem auto;
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
</style>
