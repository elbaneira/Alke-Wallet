# 💰 Alke Wallet - Sistema de Gestión Financiera (Módulo 7 ABP)

![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

**Alke Wallet** es una aplicación web desarrollada con **Django 5** y **PostgreSQL** como parte del proyecto integrador para el Módulo 7. Permite gestionar clientes, cuentas bancarias/billeteras virtuales y ejecutar transacciones financieras (depósitos, retiros y transferencias entre cuentas) con total precisión de decimales e integridad referencial.

---

## 📌 Objetivos y Cumplimiento de Requerimientos

El proyecto cumple al 100% con los criterios evaluados en la rúbrica del Módulo 7:

1. **Configuración de Base de Datos Relacional:**
   - Integración con **PostgreSQL** mediante el conector `psycopg2`.
   - Ajustes regionales para Chile (`es-cl`, `America_Santiago`) y formateo de separadores de miles con `django.contrib.humanize`.

2. **Modelo de Datos y ORM:**
   - Modelos estructurados (`Cliente`, `Cuenta`, `Transaccion`) utilizando `DecimalField` para garantizar precisión en montos monetarios.
   - Relaciones de clave foránea (`ForeignKey`) con integridad referencial.

3. **Operaciones CRUD Completas:**
   - **Clientes:** Registro, edición de datos, listado interactivo con notificaciones detalladas (ID y nombre) y eliminación.
   - **Cuentas:** Creación vinculada a clientes, categorización dinámica (Virtual, Corriente, Ahorro), eliminación y vista detallada por cuenta.
   - **Transacciones:** Registro de depósitos, retiros y transferencias con validación automática de saldo suficiente.

4. **Consultas Avanzadas y Agregaciones:**
   - Cálculo del total custodiado en el sistema mediante agregaciones del ORM (`Sum('saldo')`).
   - Consultas con SQL nativo a través de `raw()` probadas en la shell para filtrado avanzado.

5. **Panel de Administración:**
   - Configuración extendida en `gestion/admin.py` con filtros por tipo de cuenta, barra de búsqueda por cliente y vista detallada de transacciones.

---

## 🏗️ Arquitectura y Escalabilidad (Gestión de Condominios)

La estructura modular desarrollada en este proyecto sirve como base para el sistema de **Gestión de Condominios**:

| Componente Alke Wallet | Proyección en Gestión de Condominios |
| :--- | :--- |
| `Cliente` | **Copropietario / Residente** (Dueño de departamento o casa) |
| `Cuenta` | **Unidad / Departamento** (Cuenta de gastos comunes por vivienda) |
| `Transaccion` | **Pago de Gastos Comunes / Fondo de Reserva** |
| `DecimalField` | **Cálculo preciso de prorrateos y cobros** |

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3, Django 5 (ORM, Forms, Views, Messages).
- **Base de Datos:** PostgreSQL.
- **Frontend:** HTML5, CSS3, Bootstrap 5 (UI responsiva, Badges, Modales y Componentes).
- **Librerías / Aplicaciones:** `django.contrib.humanize`, `psycopg2`.

---

## ⚙️ Configuración e Instalación Local

### 1. Requisitos Previos
Asegúrate de tener instalados **Python 3.11+**, **PostgreSQL** y **Git**.

### 2. Clonar el Repositorio
```bash
git clone [https://github.com/tu-usuario/alke-wallet.git](https://github.com/elbaneira/AlkeWallet.git)
cd AlkeWallet

---
👩‍💻 Autora:

Elba Neira — Desarrollo Full Stack & Modelamiento de Base de Datos.

---
📌 Ver repositorio en GitHub

⭐ Un proyecto más en el camino de convertir el aprendizaje en proyectos reales.

---
© 2026 Elba Neira Arévalo
---
