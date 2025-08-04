<template>
  <div class="pagina">
    <!-- ENCABEZADO -->
    <header class="encabezado">
    <div class="logo-container">
        <img src="/imagenes/logo.jpg" alt="Logo" class="logo" />
    </div>
    <h1>ÁREA DE DIRECCIÓN TÉCNICA DE MEDICAMENTOS</h1>
    </header>


    <!-- CUERPO PRINCIPAL -->
    <main class="cuerpo">
      <p class="instrucciones">Pulse el botón correspondiente al reporte por generar:</p>

      <div class="botonera">
        <button class="boton" @click="irADespachoTrasl">ACTAS DE DESPACHO TRASL</button>
        <button class="boton" @click="irADespachoVenta">ACTAS DE DESPACHO VENTA</button>
        <button class="boton boton-migrar" @click="irAMigracion">MIGRAR BASE DE DATOS</button>
        <strong id="estadoBd"></strong>
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

function irAMigracion() {
  router.push('/migracion')
}
</script>

