// @ts-check
const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost';

// ─────────────────────────────────────────
// PRUEBAS DE LOGIN
// ─────────────────────────────────────────

test.describe('Login', () => {

  test('Carga la pagina de login correctamente', async ({ page }) => {
    await page.goto(`${BASE_URL}/pages/index.html`);
    await expect(page).toHaveTitle(/StreamHub/);
    await expect(page.locator('#loginForm')).toBeVisible();
    await expect(page.locator('#email')).toBeVisible();
    await expect(page.locator('#password')).toBeVisible();
    await expect(page.locator('#loginBtn')).toBeVisible();
  });

  test('Login exitoso con credenciales correctas', async ({ page }) => {
    await page.goto(`${BASE_URL}/pages/index.html`);
    await page.fill('#email', 'admin@cineapp.com');
    await page.fill('#password', 'admin123');
    await page.click('#loginBtn');
    await page.waitForURL(/home\.html/, { timeout: 5000 });
    expect(page.url()).toContain('home.html');
  });

  test('Login fallido con credenciales incorrectas', async ({ page }) => {
    await page.goto(`${BASE_URL}/pages/index.html`);
    await page.fill('#email', 'admin@cineapp.com');
    await page.fill('#password', 'contrasena_incorrecta');
    await page.click('#loginBtn');
    await page.waitForTimeout(2000);
    expect(page.url()).not.toContain('home.html');
  });

  test('No permite enviar formulario con campos vacios', async ({ page }) => {
    await page.goto(`${BASE_URL}/pages/index.html`);
    await page.click('#loginBtn');
    await page.waitForTimeout(1000);
    expect(page.url()).not.toContain('home.html');
  });

  test('Link a registro visible y funcional', async ({ page }) => {
    await page.goto(`${BASE_URL}/pages/index.html`);
    await page.click('a[href="registro.html"]');
    await expect(page).toHaveURL(/registro\.html/);
  });

});

// ─────────────────────────────────────────
// PRUEBAS DE CATALOGO
// ─────────────────────────────────────────

test.describe('Catalogo', () => {

  test.beforeEach(async ({ page }) => {
    // Login antes de cada prueba de catalogo
    await page.goto(`${BASE_URL}/pages/index.html`);
    await page.fill('#email', 'admin@cineapp.com');
    await page.fill('#password', 'admin123');
    await page.click('#loginBtn');
    await page.waitForURL(/home\.html/, { timeout: 5000 });
  });

  test('Pagina de home carga despues del login', async ({ page }) => {
    await expect(page).toHaveURL(/home\.html/);
  });

  test('El catalogo muestra contenido', async ({ page }) => {
    await page.waitForTimeout(2000);
    const tarjetas = page.locator('.movie-card, .content-card, [class*="card"]');
    const cantidad = await tarjetas.count();
    expect(cantidad).toBeGreaterThan(0);
  });

  test('Navegacion al catalogo desde home', async ({ page }) => {
    const linkCatalogo = page.locator('a[href*="catalogo"], a[href*="catalog"]');
    const existe = await linkCatalogo.count();
    if (existe > 0) {
      await linkCatalogo.first().click();
      await page.waitForTimeout(1000);
      expect(page.url()).toContain('catalogo');
    } else {
      await page.goto(`${BASE_URL}/pages/catalogo.html`);
      await expect(page).toHaveURL(/catalogo\.html/);
    }
  });

});

// ─────────────────────────────────────────
// PRUEBAS DE REGISTRO
// ─────────────────────────────────────────

test.describe('Registro', () => {

  test('Pagina de registro carga correctamente', async ({ page }) => {
    await page.goto(`${BASE_URL}/pages/registro.html`);
    await expect(page.locator('form')).toBeVisible();
  });

  test('Link de volver al login funciona', async ({ page }) => {
    await page.goto(`${BASE_URL}/pages/registro.html`);
    const linkLogin = page.locator('a[href*="index"], a[href*="login"]');
    const existe = await linkLogin.count();
    if (existe > 0) {
      await linkLogin.first().click();
      await page.waitForTimeout(1000);
      expect(page.url()).toMatch(/index\.html|login\.html/);
    }
  });

});

// ─────────────────────────────────────────
// PRUEBAS DE CONECTIVIDAD
// ─────────────────────────────────────────

test.describe('Conectividad', () => {

  test('Frontend responde en puerto 80', async ({ page }) => {
    const res = await page.goto(BASE_URL);
    expect(res.status()).toBe(200);
  });

  test('Backend responde en puerto 5000', async ({ request }) => {
    const res = await request.get('http://localhost:5000/');
    expect(res.status()).toBe(200);
    const data = await res.json();
    expect(data).toHaveProperty('mensaje');
  });

  test('Swagger disponible en /apidocs/', async ({ request }) => {
    const res = await request.get('http://localhost:5000/apidocs/');
    expect(res.status()).toBe(200);
  });

  test('Regiones disponibles desde la BD', async ({ request }) => {
    const res = await request.get('http://localhost:5000/regiones');
    expect(res.status()).toBe(200);
    const data = await res.json();
    expect(Array.isArray(data)).toBe(true);
    expect(data.length).toBeGreaterThan(0);
  });

});