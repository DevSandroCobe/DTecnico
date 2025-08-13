<template>
  <div class="pagina">
    <!-- ENCABEZADO -->
    <header class="encabezado">
      <div class="logo-container">
        <img src="/imagenes/logo.jpg" alt="Logo" class="logo" />
      </div>
      <div class="titulo-container">
        <h1>ÁREA DE DIRECCIÓN TÉCNICA DE MEDICAMENTOS</h1>
        <h2 class="subtitulo">Panel de Reportes y Utilidades</h2>
      </div>
    </header>

    <!-- CUERPO PRINCIPAL -->
    <main class="cuerpo">
      <p class="instrucciones">Seleccione el tipo de acta que desea generar:</p>
      <div class="botonera">
        <button class="boton trasl" @click="irADespachoTrasl">
          <span>🚚</span> Actas de Despacho Traslado
        </button>
        <button class="boton venta" @click="irADespachoVenta">
          <span>🧾</span> Actas de Despacho Venta
        </button>
      </div>
    </main>

    <!-- PIE DE PÁGINA -->
    <footer class="pie">
      <div class="p1">
        <p><strong>👨‍💻 Desarrollado por:</strong><br><br>
          Área de Sistemas y T.I.<br>
          - Sandro Dominguez Albornoz
        </p>
      </div>
      <div class="p2">
        <p><strong>📬Contacto :</strong><br><br>
          soporte.ti@cobefar.com.pe<br>
        <span class="nivel-contacto">↳ coordinador.ti@cobefar.com.pe</span><br>
        <span class="nivel-contacto">↳↳ coordinador.desarrollo@cobefar.com.pe</span><br>
        <span class="nivel-contacto">↳↳↳ soporte.desarrollo@cobefar.com.pe</span>
        </p>
      </div>
      <div class="p3">
        <p><strong>Tecnologías usadas :</strong></p>
        <ul>
          <li><img src="/imagenes/pie/p_1.jpg" alt="Hana SQL" /> Hana SQL</li>
          <li><img src="/imagenes/pie/p_2.jpg" alt="PHP 7" /> PHP 7</li>
          <li><img src="/imagenes/pie/p_3.jpg" alt="HTML5" /> HTML5</li>
          <li><img src="/imagenes/pie/p_4.jpg" alt="CSS3" /> CSS3</li>
        </ul>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function irADespachoTrasl() {
  router.push('/actas-traslados')
}

function irADespachoVenta() {
  router.push('/actas-ventas')
}
</script>

<style scoped>
.pagina {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  /* Fondo con imagen y color de respaldo */
  background: url('/imagenes/fondo_body.jpg') center center/cover no-repeat, linear-gradient(135deg, #f8fafc 0%, #e8f5e9 100%);
  font-family: 'Rubik', Arial, sans-serif;
}

.encabezado {
  display: flex;
  align-items: center;
  gap: 2.2rem;
  background: #388e3c;
  color: #fff;
  padding: 2.2rem 2.5rem 1.5rem 2.5rem;
  border-bottom-left-radius: 32px;
  border-bottom-right-radius: 32px;
  box-shadow: 0 6px 24px rgba(44, 62, 80, 0.10);
  justify-content: center;
  text-align: center;
}
.logo-container {
  background: #fff;
  border-radius: 14px;
  padding: 0.7rem 1.2rem;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.10);
}
.logo {
  width: 100px;
  height: auto;
  display: block;
}
.titulo-container {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  align-items: center;
  justify-content: center;
}
.encabezado h1 {
  font-size: 1.7rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: 1.2px;
  text-align: center;
}
.subtitulo {
  font-size: 1.08rem;
  font-weight: 400;
  color: #c8e6c9;
  margin: 0;
  letter-spacing: 0.5px;
  text-align: center;
}

.cuerpo {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 3.2rem 1rem 1rem 1rem;
}
.instrucciones {
  font-size: 1.13rem;
  color: #333;
  margin-bottom: 2.5rem;
  font-weight: 500;
}
.botonera {
  display: flex;
  gap: 2.5rem;
  margin-bottom: 2.5rem;
}
.boton {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  background: linear-gradient(90deg, #43a047 0%, #8bc34a 100%);
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 1.2rem 2.5rem;
  font-size: 1.18rem;
  font-weight: 700;
  box-shadow: 0 2px 10px rgba(44, 62, 80, 0.10);
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
  letter-spacing: 0.5px;
}
.boton.trasl span {
  font-size: 1.4em;
}
.boton.venta span {
  font-size: 1.3em;
}
.boton:hover {
  background: linear-gradient(90deg, #2e7d32 0%, #689f38 100%);
  transform: translateY(-2px) scale(1.05);
}

.pie {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #f1f8e9;
  padding: 1.7rem 2.5rem;
  border-top-left-radius: 32px;
  border-top-right-radius: 32px;
  box-shadow: 0 -2px 8px rgba(44, 62, 80, 0.04);
  font-size: 1.01rem;
  margin-top: auto;
}
.p1, .p2, .p3 {
  flex: 1;
  margin: 0 1.3rem;
}
.p1 strong, .p2 strong, .p3 strong {
  color: #388e3c;
}
.p3 ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.p3 li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.3rem;
}
.p3 img {
  width: 22px;
  height: 22px;
  border-radius: 4px;
  background: #fff;
  box-shadow: 0 1px 3px rgba(44, 62, 80, 0.08);
}
.nivel-contacto {
  font-size: 0.93em;
  color: #388e3c;
  margin-left: 0.5rem;
}
@media (max-width: 900px) {
  .pie { flex-direction: column; align-items: stretch; }
  .p1, .p2, .p3 { margin: 0.5rem 0; }
  .botonera { flex-direction: column; gap: 1.2rem; }
  .encabezado { flex-direction: column; gap: 1.2rem; text-align: center; }
  .titulo-container { align-items: center; }
}
</style>

