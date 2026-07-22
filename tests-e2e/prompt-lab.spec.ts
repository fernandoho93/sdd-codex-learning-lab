import { expect, test } from '@playwright/test';

test('apresenta formulário acessível e histórico vazio', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'O que você quer explorar?' })).toBeVisible();
  await expect(page.getByRole('textbox', { name: 'Prompt', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Executar prompt' })).toBeEnabled();
  await expect(page.getByText('Nenhum experimento registrado.')).toBeVisible();
});

test('rejeita prompt vazio e devolve o foco ao campo', async ({ page }) => {
  await page.goto('/');

  await page.getByRole('button', { name: 'Executar prompt' }).click();

  await expect(page.getByRole('alert')).toHaveText('O prompt não pode estar vazio.');
  await expect(page.getByRole('textbox', { name: 'Prompt', exact: true })).toBeFocused();
  await expect(page.getByRole('heading', { name: 'Resultado' })).toBeHidden();
});

test('executa por teclado e atualiza histórico sem recarregar', async ({ page }) => {
  const prompt = `Playwright SDD ${Date.now()}`;
  await page.goto('/');

  const promptField = page.getByRole('textbox', { name: 'Prompt', exact: true });
  const submitButton = page.getByRole('button', { name: 'Executar prompt' });
  await promptField.fill(prompt);
  await promptField.press('Tab');
  await expect(submitButton).toBeFocused();
  await submitButton.press('Enter');

  await expect(page.getByRole('heading', { name: 'Resultado' })).toBeVisible();
  await expect(page.getByText(/Simulação local:/)).toContainText(prompt);
  await expect(page.getByText(/Experimento salvo:/)).toBeVisible();
  await expect(
    page.getByRole('button', { name: `Ver detalhes do experimento: ${prompt}` }),
  ).toBeVisible();
});

test('duplo clique rápido cria somente um experimento', async ({ page }) => {
  const prompt = `Sem duplicar ${Date.now()}`;
  await page.goto('/');
  await page.getByRole('textbox', { name: 'Prompt', exact: true }).fill(prompt);

  await page.getByRole('button', { name: 'Executar prompt' }).evaluate((button) => {
    const submitButton = button as HTMLButtonElement;
    submitButton.click();
    submitButton.click();
  });

  await expect(page.getByRole('heading', { name: 'Resultado' })).toBeVisible();
  await expect(
    page.getByRole('button', { name: `Ver detalhes do experimento: ${prompt}` }),
  ).toHaveCount(1);
});

test('abre todos os detalhes reproduzíveis pelo histórico', async ({ page }) => {
  const prompt = `Detalhes E2E ${Date.now()}`;
  await page.goto('/');
  await page.getByRole('textbox', { name: 'Prompt', exact: true }).fill(prompt);
  await page.getByRole('button', { name: 'Executar prompt' }).click();

  await page
    .getByRole('button', { name: `Ver detalhes do experimento: ${prompt}` })
    .click();

  const details = page.getByRole('region', { name: 'Detalhes do experimento' });
  await expect(details).toBeFocused();
  await expect(details).toContainText(prompt);
  await expect(details).toContainText('fake');
  await expect(details).toContainText('deterministic-study-v1');
  await expect(details).toContainText('completed');
});
