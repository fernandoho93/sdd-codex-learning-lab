import { expect, test, type APIRequestContext } from '@playwright/test';
import { GamesPage } from './pages/games.page.js';

async function clearCollection(request: APIRequestContext): Promise<void> {
  const response = await request.get('/api/games');
  if (!response.ok()) return;
  const payload = await response.json() as { items: Array<{ id: string }> };
  for (const game of payload.items) await request.delete(`/api/games/${game.id}`);
}

test.beforeEach(async ({ request }) => {
  await clearCollection(request);
});

test('exibe o estado vazio da coleção', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open();
  await expect(page.getByText('Nenhum jogo cadastrado. Cadastre seu primeiro jogo.')).toBeVisible();
});

test('cadastra e lista um jogo com sucesso', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open();
  await games.createGame({ name: 'Astro Bot', genre: 'Plataforma', rating: '9.5' });
  await expect(games.message).toContainText('foi cadastrado');
  await expect(games.card('Astro Bot')).toContainText('Nota 9.5');
});

test('impede cadastro sem campos obrigatórios', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.openCreate(); await games.save();
  await expect(page.getByText('Revise os campos obrigatórios')).toBeVisible();
  await expect(page.getByText('Nenhum jogo cadastrado')).toBeVisible();
});

test('impede nome duplicado sem considerar maiúsculas', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.createGame({ name: 'Astro Bot' });
  await games.openCreate(); await games.fillGame({ name: 'astro bot' }); await games.save();
  await expect(page.locator('#form-summary')).toHaveText('Já existe um jogo com esse nome.');
  await page.getByRole('button', { name: 'Fechar formulário' }).click();
  await expect(page.locator('.game-card')).toHaveCount(1);
});

test('lista todos os jogos cadastrados', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open();
  await games.createGame({ name: 'Returnal' });
  await games.createGame({ name: 'Demon Souls', genre: 'RPG' });
  await expect(page.locator('.game-card')).toHaveCount(2);
});

test('pesquisa pelo nome', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.createGame({ name: 'Returnal' }); await games.createGame({ name: 'Astro Bot' });
  await games.search.fill('astro');
  await expect(games.card('Astro Bot')).toBeVisible();
  await expect(games.card('Returnal')).toBeHidden();
});

test('filtra por gênero', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.createGame({ name: 'Returnal', genre: 'Ação' }); await games.createGame({ name: 'Baldurs Gate 3', genre: 'RPG' });
  await games.genreFilter.selectOption('RPG');
  await expect(games.card('Baldurs Gate 3')).toBeVisible();
  await expect(games.card('Returnal')).toBeHidden();
});

test('filtra por status', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.createGame({ name: 'Returnal', status: 'playing' }); await games.createGame({ name: 'Astro Bot', status: 'completed' });
  await games.statusFilter.selectOption('completed');
  await expect(games.card('Astro Bot')).toBeVisible();
  await expect(games.card('Returnal')).toBeHidden();
});

test('edita status e nota', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.createGame({ name: 'Returnal' }); await games.edit('Returnal');
  await page.locator('#game-status').selectOption('completed');
  await page.locator('#personal-rating').fill('10');
  await games.save();
  await expect(games.card('Returnal')).toContainText('Concluído');
  await expect(games.card('Returnal')).toContainText('Nota 10.0');
});

test('cancela a exclusão', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.createGame({ name: 'Returnal' }); await games.requestDelete('Returnal');
  await page.getByRole('button', { name: 'Cancelar' }).last().click();
  await expect(games.card('Returnal')).toBeVisible();
});

test('exclui após confirmação', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.createGame({ name: 'Returnal' }); await games.requestDelete('Returnal');
  await page.getByRole('button', { name: 'Excluir jogo' }).click();
  await expect(games.card('Returnal')).toHaveCount(0);
  await expect(games.message).toContainText('foi excluído');
});

test('trata erro da API de listagem sem mostrar dados antigos', async ({ page }) => {
  await page.route('**/api/games', (route) => route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ error: { code: 'storage_error', message: 'Banco indisponível.' } }) }));
  const games = new GamesPage(page);
  await games.open();
  await expect(page.locator('#collection-state')).toHaveText('Banco indisponível.');
  await expect(page.locator('.game-card')).toHaveCount(0);
});

test('preenche formulário com resultado RAWG e mantém edição manual', async ({ page }) => {
  await page.route('**/api/catalog/search?**', (route) => route.fulfill({
    status: 200, contentType: 'application/json', body: JSON.stringify({
      items: [{ external_id: '1', name: 'Astro Bot', description: 'Aventura', genre: 'Platformer', developer: 'Team Asobi', publisher: 'Sony', release_date: '2024-09-06', cover_url: 'https://media.rawg.io/astro.jpg', source_name: 'RAWG', source_url: 'https://rawg.io/games/astro-bot' }],
      attribution: { text: 'Dados e imagens fornecidos por RAWG', url: 'https://rawg.io/' },
    }),
  }));
  const games = new GamesPage(page);
  await games.open(); await games.openCreate();
  await page.getByLabel('Pesquisar no catálogo RAWG').fill('Astro');
  await page.getByRole('button', { name: 'Pesquisar', exact: true }).click();
  await page.getByRole('button', { name: 'Usar estes dados' }).click();
  await expect(page.locator('#name')).toHaveValue('Astro Bot');
  await page.locator('#name').fill('Astro Bot Edição Local');
  await expect(page.getByText('Dados e imagens fornecidos por RAWG').first()).toBeVisible();
});

test('mantém cadastro manual quando RAWG não está configurado', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open(); await games.openCreate();
  await page.getByLabel('Pesquisar no catálogo RAWG').fill('Astro');
  await page.getByRole('button', { name: 'Pesquisar', exact: true }).click();
  await expect(page.getByText(/cadastro manual continua disponível/i)).toBeVisible();
  await games.fillGame({ name: 'Cadastro Manual' }); await games.save();
  await expect(games.card('Cadastro Manual')).toBeVisible();
});

test('não cria rolagem horizontal e mantém controles essenciais', async ({ page }) => {
  const games = new GamesPage(page);
  await games.open();
  const overflows = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflows).toBe(false);
  await expect(games.createButton).toBeVisible();
  await games.createButton.focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#name')).toBeFocused();
});
