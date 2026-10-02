# Matriz de riesgos técnicos — MercadoTico 360 (MongoDB)

**Responsable:** Integrante 5 (QA & Performance)
**Estado:** borrador inicial (Entregable 1)

**Escala:** Probabilidad e Impacto en Baja / Media / Alta.

| ID | Riesgo | Prob. | Impacto | Mitigación | Responsable |
|---|---|---|---|---|---|
| R1 | Credenciales de MongoDB Atlas expuestas en el repositorio o en su historial de commits | Media | Alta | Usar `.env` (en `.gitignore`) y `.env.example` sin secretos; rotar cualquier contraseña que haya estado en el repo | Todos |
| R2 | El profesor no puede reproducir el entorno si solo funciona con Atlas | Media | Alta | Documentar una alternativa local (MongoDB en Docker) en el README | Integrante 6 |
| R3 | Las líneas de pedido no guardan nombre y precio al momento de la compra, y se pierde la integridad histórica | Media | Alta | Definir `lineas_detalle` con nombre, precio unitario y cantidad; probar con F5 | Integrante 4 |
| R4 | Los índices no cubren las consultas reales (por ejemplo categoría + precio + atributo) | Media | Media | Revisar con `explain()`; evaluar un índice compuesto como `(categoria, atributos.talla, precio)` | Integrantes 4 y 5 |
| R5 | Atributos inconsistentes entre productos de una misma categoría | Media | Media | Aplicar validación de esquema (`$jsonSchema`) por categoría | Integrante 4 |
| R6 | Datos insuficientes: no se alcanza el volumen mínimo (25 000 / 10 000 / 50 000) | Baja | Alta | Verificar conteos tras el seeding; generar con semilla fija | Integrante 3 |
| R7 | Mediciones poco confiables (caché, otros procesos, hardware distinto) | Alta | Media | Calentamiento, 30 repeticiones, mediana y p95, mismo entorno y documentación del hardware | Integrante 5 |
| R8 | Resultados con y sin índice no comparables | Media | Alta | Mismos datos y mismo orden de pruebas; crear el índice solo después de medir sin él | Integrante 5 |
| R9 | Crecimiento sin control del documento de pedido (muchas líneas) | Baja | Media | Limitar líneas por pedido en el generador; documentar el límite de 16 MB de MongoDB | Integrante 3 |
| R10 | Límites del plan gratuito de Atlas (almacenamiento y rendimiento) afectan las pruebas | Media | Media | Ejecutar las pruebas en local y reportar el entorno | Integrante 5 |
| R11 | Falla de la demostración en vivo | Media | Alta | Respaldo local de los datos, capturas y video corto de la ejecución | Todos |
| R12 | Historial del repositorio con pocos aportes por integrante | Media | Alta | Commits pequeños y frecuentes de cada integrante, en fechas distintas | Todos |

## Limitaciones conocidas (para la Sección 7 del paper)

- Los datos son sintéticos y pueden no reflejar patrones reales de compra.
- Las mediciones dependen del hardware y la configuración del entorno de pruebas.
- Los resultados corresponden a una instancia única, no a un clúster distribuido.
- El alcance excluye interfaz de usuario, pasarelas de pago y logística.

## Pendientes

- Confirmar responsables con el grupo.
- Actualizar probabilidad e impacto después de las primeras mediciones.
- Pasar esta matriz al documento de la Propuesta Inicial.
