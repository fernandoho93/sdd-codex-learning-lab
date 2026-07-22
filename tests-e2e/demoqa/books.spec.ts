import { expect, test } from '@playwright/test';

import { BooksPage, REFERENCE_BOOK } from './pages/books.page';

test.describe('DemoQA Books', () => {
  test('US1: apresenta os elementos essenciais do catálogo', async ({ page }) => {
    const books = new BooksPage(page);

    await books.open();

    await expect(books.searchBox).toBeVisible();
    await expect(books.bookLinks.first()).toBeVisible();
    await expect(books.bookLink(REFERENCE_BOOK.title)).toBeVisible();
  });

  test('US2: filtra, esvazia e restaura o catálogo', async ({ page }) => {
    const books = new BooksPage(page);

    await books.open();
    await books.searchFor(REFERENCE_BOOK.title);

    await expect(books.bookLink(REFERENCE_BOOK.title)).toBeVisible();
    await expect(books.bookLinks).toHaveCount(1);

    await books.searchFor('livro-que-nao-existe-qa-2026');
    await expect(books.bookLinks).toHaveCount(0);

    await books.clearSearch();
    await expect(books.bookLinks.first()).toBeVisible();
    await expect(books.bookLink(REFERENCE_BOOK.title)).toBeVisible();
  });

  test('US3: apresenta os detalhes do livro e retorna ao catálogo', async ({ page }) => {
    const books = new BooksPage(page);

    await books.open();
    await books.openBook(REFERENCE_BOOK.title, REFERENCE_BOOK.isbn);

    await expect(books.detailValue(REFERENCE_BOOK.title)).toHaveText(
      REFERENCE_BOOK.title,
    );
    await expect(books.detailValue(REFERENCE_BOOK.author)).toHaveText(
      REFERENCE_BOOK.author,
    );
    await expect(books.detailValue(REFERENCE_BOOK.isbn)).toHaveText(
      REFERENCE_BOOK.isbn,
    );

    await books.returnToStore();
    await expect(books.searchBox).toBeVisible();
  });
});
