import {
  expect,
  test,
  type APIResponse,
  type TestInfo,
} from '@playwright/test';

interface Book {
  isbn: string;
  title: string;
  subTitle: string;
  author: string;
  publish_date: string;
  publisher: string;
  pages: number;
  description: string;
  website: string;
}

interface BookCollection {
  books: Book[];
}

interface ApiError {
  code: string;
  message: string;
}

const REFERENCE_BOOK = {
  isbn: '9781449325862',
  title: 'Git Pocket Guide',
  author: 'Richard E. Silverman',
} as const;

const UNKNOWN_ISBN = '0000000000000';

const REQUEST_TIMEOUT = 15_000;

function expectBookContract(value: unknown): Book {
  expect(value).toBeTruthy();
  expect(typeof value).toBe('object');

  const book = value as Record<string, unknown>;
  expect(book.isbn).toEqual(expect.stringMatching(/^\d{13}$/));
  expect(book.title).toEqual(expect.any(String));
  expect(book.subTitle).toEqual(expect.any(String));
  expect(book.author).toEqual(expect.any(String));
  expect(book.publish_date).toEqual(expect.any(String));
  expect(book.publisher).toEqual(expect.any(String));
  expect(book.pages).toEqual(expect.any(Number));
  expect(book.description).toEqual(expect.any(String));
  expect(book.website).toEqual(expect.any(String));
  expect((book.title as string).length).toBeGreaterThan(0);
  expect((book.author as string).length).toBeGreaterThan(0);
  expect((book.publisher as string).length).toBeGreaterThan(0);
  expect(Number.isInteger(book.pages)).toBe(true);
  expect(book.pages as number).toBeGreaterThan(0);

  return book as unknown as Book;
}

function expectBookCollection(value: unknown): BookCollection {
  expect(value).toBeTruthy();
  expect(typeof value).toBe('object');

  const collection = value as Record<string, unknown>;
  expect(Array.isArray(collection.books)).toBe(true);
  const books = (collection.books as unknown[]).map(expectBookContract);
  expect(books.length).toBeGreaterThan(0);

  return { books };
}

async function captureJsonResponse(
  testInfo: TestInfo,
  name: string,
  method: string,
  resource: string,
  response: APIResponse,
): Promise<unknown> {
  const rawBody = await response.text();
  let body: unknown = rawBody;
  let parseError: string | undefined;

  try {
    body = JSON.parse(rawBody) as unknown;
  } catch (error) {
    parseError = error instanceof Error ? error.message : String(error);
  }

  await testInfo.attach(name, {
    contentType: 'application/json',
    body: Buffer.from(
      JSON.stringify(
        {
          request: { method, resource },
          response: {
            status: response.status(),
            headers: response.headers(),
            body,
            parseError,
          },
        },
        null,
        2,
      ),
    ),
  });

  expect(response.headers()['content-type']).toContain('application/json');
  expect(parseError, 'A resposta deve possuir JSON válido').toBeUndefined();
  return body;
}

test.describe('DemoQA Book Store API', () => {
  test('API-US1: lista o catálogo com contrato básico válido', async ({
    request,
  }, testInfo) => {
    const resource = '/BookStore/v1/Books';
    const response = await request.get(resource, { timeout: REQUEST_TIMEOUT });
    const body = await captureJsonResponse(
      testInfo,
      'catalog-response.json',
      'GET',
      resource,
      response,
    );

    expect(response.status()).toBe(200);
    const collection = expectBookCollection(body);
    expect(collection.books).toContainEqual(
      expect.objectContaining(REFERENCE_BOOK),
    );
  });

  test('API-US2: consulta um livro e confirma coerência com o catálogo', async ({
    request,
  }, testInfo) => {
    const collectionResource = '/BookStore/v1/Books';
    const collectionResponse = await request.get(collectionResource, {
      timeout: REQUEST_TIMEOUT,
    });
    const collectionBody = await captureJsonResponse(
      testInfo,
      'catalog-for-detail.json',
      'GET',
      collectionResource,
      collectionResponse,
    );

    expect(collectionResponse.status()).toBe(200);
    const collection = expectBookCollection(collectionBody);
    const listedBook = collection.books.find(
      (book) => book.isbn === REFERENCE_BOOK.isbn,
    );
    expect(listedBook).toBeDefined();

    const detailResource = '/BookStore/v1/Book';
    const detailResponse = await request.get(detailResource, {
      params: { ISBN: REFERENCE_BOOK.isbn },
      timeout: REQUEST_TIMEOUT,
    });
    const detailBody = await captureJsonResponse(
      testInfo,
      'book-detail-response.json',
      'GET',
      `${detailResource}?ISBN=${REFERENCE_BOOK.isbn}`,
      detailResponse,
    );

    expect(detailResponse.status()).toBe(200);
    const detail = expectBookContract(detailBody);
    expect(detail).toMatchObject({
      isbn: listedBook?.isbn,
      title: listedBook?.title,
      author: listedBook?.author,
    });
    expect(detail).toMatchObject(REFERENCE_BOOK);
  });

  test('API-US3: rejeita ISBN inexistente com erro de domínio', async ({
    request,
  }, testInfo) => {
    const resource = '/BookStore/v1/Book';
    const response = await request.get(resource, {
      params: { ISBN: UNKNOWN_ISBN },
      timeout: REQUEST_TIMEOUT,
    });
    const body = await captureJsonResponse(
      testInfo,
      'unknown-isbn-response.json',
      'GET',
      `${resource}?ISBN=${UNKNOWN_ISBN}`,
      response,
    );

    expect(response.status()).toBe(400);
    expect(body).toEqual(
      expect.objectContaining({
        code: '1205',
        message: expect.any(String),
      }),
    );

    const error = body as ApiError;
    expect(error.message.length).toBeGreaterThan(0);
    expect(error.message).toContain('ISBN');
    expect(error.message).toContain('not available');
  });
});
