import { expect, type Locator, type Page } from '@playwright/test';

export const REFERENCE_BOOK = {
  title: 'Git Pocket Guide',
  author: 'Richard E. Silverman',
  isbn: '9781449325862',
} as const;

export class BooksPage {
  readonly searchBox: Locator;
  readonly bookLinks: Locator;
  readonly titleColumn: Locator;
  readonly backToStoreButton: Locator;

  constructor(private readonly page: Page) {
    this.searchBox = page.getByPlaceholder('Type to search');
    this.bookLinks = page.getByRole('table').getByRole('link');
    this.titleColumn = page.getByRole('columnheader', { name: 'Title' });
    this.backToStoreButton = page.getByRole('button', {
      name: 'Back To Book Store',
    });
  }

  async open(): Promise<void> {
    await this.page.goto('/books');
    await expect(this.page).toHaveURL(/\/books$/);
    await expect(this.titleColumn).toBeVisible();
  }

  bookLink(title: string): Locator {
    return this.page.getByRole('link', { name: title, exact: true });
  }

  detailValue(value: string): Locator {
    return this.page.locator('#userName-value').filter({ hasText: value });
  }

  async searchFor(term: string): Promise<void> {
    await this.searchBox.fill(term);
  }

  async clearSearch(): Promise<void> {
    await this.searchBox.clear();
  }

  async openBook(title: string, isbn: string): Promise<void> {
    await this.bookLink(title).click();
    await expect(this.page).toHaveURL(new RegExp(`/books\\?search=${isbn}$`));
  }

  async returnToStore(): Promise<void> {
    await this.backToStoreButton.click();
    await expect(this.page).toHaveURL(/\/books$/);
  }
}
