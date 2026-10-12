---
layout: default
title: "FIAT/IFTA 2026: página de la charla"
nav_exclude: true
permalink: /fiat-ifta-2026-companion/es/
fc_lang: es
description: Ejemplos a tamaño completo y notas de la charla de Fabio Bedoya en FIAT/IFTA 2026, Los límites actuales de la IA en la restauración de películas y cómo podrían superarse.
---

{% include fiat-companion/style.html %}
{% assign vb = site.fc_view_base_override | default: site.data.fiat_evidence.view_base %}

<div class="fc" lang="es">

{% include fiat-companion/langswitch.html %}

<header class="fc-hero">
  <p class="fc-kicker">Congreso Mundial de FIAT/IFTA · São Paulo 2026</p>
  <h1 id="the-current-limits-of-ai-in-film-restoration">Los límites actuales de la IA en la restauración de películas y cómo podrían superarse</h1>
  <p class="fc-byline">Fabio Bedoya<span>Director de Restauración, Filmfinity</span></p>
  <p class="fc-panel">Cinemateca Brasileira<span>8 de octubre de 2026</span></p>
  <div class="fc-buttons">
    <a class="fc-btn fc-btn-primary" href="https://github.com/fabiocolor/custom-machine-learning-for-film-restoration">La investigación en GitHub</a>
    <a class="fc-btn" href="#workflows">Flujos de trabajo y guías</a>
  </div>
  <p>Esta página acompaña mi charla. Sigue las diapositivas en orden, así que puedes encontrar la versión a tamaño completo de cada ejemplo a medida que aparece, o volver a ella más tarde. Para cada experimento, anoté qué funcionó y en qué todavía se queda corto.</p>
  <p>Después de la charla, también escribí un resumen de <a href="{{ '/research-status/' | relative_url }}">dónde está la investigación ahora</a> (en inglés): qué funciona, qué todavía no y qué flujos de trabajo puedes reproducir hoy.</p>
</header>

<p class="fc-tip">Toca un video para reproducirlo aquí. El reproductor transmite desde Google Drive, así que puede mostrar una calidad menor que la del original, sobre todo con una conexión lenta. Las partes y la evidencia de cada ejemplo se abren a tamaño completo en un visor, donde puedes hacer zoom para ver el detalle. La mayoría de los videos son comparaciones lado a lado, así que cada mitad es más pequeña que el archivo completo.</p>

<nav class="fc-toc" aria-labelledby="contents">
  <h2 id="contents">Sigue la charla</h2>
  <ol>
    <li><a href="#copycat-to-open-weight"><span class="fc-n">2</span>De CopyCat a los modelos de pesos abiertos</a></li>
    <li><a href="#masking-versus-recovery"><span class="fc-n">3</span>Ocultar frente a recuperar</a></li>
    <li><a href="#the-limits"><span class="fc-n">4</span>Los límites<span class="fc-v">Imágenes</span></a></li>
    <li><a href="#reference-recovery"><span class="fc-n">5–6</span>Recuperación de color a partir de una referencia</a></li>
    <li><a href="#synthetic-reference"><span class="fc-n">7</span>Crear una referencia sintética<span class="fc-v">Imágenes</span></a></li>
    <li><a href="#telestyle"><span class="fc-n">8–9</span>Mantener el color estable a lo largo de un plano<span class="fc-v">Video</span></a></li>
    <li><a href="#h3-controlnet"><span class="fc-n">10–11</span>Hacerlo más rápido</a></li>
    <li><a href="#temporal-cbcr"><span class="fc-n">12–13</span>El adaptador Temporal CbCr<span class="fc-v">Video</span></a></li>
    <li><a href="#diffusion-upscaling"><span class="fc-n">14–15</span>Escalado por difusión</a></li>
    <li><a href="#diffusion-reconstruction"><span class="fc-n">16–17</span>Reconstrucción por difusión</a></li>
    <li><a href="#combining-sources"><span class="fc-n">18–19</span>Combinar fuentes y luego reconstruir</a></li>
    <li><a href="#dialogue-recovery"><span class="fc-n">20</span>Recuperación de diálogos</a></li>
    <li><a href="#inside-existing-tools"><span class="fc-n">21</span>IA dentro de las herramientas que ya usamos<span class="fc-v">Video</span></a></li>
    <li><a href="#limits-now"><span class="fc-n">22</span>Dónde están los límites ahora</a></li>
    <li><a href="#thanks"><span class="fc-n">23</span>Agradecimientos y créditos</a></li>
  </ol>
</nav>

<section class="fc-section" id="copycat-to-open-weight">
  <p class="fc-slide">Diapositiva 2</p>
  <h2 id="copycat-to-open-weight-title">De CopyCat a los modelos de pesos abiertos</h2>
  <p>Mi investigación empezó con CopyCat, dentro de Nuke. La idea es entrenar un modelo pequeño para cada película a partir de fotogramas equivalentes de dos copias: el escaneo dañado y una copia mejor de la misma película que muestra el resultado que queremos. Eso es lo que presenté el año pasado en Roma, y sigue siendo mi punto de partida. Pero necesita esa copia mejor para aprender, y es una plataforma cerrada hecha para efectos visuales.</p>
  <p>Desde entonces, los modelos de pesos abiertos, los que cualquiera puede descargar y ejecutar, se han vuelto lo bastante buenos para imagen, video y voz en una sola estación de trabajo. La gente ya los usa para “restaurar” fotos antiguas y películas caseras, pero casi siempre fuera del archivo. Así que mi pregunta es: ¿cómo los acotamos para que sean útiles para el trabajo que realmente necesitamos?</p>
</section>

<section class="fc-section" id="masking-versus-recovery">
  <p class="fc-slide">Diapositiva 3</p>
  <h2 id="masking-versus-recovery-title">Ocultar frente a recuperar</h2>
  <p>La mayoría de las herramientas de restauración usan filtros espaciales y temporales. Toman imagen prestada del mismo fotograma o de los fotogramas de alrededor, y cuando no hay nada limpio que copiar, interpolan. La diapositiva muestra Dry Clean en Phoenix sobre <em>Point Blank</em> (1967); las marcas rojas son lo que detectó y eliminó.</p>
  <p>Estas herramientas pueden ocultar polvo, rayas y parpadeo, y cubrir dos o tres fotogramas faltantes. Pero no pueden traer de vuelta lo que se perdió. Si somos honestos, la restauración digital siempre ha consistido en ocultar, no en recuperar.</p>
  <p>Así que la IA en restauración no es algo completamente nuevo. Lo que nos da es una forma de abordar problemas que antes no eran posibles ni técnica ni económicamente, trabajando con el escaneo tal como está. En muchos archivos, sobre todo en América Latina y el Sudeste Asiático, ese escaneo desvanecido es lo único que queda de una película.</p>
{% include fiat-companion/evidence.html key="slide03" %}
</section>

<section class="fc-section" id="the-limits">
  <p class="fc-slide">Diapositiva 4</p>
  <h2 id="the-limits-title">Los límites</h2>
  <p>Tal como yo lo veo, hay tres límites principales.</p>
  <ul class="fc-points">
    <li><strong>No fueron hechos para el cine.</strong> Estos modelos se crearon para generar o editar imágenes nacidas digitales. Borran el grano y el detalle fino, o inventan detalle nuevo. La imagen se ve más nítida, pero deja de parecer película.</li>
    <li><strong>Resolución y duración.</strong> En mis pruebas, los modelos de video locales trabajaban a unos 768 × 432 píxeles y solo podían seguir unos diez segundos a la vez. En la diapositiva, Qwen Image Edit se ejecutó dos veces sobre un fotograma de <em>Reptilicus</em> (1961) con el mismo prompt: una vez sobre el fotograma completo (1184 × 880) y otra sobre cuatro mosaicos unidos (2048 × 1556). Mira la torre del salvavidas: los mosaicos conservan más grano y detalle de la película, pero el color varía entre ellos y se notan las uniones. Dividir en mosaicos ayuda, pero trae un problema nuevo que resolver.</li>
    <li><strong>Costo.</strong> La restauración requiere muchas iteraciones, y en la nube cada una cuesta dinero. Por eso trabajo en local, pero eso igual implica equipo, tiempo y electricidad. No hay cómputo gratis, aunque la computadora sea tuya.</li>
  </ul>

  <figure class="fc-media fc-still">
    <button type="button" class="fc-ev fc-ev-img" data-id="v-reptilicus-beach-tiled-vs-fu-f83c" data-kind="image" data-w="1732" data-h="770" data-title="Fotograma de la playa de Reptilicus: cuatro mosaicos unidos a la izquierda y el fotograma completo en una sola pasada a la derecha"><img src="{{ vb }}v-reptilicus-beach-tiled-vs-fu-f83c_preview.jpg" alt="Fotograma de la playa de Reptilicus: cuatro mosaicos unidos a la izquierda y el fotograma completo en una sola pasada a la derecha" loading="lazy" decoding="async"></button>
    <p class="fc-bar">Diapositiva 4 · <em>Reptilicus</em> (1961): cuatro mosaicos unidos (izquierda) y el fotograma completo en una sola pasada (derecha)</p>
    <figcaption class="fc-body">
      <p class="fc-file">Cómo se hizo · abre cada parte a tamaño completo</p>
      <ol class="fc-parts">
        <li><button type="button" class="fc-part fc-ev" data-id="v-01-source-reptilicus-tlr-000-f859" data-kind="image" data-w="2048" data-h="1556" data-title="Fuente desvanecida">Fuente desvanecida<span class="fc-dims">2048 × 1556</span></button><p>El fotograma desvanecido al tamaño completo del escaneo.</p></li>
        <li><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-fullframe-cl-cf78" data-kind="image" data-w="1184" data-h="880" data-title="Fotograma completo en una pasada">Fotograma completo en una pasada<span class="fc-dims">1184 × 880</span></button><p>Qwen Image Edit sobre el fotograma completo, con el prompt Clara de la diapositiva 7. El resultado sale más pequeño que el escaneo.</p></li>
        <li><span class="fc-part-label">Cuatro mosaicos de la fuente<span class="fc-dims">1328 × 800 cada uno</span></span><span class="fc-part-set"><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-top-left-sou-fd20" data-kind="image" data-w="1328" data-h="800" data-title="superior izquierdo">superior izquierdo</button><button type="button" class="fc-part fc-ev" data-id="s04-01" data-kind="image" data-w="1328" data-h="800" data-title="superior derecho">superior derecho</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-bottom-left--3036" data-kind="image" data-w="1328" data-h="800" data-title="inferior izquierdo">inferior izquierdo</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-bottom-right-b547" data-kind="image" data-w="1328" data-h="800" data-title="inferior derecho">inferior derecho</button></span><p>El mismo fotograma cortado en cuatro mosaicos que se superponen.</p></li>
        <li><span class="fc-part-label">Cada mosaico después del modelo<span class="fc-dims">1328 × 800 cada uno</span></span><span class="fc-part-set"><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-tile-top-lef-75eb" data-kind="image" data-w="1328" data-h="800" data-title="superior izquierdo">superior izquierdo</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-tile-top-rig-e731" data-kind="image" data-w="1328" data-h="800" data-title="superior derecho">superior derecho</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-tile-bottom--4bd3" data-kind="image" data-w="1328" data-h="800" data-title="inferior izquierdo">inferior izquierdo</button><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-tile-bottom--f8c1" data-kind="image" data-w="1328" data-h="800" data-title="inferior derecho">inferior derecho</button></span><p>Cada mosaico pasó por el modelo por separado, con el mismo prompt.</p></li>
        <li><button type="button" class="fc-part fc-ev" data-id="v-reptilicus-t001-four-tile-ra-2024" data-kind="image" data-w="2048" data-h="1556" data-title="Cuatro mosaicos unidos">Cuatro mosaicos unidos<span class="fc-dims">2048 × 1556</span></button><p>Los cuatro resultados pegados de nuevo en un solo fotograma, al tamaño del escaneo, sin fundido, así que las uniones siguen a la vista.</p></li>
      </ol>
    </figcaption>
  </figure>
{% include fiat-companion/evidence.html key="slide04" %}
</section>

<section class="fc-section" id="reference-recovery">
  <p class="fc-slide">Diapositivas 5–6</p>
  <h2 id="reference-recovery-title">Recuperación de color a partir de una referencia</h2>
  <p>Empecemos por lo que ya funciona. Un modelo pequeño se entrena con pares de fotogramas equivalentes: la fuente desvanecida y una referencia que todavía conserva el color. Esa referencia puede ser un telecine, un DVD, otra copia o el negativo original, donde los dos coincidan.</p>
  <p>El modelo solo aprende el color. Su salida se combina con la luma, el brillo, del escaneo original, así que la resolución, el grano y el detalle se mantienen como estaban. El flujo de trabajo está <a href="{{ '/chroma-recovery/' | relative_url }}">documentado aquí</a>.</p>
  <div class="fc-missing"><p>Los ejemplos de las diapositivas 5 y 6 no se muestran en esta página.</p></div>

</section>

<section class="fc-section" id="synthetic-reference">
  <p class="fc-slide">Diapositiva 7</p>
  <h2 id="synthetic-reference-title">Crear una referencia sintética</h2>
  <p>¿Y qué pasa cuando no hay referencia? Creas una: un fotograma de color aprobado para cada plano. Lo llamo referencia sintética, y la hago con Qwen Image Edit, un modelo de imagen de pesos abiertos de Alibaba.</p>
  <p>Mi primer intento fue guiarlo con una leader lady, la mujer de los fotogramas de calibración al comienzo de un rollo. No funcionó. Estos modelos no entienden el significado como nosotros, así que en vez de tomar solo el color, el modelo mezcló las dos imágenes y la mujer terminó dentro del plano. A eso lo llamo contaminación semántica.</p>
  <p>Una carta de color simple funcionó mejor, una vez que la desenfoqué un poco. Guía el color sin darle al modelo nada más que copiar.</p>

  <p>Luego vino el prompt, que es la forma de hablarle al modelo. Hice un pequeño concurso, al que llamé America's Next Top Machine Learning Model: decenas de prompts y cientos de fotogramas de prueba, en siete rondas sobre siete películas desvanecidas. Un prompt solo pasaba una ronda si ocho de cada diez fotogramas eran aceptables. El ganador, Clara, es el que más uso, pero también uso los otros, según el plano.</p>
  <p>De la referencia sintética me quedo solo con el color. El brillo sigue viniendo del escaneo.</p>



  <div class="fc-missing"><p>Los fotogramas de prueba de la diapositiva 7 no se muestran en esta página. La carta de colores está en la evidencia de abajo.</p></div>
{% include fiat-companion/evidence.html key="slide07" %}
</section>

<section class="fc-section" id="telestyle">
  <p class="fc-slide">Diapositivas 8–9</p>
  <h2 id="telestyle-section-title">Mantener el color estable a lo largo de un plano</h2>
  <p>Conseguir un fotograma convincente ya no es lo difícil. Si simplemente ejecutas el modelo 24 veces por segundo, no funciona, porque estos modelos no son deterministas: cada ejecución es un poco una ruleta. Cada fotograma recibe una interpretación ligeramente distinta, y el color parpadea.</p>
  <p>La diapositiva 8 muestra una escena de baile de <em>Obsession</em> en la que cada fotograma se recuperó por separado. Mira el vestido de la mujer de la derecha, y el fondo. Cada fotograma es una interpretación razonable por sí solo, pero juntos no coinciden. Un buen fotograma es una miniatura. Una restauración necesita que todo el plano sea coherente consigo mismo. Eso es la consistencia temporal, y fue el mayor obstáculo.</p>

{% include fiat-companion/evidence.html key="slide08" %}

  <figure class="fc-media">
      <div class="fc-missing"><p>El clip de la charla no se muestra en esta página. Lo que sigue viene de los registros de la investigación.</p></div>
    <figcaption class="fc-body">
      <p>TeleStyle, de TeleAI, es un LoRA: un pequeño complemento para Qwen Image Edit, hecho para copiar el estilo de una imagen en otra. Tomo una referencia aprobada y copio su color en cada fotograma del plano.</p>
      <div class="fc-verdict">
        <div><strong>Lo que funcionó</strong><p>El color se mantiene a lo largo de todo el plano.</p></div>
        <div><strong>Limitaciones</strong><p>Ejecuta el modelo en cada fotograma, con una sola semilla fija para todo el plano. Este plano de 11 segundos tomó casi cuatro horas. Está bien como prueba, pero no es algo que puedas usar en un largometraje.</p></div>
      </div>
      <p class="fc-file">Cómo se hizo, según los registros de la investigación</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">TeleStyle en cada fotograma</span><p>Cada fotograma pasó por separado por Qwen Image Edit con el LoRA TeleStyle, con el fotograma desvanecido y la referencia aprobada como sus dos entradas, en 4 pasos. Se generaron los 338 fotogramas.</p></li>
        <li><span class="fc-part-label">Solo el color</span><p>El color de TeleStyle, generado a 1184 × 880, se puso sobre el brillo intacto del escaneo a 1920 × 1440.</p></li>
        <li><span class="fc-part-label">Tiempo</span><p>La ejecución completa tomó unos 13.560 segundos, casi cuatro horas: unos 32 segundos por fotograma una vez que la máquina estaba caliente.</p></li>
        <li><span class="fc-part-label">Comparación</span><p>Después de la aprobación, los tres paneles se pusieron lado a lado: escaneo original, referencia aprobada y recuperación de croma, a 30 fotogramas por segundo.</p></li>
      </ol>
    </figcaption>
  </figure>
</section>

<section class="fc-section" id="h3-controlnet">
  <p class="fc-slide">Diapositivas 10–11</p>
  <h2 id="h3-controlnet-section-title">Hacerlo más rápido: H3 y ControlNet</h2>
  <p>Tenía un color que se mantenía, pero tomaba demasiado tiempo. A finales de julio, MiniMax lanzó H3, un modelo de video muy bueno con imágenes de referencia. En una sola pasada, lleva el color aprobado a lo largo de toda una sección de un plano.</p>
  <p>Pero por sí solo, H3 se aleja de la imagen y pierde la geometría. Así que tuve que ejecutarlo en secciones cortas y hacer que todas coincidieran, lo que significaba más procesamiento y más tiempo. Luego, en agosto, Alibaba PAI lanzó un ControlNet para H3. Un ControlNet es una forma de dirigir lo que hace el modelo; este le pasa los bordes de cada fotograma, lo que ayuda a conservar la geometría y el movimiento propios de la película.</p>
  <p>Me quedo solo con el color y lo pongo sobre el brillo original, así que el grano, la aspereza, incluso la suciedad, se mantienen. Si los dejas solos, estos modelos quieren cambiarlo todo y darle un aspecto plástico.</p>

  <figure class="fc-media">
      <div class="fc-missing"><p>El clip de la charla no se muestra en esta página. Lo que sigue viene de los registros de la investigación.</p></div>
    <figcaption class="fc-body">
      <p>El color viene de H3 con el ControlNet, y se termina con el adaptador Temporal CbCr, que explico en la siguiente sección. Elegí este plano porque es difícil: mucho movimiento, una multitud que cambia todo el tiempo y un paneo rápido en el medio.</p>
      <div class="fc-verdict">
        <div><strong>Lo que funcionó</strong><p>El color se mantiene a pesar de todo ese movimiento, y la geometría sigue igual que en el original.</p></div>
        <div><strong>Limitaciones</strong><p>Si miras de cerca, hay algo de tinte en las sombras. Mi copia era de 30 fotogramas por segundo con una cadencia rota, así que sacar fotogramas limpios de ella fue difícil, y el adaptador necesita fotogramas bien alineados. Todavía estoy trabajando en esto.</p></div>
      </div>
      <p class="fc-file">Cómo se hizo, según los registros de la investigación</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">Fuente y cadencia</span><p>385 fotogramas a 1920 × 1440 y 30 fotogramas por segundo. 77 eran casi duplicados por la cadencia rota, así que los 308 fotogramas distintos se mapearon a 24 fotogramas por segundo, fotograma por fotograma.</p></li>
        <li><span class="fc-part-label">Paletas aprobadas</span><p>Dos referencias de color aprobadas: la paleta principal de exteriores y otra para un primer plano en interior.</p></li>
        <li><span class="fc-part-label">Bordes</span><p>Un mapa de bordes (Canny) de cada fotograma, hecho a partir de la fuente después de un filtro de mediana leve y un ajuste de contraste local.</p></li>
        <li><span class="fc-part-label">H3 con el ControlNet</span><p>H3 se ejecutó con el ControlNet en secciones de 124 fotogramas, a 768 × 576 y 24 fotogramas por segundo.</p></li>
        <li><span class="fc-part-label">Maestros</span><p>Cada fotograma de H3 se registró con la fuente y solo se conservó si el brillo coincidía, con un máximo de 1,5 píxeles de diferencia en general. Después de una auditoría de contaminación, 278 fotogramas se aceptaron como maestros.</p></li>
        <li><span class="fc-part-label">Adaptador</span><p>El adaptador Temporal CbCr aprendió de los maestros. La mejor época se eligió con fotogramas reservados para validación, y luego el adaptador se ajustó de nuevo con todos.</p></li>
        <li><span class="fc-part-label">Final</span><p>El color se generó otra vez a 640 × 480, se escaló con guía y se puso sobre el brillo original a 1920 × 1440, en los 385 fotogramas. Aprobado el 30 de septiembre. El tinte que queda está en los pliegues en sombra de una chaqueta amarilla, en los primeros fotogramas.</p></li>
      </ol>
      <p class="fc-more fc-steps-note">Las imágenes de estos pasos están en carpetas de investigación privadas y todavía no están en esta página.</p>
    </figcaption>
  </figure>
</section>

<section class="fc-section" id="temporal-cbcr">
  <p class="fc-slide">Diapositivas 12–13</p>
  <h2 id="temporal-cbcr-section-title">El adaptador Temporal CbCr</h2>
  <p>Esta es la idea detrás de mi trabajo con CopyCat, llevada fuera de Nuke para que la investigación pueda funcionar en una plataforma abierta. CbCr son los dos canales de color de una imagen de video, separados de su brillo.</p>
  <p>Ejecuto H3 o TeleStyle una o dos veces, según la duración del plano, y me quedo solo con los fotogramas que pasan la revisión. Los llamo maestros. No tienen que cubrir todo el plano, siempre que su geometría coincida con la imagen.</p>
  <p>Un modelo pequeño, con menos de un millón de parámetros, aprende el color del plano a partir de los maestros en minutos. Luego completa los fotogramas que no tienen maestro y mantiene el color estable en todo el plano. En la diapositiva 12, el primer y el tercer fotograma no tienen maestro, y el segundo y el cuarto sí.</p>

  <figure class="fc-media">
{% include fiat-companion/video.html key="slide13" title="Unman, Wittering and Zigo: adaptador Temporal CbCr" label="Reproducir video: Unman, Wittering and Zigo, adaptador Temporal CbCr (7 segundos)" %}
    <p class="fc-bar">Diapositiva 13 · <em>Unman, Wittering and Zigo</em> (1971): adaptador Temporal CbCr</p>
    <figcaption class="fc-body">
      <p>Una escena de coro, con la fuente desvanecida a la izquierda y el resultado del adaptador a la derecha. En este plano, H3 no se alineó con la imagen, así que todos los maestros salieron de TeleStyle. Cubrieron 101 de los 164 fotogramas, y el adaptador completó el resto. El entrenamiento en sí tomó alrededor de un minuto y medio (88,5 segundos).</p>
      <div class="fc-verdict">
        <div><strong>Lo que funcionó</strong><p>Conserva todo lo del original: la suciedad, la aspereza de la película. Incluso el vitral detrás del coro se mantiene consistente durante todo el paneo.</p></div>
        <div><strong>Limitaciones</strong><p>El adaptador es tan bueno como sus maestros, y necesita fotogramas que coincidan bien. El color sigue siendo una interpretación, a menos que lo respalde una referencia que haya sobrevivido.</p></div>
      </div>
{% include fiat-companion/files.html key="slide13" desc="comparación 1920 × 850 · 7 s · 24 fps" %}
      <p class="fc-file">Cómo se hizo, según los registros de la investigación</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">Fuente</span><p>164 fotogramas del tráiler, 2048 × 1556, a 24 fotogramas por segundo.</p></li>
        <li><span class="fc-part-label">H3, probado primero</span><p>H3 se ejecutó primero en dos secciones que se superponen. Ninguno de sus fotogramas se alineó lo bastante bien con la fuente, así que no se usó ninguno.</p></li>
        <li><span class="fc-part-label">Paleta</span><p>Un fotograma aprobado definió la paleta: un resultado de Qwen Image Edit puesto sobre el brillo de la fuente.</p></li>
        <li><span class="fc-part-label">Maestros</span><p>TeleStyle hizo los maestros, y cada uno se revisó en alineación y paleta. Pasaron 101 fotogramas: 82, en tres tramos, usados para el entrenamiento, y un tramo aparte de 19 reservado para validación. 63 fotogramas quedaron sin maestro.</p></li>
        <li><span class="fc-part-label">Entrenamiento</span><p>El adaptador tiene 931.274 parámetros. 60 épocas tomaron 88,5 segundos de entrenamiento en una RTX 5090. La mejor época fue la 56.</p></li>
        <li><span class="fc-part-label">Resultado</span><p>El adaptador coloreó los 164 fotogramas, y su color se puso sobre el brillo intacto de la fuente.</p></li>
      </ol>
      <p class="fc-more fc-steps-note">Las imágenes de estos pasos están en carpetas de investigación privadas y todavía no están en esta página.</p>
    </figcaption>
  </figure>
{% include fiat-companion/evidence.html key="slide13" %}
</section>

<section class="fc-section" id="diffusion-upscaling">
  <p class="fc-slide">Diapositivas 14–15</p>
  <h2 id="diffusion-upscaling-section-title">Escalado por difusión</h2>
  <p>Hasta aquí, el modelo solo agrega color y el escaneo conserva su propia imagen. Pero a veces el elemento que sobrevive no tiene suficiente información para una restauración tradicional. Nuestras herramientas toman prestado del mismo fotograma o de los fotogramas de alrededor, y cuando todos los fotogramas están dañados, no queda nada que tomar. El escalado por difusión permite que un modelo de video reconstruya la imagen a partir de lo que sobrevive, siguiendo su estructura y su movimiento.</p>
  <p>De <em>El Tinterillo</em> solo sobreviven una copia de 16mm dañada y un telecine más limpio, pero blando, recortado y con la cadencia extraña de los telecines de esa época. Suavicé el 16mm con un filtro de mediana y luego combiné los dos, con el telecine en el centro y el 16mm alrededor. Eso da un contorno aproximado para guiar la geometría, pero el filtro también elimina el detalle fino. Así que, para definir cómo debía verse la imagen, hice otras referencias sintéticas con ChatGPT Images. Luego MiniMax H3, en modo referencia, usa esas referencias, con el clip del telecine para el movimiento, para generar cada sección del plano.</p>

  <figure class="fc-media">
      <div class="fc-missing"><p>El clip de la charla no se muestra en esta página. Lo que sigue viene de los registros de la investigación.</p></div>
    <figcaption class="fc-body">
      <div class="fc-verdict">
        <div><strong>Lo que funcionó</strong><p>La imagen de este escaneo no se puede salvar con herramientas tradicionales. H3 llena esos vacíos y reconstruye la imagen, siguiendo la estructura y el movimiento del original.</p></div>
        <div><strong>Limitaciones</strong><p>El resultado es en parte sintético: el modelo inventa detalle fino que la película ya no tiene, y eso hay que declararlo. El modelo trabajó a 768 × 432. Todavía hay un salto de brillo en el primer fotograma, y las caras y el detalle fino siguen siendo débiles.</p></div>
      </div>
      <p>Algunas personas dirán que esto es una herejía, y en cierta medida lo es. Yo mismo no lo llamaría una restauración de película propiamente dicha. Pero con material como este, no veo otro camino, y quizá tengamos que abrir la mente a lo que puede ser la restauración.</p>
      <p class="fc-file">Cómo se hizo, según los registros de la investigación</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">Fuentes</span><p>El escaneo de 16mm, contra el que se juzga el resultado, y el telecine, usado por su movimiento. El plano tiene 624 fotogramas a 24 fotogramas por segundo.</p></li>
        <li><span class="fc-part-label">Híbrido</span><p>Para cada fotograma clave, el escaneo de 16mm se suavizó con un filtro de mediana y se redujo, para hacer una base suave del cuadro completo. El telecine, registrado y con el tono igualado, entró por dentro con un difuminado de 48 píxeles.</p></li>
        <li><span class="fc-part-label">Referencias sintéticas</span><p>Se generaron siete imágenes con ChatGPT Images, cada una a partir de su propio híbrido. Cada una se revisó por desplazamiento dentro del cuadro, con un límite de 3 píxeles; las aceptadas midieron entre 0,66 y 1,23 píxeles.</p></li>
        <li><span class="fc-part-label">H3 por secciones</span><p>H3, en modo de referencia, generó el plano en cuatro secciones a 768 × 432 (fotogramas 1 a 200, 201 a 340, 341 a 400 y 401 a 624), con tres imágenes de referencia cada una y el clip del telecine como entrada de movimiento. 20 pasos, semilla 0.</p></li>
        <li><span class="fc-part-label">Una sección rehecha</span><p>La segunda sección se hizo de nuevo con referencias calibradas, porque la primera versión iba atrasada respecto al movimiento.</p></li>
        <li><span class="fc-part-label">Unión de las secciones</span><p>Un puente de tono y un fundido de 12 fotogramas unieron las secciones. El salto de brillo en el primer fotograma se dejó como estaba.</p></li>
      </ol>
      <p class="fc-more fc-steps-note">Las imágenes de estos pasos están en carpetas de investigación privadas y todavía no están en esta página.</p>
    </figcaption>
  </figure>
</section>

<section class="fc-section" id="diffusion-reconstruction">
  <p class="fc-slide">Diapositivas 16–17</p>
  <h2 id="diffusion-reconstruction-title">Reconstrucción por difusión</h2>
  <p>A veces la imagen no está dañada, sino que ya no existe: faltan fotogramas en el único elemento que sobrevive. Esto pasa mucho con el nitrato, cuando se cortó una sección en descomposición para que no dañara el resto del rollo.</p>
  <p>Herramientas como Phoenix, DIAMANT o DaVinci Resolve pueden cubrir dos o tres fotogramas faltantes con flujo óptico. En un hueco más largo, el movimiento empieza a sentirse raro, porque solo pueden interpolar lo que sobrevive.</p>
  <p>En la charla, el ejemplo es un hueco de 15 fotogramas en un negativo de cámara en el que el sonido sí sobrevive, así que hay que llenar el hueco para mantener juntos imagen y sonido. Hice el seguimiento de los actores desde el último fotograma antes del hueco hasta el primero después de él, y llevé ese movimiento a través de los fotogramas faltantes: esos son los esqueletos de la diapositiva 16. Luego el modelo de video VACE de Alibaba generó la imagen, guiado por ese movimiento, solo dentro del hueco.</p>
  <div class="fc-limits"><p><strong>Lo que funcionó, y las limitaciones.</strong> Los fotogramas generados se sostienen bien, y todos los fotogramas originales quedan intactos. El límite de resolución de la diapositiva 4 sigue vigente, y lo que se genera hay que declararlo.</p></div>
  <div class="fc-missing" style="margin-top: 1rem"><p>El clip que se muestra en la diapositiva 17 no está incluido en esta página.</p></div>
</section>

<section class="fc-section" id="combining-sources">
  <p class="fc-slide">Diapositivas 18–19</p>
  <h2 id="combining-sources-section-title">Combinar fuentes y luego reconstruir</h2>
  <p>Cuando sobreviven varios elementos, cada uno suele estar dañado en lugares distintos. En la charla lo mostré con una película muda que sobrevive como una copia en nitrato y una copia de seguridad en diacetato. Juntas cubren la mayor parte de la película, pero en algunos lugares el nitrato se ha descompuesto y a la copia de seguridad también le faltan esos fotogramas.</p>
  <p>Primero, junto los dos elementos. Tenían color, deformación y encuadre distintos, así que cada fotograma de uno se empareja con el otro por sus rasgos y se deforma hasta encajar. Luego, una sola corrección de tono, ajustada sobre los fotogramas equivalentes más limpios, les da a ambos el mismo aspecto.</p>
  <p>Después, cada fotograma sale del elemento que haya sobrevivido sin daño. Una línea de tiempo del plano funciona como un mapa de esto: de qué elemento sale cada fotograma y dónde no sobrevive ninguno. En esos fotogramas enmascaro solo las zonas dañadas, y Wan VACE 14B, el modelo de video de Alibaba, reconstruye solo esas zonas. La imagen que sobrevive sigue siendo original, porque no queremos reemplazar un fotograma entero solo porque una parte esté dañada.</p>
  <div class="fc-limits"><p><strong>Qué funcionó y los límites.</strong> El resultado se sostiene bien, y todo lo que sobrevive queda intacto. Fue una prueba de trabajo a resolución reducida, no una restauración nativa en HD.</p></div>
  <div class="fc-missing" style="margin-top: 1rem"><p>El ejemplo de la charla no se muestra en esta página.</p></div>
</section>

<section class="fc-section" id="dialogue-recovery">
  <p class="fc-slide">Diapositiva 20</p>
  <h2 id="dialogue-recovery-title">Recuperación de diálogos</h2>
  <p>La misma idea se aplica al sonido: una palabra muy distorsionada se puede reconstruir con la propia voz del actor.</p>
  <p>Usé Fish Audio S2 Pro, un modelo de voz de pesos abiertos, ejecutado en local. Se le dan unos segundos de diálogo limpio del mismo actor en la película, unos diez segundos en este caso, y las palabras exactas. Genera muchas tomas de la frase completa. El reconocimiento de voz y la comparación de voces ayudan a ordenarlas, pero lo que decide es la escucha. Luego solo se reemplaza la parte dañada, aquí alrededor de un tercio de segundo. Todo lo demás es la banda sonora original.</p>
  <div class="fc-limits"><p><strong>Limitaciones.</strong> La salida del modelo era tan limpia que no se integraba, así que agregué algo del ruido de fondo de la propia película. Un buen oído quizá todavía lo note en la palabra reparada.</p></div>
  <div class="fc-missing" style="margin-top: 1rem"><p>El ejemplo de audio de la charla no está incluido en esta página.</p></div>
</section>

<section class="fc-section" id="inside-existing-tools">
  <p class="fc-slide">Diapositiva 21</p>
  <h2 id="inside-existing-tools-section-title">IA dentro de las herramientas que ya usamos</h2>
  <p>La IA también puede trabajar a través de las herramientas que ya usamos. Las empresas que las fabrican la están incorporando, tanto para control y gestión como para procesamiento. DaVinci Resolve 21.1 permite que asistentes de IA lo operen directamente, Premiere Pro tiene un AI Assistant que trabaja dentro del proyecto, y Avid ha mostrado IA agéntica para Media Composer. Las herramientas de restauración pueden funcionar de la misma manera.</p>

  <figure class="fc-media">
{% include fiat-companion/video.html key="slide21" title="Point Blank: un modelo trabajando dentro de Phoenix" label="Reproducir video: Point Blank, un modelo trabajando dentro de Phoenix (30 segundos)" %}
    <p class="fc-bar">Diapositiva 21 · <em>Point Blank</em> (1967): un modelo trabajando dentro de Phoenix</p>
    <figcaption class="fc-body">
      <p>Una de mis pruebas de investigación. Después de ejecutar Dry Clean en Phoenix, un modelo pinta las máscaras de protección directamente en el proyecto. El rojo muestra lo que cambió Dry Clean.</p>
      <div class="fc-limits"><p><strong>Limitaciones.</strong> Todavía está en una etapa temprana. Esta es una grabación de pantalla del flujo de trabajo, no una restauración terminada.</p></div>
{% include fiat-companion/files.html key="slide21" desc="grabación de pantalla 1920 × 1080 · 30 s · 24 fps · sin sonido" %}
      <p class="fc-file">Cómo se hizo, según los registros de la investigación</p>
      <ol class="fc-parts fc-steps">
        <li><span class="fc-part-label">Fuente</span><p>Una copia de estudio del proyecto del tráiler de Point Blank en Phoenix: un plano de 52 fotogramas, 2048 × 1556, a 24 fotogramas por segundo.</p></li>
        <li><span class="fc-part-label">Dos exportaciones</span><p>El plano se exportó dos veces desde Phoenix: una sin Dry Clean y otra con él.</p></li>
        <li><span class="fc-part-label">Lo que cambió Dry Clean</span><p>La diferencia entre las dos exportaciones muestra lo que cambió Dry Clean. Los cambios mayores de 8 valores de código se agruparon en marcas separadas.</p></li>
        <li><span class="fc-part-label">El modelo</span><p>Un pequeño clasificador de imágenes (ResNet18), entrenado con pinceladas de otra película, miró cada marca con los fotogramas anterior y siguiente y predijo si debía devolver ahí la imagen original.</p></li>
        <li><span class="fc-part-label">En el proyecto</span><p>Sus decisiones se convirtieron en pinceladas de Matte Paint: 630 a lo largo de los 52 fotogramas, escritas en el proyecto de Phoenix y leídas de nuevo para comprobarlas.</p></li>
        <li><span class="fc-part-label">Revisión</span><p>La grabación es Phoenix reproduciendo el resultado con Red Difference activado. En la revisión, también devolvió zonas de la pared donde no se perdió información importante, así que todavía no se aceptó.</p></li>
      </ol>
      <p class="fc-more fc-steps-note">Las imágenes de estos pasos están en carpetas de investigación privadas y todavía no están en esta página.</p>
    </figcaption>
  </figure>
{% include fiat-companion/evidence.html key="slide21" %}
</section>

<section class="fc-section" id="limits-now">
  <p class="fc-slide">Diapositiva 22</p>
  <h2 id="limits-now-title">Dónde están los límites ahora</h2>
  <ul class="fc-points">
    <li>Lo que mejor ha funcionado es conservar la propia imagen de la película y dejar que el modelo agregue solo lo que falta: el color, un hueco, una palabra.</li>
    <li>El color se mantiene a lo largo de un plano cuando referencias aprobadas guían todo el plano, ya sea a través de un modelo de video o del pequeño adaptador.</li>
    <li>Lo que más ayuda es el control. Los bordes, el movimiento con seguimiento y el registro mantienen al modelo pegado a la película, no a su propia idea de ella.</li>
    <li>En el flujo de trabajo de color, un modelo pequeño aprende de fotogramas maestros aprobados y completa el plano, así que el modelo grande no tiene que ejecutarse en cada fotograma.</li>
    <li>Lo que todavía tiene que mejorar es la resolución y la duración. Los modelos siguen viendo una imagen reducida, de unos diez segundos a la vez.</li>
    <li>Nada de esto se hace con un clic. Requiere paciencia, y un restaurador que decida qué es aceptable y que diga qué se generó.</li>
  </ul>
  <p>Hace un año, incluso hace un par de meses, nada de esto era posible.</p>
</section>

<section class="fc-section" id="workflows">
  <h2 id="workflows-title">Flujos de trabajo y guías</h2>
  <ul class="fc-points">
    <li><a href="{{ '/chroma-recovery/' | relative_url }}">Recuperación de color entrenada con referencia</a>: aprender de fotogramas equivalentes de la fuente y la referencia, y luego combinar el color predicho con el brillo del escaneo.</li>
    <li><a href="{{ '/open-weight-color-recovery/' | relative_url }}">Recuperación de color con modelos de pesos abiertos</a>: crear y revisar propuestas de color mientras el escaneo sigue siendo la autoridad.</li>
    <li><a href="{{ '/training-inference-review/' | relative_url }}">Entrenamiento, inferencia y revisión</a>: preparar el material, iterar y decidir cuándo un resultado es aceptable.</li>
    <li><a href="{{ '/open-weight-color-recovery/research-routes/' | relative_url }}">Líneas de investigación y preguntas abiertas</a>: una instantánea anterior de la investigación, con su evidencia y sus límites.</li>
    <li><a href="{{ '/research-status/' | relative_url }}">Dónde está la investigación (octubre de 2026)</a> (en inglés): qué funciona, qué todavía no y qué puedes reproducir. La plantilla de Nuke se ejecuta localmente en Nuke Non-Commercial o Indie con tu propio material, y los flujos de Qwen Image Edit se ejecutan en ComfyUI. Los dos todavía necesitan algo de trabajo para que sean fáciles de usar.</li>
    <li><a href="{{ '/' | relative_url }}">Toda la investigación de este sitio</a>, o el <a href="https://github.com/fabiocolor/custom-machine-learning-for-film-restoration">repositorio en GitHub</a>.</li>
  </ul>
</section>

<section class="fc-thanks" id="thanks">
  <p class="fc-slide fc-slide-light">Diapositiva 23</p>
  <h2 id="thanks-title">Gracias</h2>
  <p>Gracias a FIAT/IFTA y a los organizadores.</p>
  <p class="fc-small">Los ejemplos de esta página son pruebas de investigación con tráileres desvanecidos de un escaneo de un rollo de tráileres en 35mm publicado abiertamente en <a href="https://archive.org/details/film-bar-70-trailers-reel-1440x-1080-24fps">archive.org</a>. Los fragmentos de películas siguen siendo propiedad de sus titulares de derechos, y mostrarlos aquí no otorga permiso para reutilizarlos. Consulta los <a href="{{ '/credits/' | relative_url }}">créditos y la atribución</a>.</p>
  <p>Las preguntas y sugerencias son bienvenidas:</p>
  <ul>
    <li>Email: <a href="mailto:info@fabiocolor.com">info@fabiocolor.com</a></li>
    <li>LinkedIn: <a href="https://www.linkedin.com/in/fabiobedoya/">/fabiobedoya</a> · Instagram: <a href="https://www.instagram.com/fabiocolor/">@fabiocolor</a></li>
    <li>YouTube: <a href="https://www.youtube.com/@fabiocolor">@fabiocolor</a> · GitHub: <a href="https://github.com/fabiocolor">/fabiocolor</a></li>
  </ul>
</section>

</div>

{% include fiat-companion/script.html %}
