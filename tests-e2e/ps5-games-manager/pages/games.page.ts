import { expect, type Locator, type Page } from '@playwright/test';

export type GameInput = {
  name: string;
  genre?: string;
  media?: 'physical' | 'digital';
  status?: 'wishlist' | 'purchased' | 'playing' | 'completed' | 'abandoned';
  rating?: string;
};

export class GamesPage {
  readonly page: Page;
  readonly createButton: Locator;
  readonly formDialog: Locator;
  readonly message: Locator;
  readonly search: Locator;
  readonly genreFilter: Locator;
  readonly statusFilter: Locator;

  constructor(page: Page) {
    this.page = page;
    this.createButton = page.getByRole('button', { name: 'Cadastrar jogo' });
    this.formDialog = page.getByRole('dialog', { name: /Cadastrar jogo|Editar/ });
    this.message = page.getByRole('status').first();
    this.search = page.getByLabel('Pesquisar por nome');
    this.genreFilter = page.locator('#genre-filter');
    this.statusFilter = page.locator('#status-filter');
  }

  async open(): Promise<void> {
    await this.page.goto('/');
    await expect(this.page.getByRole('heading', { name: 'PS5 Games Manager' })).toBeVisible();
  }

  async openCreate(): Promise<void> {
    await this.createButton.click();
    await expect(this.page.getByRole('heading', { name: 'Cadastrar jogo' })).toBeVisible();
  }

  async fillGame(input: GameInput): Promise<void> {
    await this.page.locator('#name').fill(input.name);
    await this.page.locator('#genre').fill(input.genre ?? 'Ação');
    await this.page.locator('#media-type').selectOption(input.media ?? 'physical');
    await this.page.locator('#game-status').selectOption(input.status ?? 'playing');
    if (input.rating) await this.page.locator('#personal-rating').fill(input.rating);
  }

  async save(): Promise<void> {
    await this.page.getByRole('button', { name: /Salvar jogo|Salvar alterações/ }).click();
  }

  async createGame(input: GameInput): Promise<void> {
    await this.openCreate();
    await this.fillGame(input);
    await this.save();
    await expect(this.card(input.name)).toBeVisible();
  }

  card(name: string): Locator {
    return this.page.locator('.game-card').filter({ has: this.page.getByRole('heading', { name, exact: true }) });
  }

  async edit(name: string): Promise<void> {
    await this.page.getByRole('button', { name: `Editar ${name}` }).click();
    await expect(this.page.getByRole('heading', { name: `Editar ${name}` })).toBeVisible();
  }

  async requestDelete(name: string): Promise<void> {
    await this.page.getByRole('button', { name: `Excluir ${name}` }).click();
    await expect(this.page.getByRole('dialog', { name: 'Excluir jogo?' })).toBeVisible();
  }
}
