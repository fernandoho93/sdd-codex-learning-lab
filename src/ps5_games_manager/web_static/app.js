const $ = (selector) => document.querySelector(selector);

const elements = {
  create: $('#create-button'), search: $('#search'), genre: $('#genre-filter'),
  status: $('#status-filter'), clear: $('#clear-filters'), message: $('#message'),
  state: $('#collection-state'), list: $('#game-list'), count: $('#game-count'),
  formDialog: $('#game-dialog'), form: $('#game-form'), formTitle: $('#form-title'),
  formSummary: $('#form-summary'), save: $('#save-game'), detailsDialog: $('#details-dialog'),
  detailsTitle: $('#details-title'), detailsContent: $('#details-content'),
  deleteDialog: $('#delete-dialog'), deleteName: $('#delete-name'),
  cancelDelete: $('#cancel-delete'), confirmDelete: $('#confirm-delete'),
  catalogQuery: $('#catalog-query'), catalogSearch: $('#catalog-search'),
  catalogState: $('#catalog-state'), catalogResults: $('#catalog-results'),
  sourceAttribution: $('#source-attribution'),
};

const labels = {
  status: { wishlist: 'Desejo comprar', purchased: 'Comprado', playing: 'Jogando', completed: 'Concluído', abandoned: 'Abandonado' },
  media: { physical: 'Física', digital: 'Digital' },
};

let games = [];
let deleteTarget = null;
let lastDeleteTrigger = null;
let catalogCandidates = new Map();
let searchTimer = null;

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const payload = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) {
    const error = payload?.error || { code: 'network_error', message: 'Não foi possível concluir a operação.' };
    throw error;
  }
  return payload;
}

function showMessage(text, error = false) {
  elements.message.textContent = text;
  elements.message.classList.toggle('error', error);
}

async function loadGames() {
  elements.state.hidden = false;
  elements.state.textContent = 'Carregando jogos...';
  elements.list.replaceChildren();
  const query = new URLSearchParams();
  if (elements.search.value.trim()) query.set('search', elements.search.value.trim());
  if (elements.genre.value) query.set('genre', elements.genre.value);
  if (elements.status.value) query.set('status', elements.status.value);
  try {
    const payload = await api(`/api/games${query.size ? `?${query}` : ''}`);
    games = payload.items;
    updateGenres(payload.filters.genres);
    renderGames();
  } catch (error) {
    games = [];
    elements.count.textContent = '';
    elements.state.hidden = false;
    elements.state.textContent = error.message || 'Não foi possível carregar os jogos.';
    showMessage(elements.state.textContent, true);
  }
}

function updateGenres(genres) {
  const selected = elements.genre.value;
  elements.genre.replaceChildren(new Option('Todos', ''));
  for (const genre of genres) elements.genre.add(new Option(genre, genre));
  elements.genre.value = genres.includes(selected) ? selected : '';
}

function renderGames() {
  elements.list.replaceChildren();
  elements.count.textContent = `${games.length}`;
  if (!games.length) {
    const hasQuery = elements.search.value.trim() || elements.genre.value || elements.status.value;
    elements.state.textContent = hasQuery
      ? 'Nenhum jogo corresponde à pesquisa e aos filtros.'
      : 'Nenhum jogo cadastrado. Cadastre seu primeiro jogo.';
    elements.state.hidden = false;
    return;
  }
  elements.state.hidden = true;
  for (const game of games) elements.list.append(gameCard(game));
}

function gameCard(game) {
  const article = document.createElement('article');
  article.className = 'game-card';
  article.dataset.id = game.id;
  article.append(cover(game));

  const body = document.createElement('div');
  body.className = 'card-body';
  const title = document.createElement('h3');
  title.textContent = game.name;
  const meta = document.createElement('p');
  meta.className = 'meta';
  meta.textContent = `${game.genre}${game.release_date ? ` • ${formatDate(game.release_date)}` : ''}`;
  body.append(title, meta, badge(labels.status[game.status]), badge(labels.media[game.media_type]));
  if (game.personal_rating !== null) body.append(badge(`Nota ${game.personal_rating.toFixed(1)}`));
  if (game.source_name && game.source_url) body.append(attribution(game.source_name, game.source_url));

  const actions = document.createElement('div');
  actions.className = 'card-actions';
  actions.append(
    actionButton('Detalhes', 'details', game.id, 'secondary'),
    actionButton('Editar', 'edit', game.id, 'secondary'),
    actionButton('Excluir', 'delete', game.id, 'danger'),
  );
  body.append(actions);
  article.append(body);
  return article;
}

function cover(game) {
  const wrapper = document.createElement('div');
  wrapper.className = 'cover';
  const fallback = document.createElement('span');
  fallback.textContent = `Sem capa para ${game.name}`;
  if (!game.cover_url) {
    wrapper.append(fallback);
    return wrapper;
  }
  const image = document.createElement('img');
  image.src = game.cover_url;
  image.alt = `Capa de ${game.name}`;
  image.loading = 'lazy';
  image.addEventListener('error', () => image.replaceWith(fallback), { once: true });
  wrapper.append(image);
  return wrapper;
}

function badge(text) {
  const span = document.createElement('span');
  span.className = 'badge';
  span.textContent = text;
  return span;
}

function attribution(name, url) {
  const p = document.createElement('p');
  p.className = 'attribution';
  p.append('Dados e imagens fornecidos por ');
  const link = document.createElement('a');
  link.href = url;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.textContent = name;
  p.append(link);
  return p;
}

function actionButton(text, action, id, className) {
  const button = document.createElement('button');
  button.type = 'button'; button.textContent = text; button.dataset.action = action;
  button.dataset.id = id; button.className = className;
  button.setAttribute('aria-label', `${text} ${games.find((g) => g.id === id)?.name || 'jogo'}`);
  return button;
}

function openCreate() {
  elements.form.reset();
  clearFormErrors();
  $('#game-id').value = '';
  clearSource();
  clearCatalog();
  elements.formTitle.textContent = 'Cadastrar jogo';
  elements.save.textContent = 'Salvar jogo';
  elements.formDialog.showModal();
  $('#name').focus();
}

async function openEdit(id) {
  try {
    const game = await api(`/api/games/${encodeURIComponent(id)}`);
    elements.form.reset(); clearFormErrors(); clearCatalog(); fillForm(game);
    $('#game-id').value = game.id;
    elements.formTitle.textContent = `Editar ${game.name}`;
    elements.save.textContent = 'Salvar alterações';
    elements.formDialog.showModal();
    $('#name').focus();
  } catch (error) { showMessage(error.message, true); await loadGames(); }
}

function fillForm(game) {
  for (const id of ['name', 'genre', 'developer', 'publisher', 'release-date', 'cover-url', 'description', 'notes']) {
    const key = id.replaceAll('-', '_');
    $(`#${id}`).value = game[key] ?? '';
  }
  $('#media-type').value = game.media_type ?? '';
  $('#game-status').value = game.status ?? '';
  $('#personal-rating').value = game.personal_rating ?? '';
  $('#source-name').value = game.source_name ?? '';
  $('#source-url').value = game.source_url ?? '';
  renderSourceAttribution();
}

function formPayload() {
  const rating = $('#personal-rating').value;
  return {
    name: $('#name').value, description: $('#description').value, genre: $('#genre').value,
    developer: $('#developer').value, publisher: $('#publisher').value,
    release_date: $('#release-date').value, media_type: $('#media-type').value,
    status: $('#game-status').value, personal_rating: rating === '' ? null : Number(rating),
    cover_url: $('#cover-url').value, notes: $('#notes').value,
    source_name: $('#source-name').value, source_url: $('#source-url').value,
  };
}

async function submitForm(event) {
  event.preventDefault(); clearFormErrors();
  if (!elements.form.checkValidity()) {
    elements.form.reportValidity();
    elements.formSummary.textContent = 'Revise os campos obrigatórios e os formatos informados.';
    return;
  }
  const id = $('#game-id').value;
  setBusy(elements.save, true, id ? 'Salvando...' : 'Cadastrando...');
  try {
    const game = await api(id ? `/api/games/${encodeURIComponent(id)}` : '/api/games', {
      method: id ? 'PUT' : 'POST', body: JSON.stringify(formPayload()),
    });
    elements.formDialog.close();
    showMessage(id ? `${game.name} foi atualizado.` : `${game.name} foi cadastrado.`);
    await loadGames();
  } catch (error) {
    elements.formSummary.textContent = error.message || 'Não foi possível salvar o jogo.';
    for (const [field, message] of Object.entries(error.fields || {})) {
      const target = document.querySelector(`[data-error-for="${field}"]`);
      if (target) target.textContent = message;
    }
    showMessage(elements.formSummary.textContent, true);
  } finally { setBusy(elements.save, false, id ? 'Salvar alterações' : 'Salvar jogo'); }
}

function clearFormErrors() {
  elements.formSummary.textContent = '';
  document.querySelectorAll('.field-error').forEach((item) => { item.textContent = ''; });
}

async function openDetails(id) {
  try {
    const game = await api(`/api/games/${encodeURIComponent(id)}`);
    elements.detailsTitle.textContent = game.name;
    const wrapper = document.createElement('div'); wrapper.className = 'details-grid';
    wrapper.append(cover(game));
    const content = document.createElement('div');
    const dl = document.createElement('dl');
    const rows = [
      ['Gênero', game.genre], ['Status', labels.status[game.status]], ['Mídia', labels.media[game.media_type]],
      ['Desenvolvedora', game.developer], ['Publicadora', game.publisher], ['Lançamento', game.release_date && formatDate(game.release_date)],
      ['Nota', game.personal_rating !== null ? game.personal_rating.toFixed(1) : null], ['Descrição', game.description],
      ['Observações', game.notes], ['Criado em', formatDateTime(game.created_at)], ['Atualizado em', formatDateTime(game.updated_at)],
    ];
    for (const [term, value] of rows) {
      const dt = document.createElement('dt'); dt.textContent = term;
      const dd = document.createElement('dd'); dd.textContent = value || 'Não informado';
      dl.append(dt, dd);
    }
    content.append(dl);
    if (game.source_name && game.source_url) content.append(attribution(game.source_name, game.source_url));
    wrapper.append(content); elements.detailsContent.replaceChildren(wrapper);
    elements.detailsDialog.showModal(); elements.detailsTitle.focus();
  } catch (error) { showMessage(error.message, true); await loadGames(); }
}

function askDelete(id, trigger) {
  const game = games.find((item) => item.id === id);
  if (!game) return;
  deleteTarget = game; lastDeleteTrigger = trigger;
  elements.deleteName.textContent = game.name;
  elements.deleteDialog.showModal(); elements.cancelDelete.focus();
}

async function confirmDelete() {
  if (!deleteTarget) return;
  setBusy(elements.confirmDelete, true, 'Excluindo...');
  try {
    await api(`/api/games/${encodeURIComponent(deleteTarget.id)}`, { method: 'DELETE' });
    const name = deleteTarget.name;
    elements.deleteDialog.close(); deleteTarget = null;
    showMessage(`${name} foi excluído.`); await loadGames(); elements.create.focus();
  } catch (error) {
    elements.deleteDialog.close(); deleteTarget = null;
    showMessage(error.message, true); await loadGames();
  } finally { setBusy(elements.confirmDelete, false, 'Excluir jogo'); }
}

function cancelDelete() {
  elements.deleteDialog.close(); deleteTarget = null;
  lastDeleteTrigger?.focus(); lastDeleteTrigger = null;
}

async function searchCatalog() {
  const query = elements.catalogQuery.value.trim();
  if (!query) { elements.catalogState.textContent = 'Informe um título para pesquisar.'; return; }
  setBusy(elements.catalogSearch, true, 'Pesquisando...');
  elements.catalogState.textContent = 'Consultando o catálogo RAWG...';
  elements.catalogResults.replaceChildren(); catalogCandidates.clear();
  try {
    const payload = await api(`/api/catalog/search?query=${encodeURIComponent(query)}`);
    elements.catalogState.textContent = payload.items.length ? `${payload.items.length} resultado(s).` : 'Nenhum jogo de PS5 encontrado. Continue com o cadastro manual.';
    for (const candidate of payload.items) {
      catalogCandidates.set(candidate.external_id, candidate);
      const row = document.createElement('div'); row.className = 'catalog-item';
      const text = document.createElement('span'); text.textContent = `${candidate.name}${candidate.release_date ? ` • ${formatDate(candidate.release_date)}` : ''}`;
      const button = document.createElement('button'); button.type = 'button'; button.className = 'secondary';
      button.textContent = 'Usar estes dados'; button.dataset.candidate = candidate.external_id;
      row.append(text, button); elements.catalogResults.append(row);
    }
    elements.catalogResults.append(attribution('RAWG', payload.attribution.url));
  } catch (error) {
    elements.catalogState.textContent = `${error.message} O cadastro manual continua disponível.`;
  } finally { setBusy(elements.catalogSearch, false, 'Pesquisar'); }
}

function applyCandidate(id) {
  const candidate = catalogCandidates.get(id); if (!candidate) return;
  fillForm({ ...formPayload(), ...Object.fromEntries(Object.entries(candidate).filter(([, value]) => value !== null)) });
  $('#source-name').value = candidate.source_name;
  $('#source-url').value = candidate.source_url;
  renderSourceAttribution();
  elements.catalogState.textContent = `Dados de ${candidate.name} aplicados. Revise antes de salvar.`;
  $('#name').focus();
}

function renderSourceAttribution() {
  elements.sourceAttribution.replaceChildren();
  const name = $('#source-name').value; const url = $('#source-url').value;
  if (!name || !url) { elements.sourceAttribution.hidden = true; return; }
  elements.sourceAttribution.hidden = false;
  elements.sourceAttribution.append(attribution(name, url));
}

function clearSource() { $('#source-name').value = ''; $('#source-url').value = ''; renderSourceAttribution(); }
function clearCatalog() { elements.catalogQuery.value = ''; elements.catalogState.textContent = ''; elements.catalogResults.replaceChildren(); catalogCandidates.clear(); }
function setBusy(button, busy, text) { button.disabled = busy; button.textContent = text; }
function formatDate(value) { return new Intl.DateTimeFormat('pt-BR', { timeZone: 'UTC' }).format(new Date(`${value}T00:00:00Z`)); }
function formatDateTime(value) { return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(value)); }

elements.create.addEventListener('click', openCreate);
elements.form.addEventListener('submit', submitForm);
elements.genre.addEventListener('change', loadGames);
elements.status.addEventListener('change', loadGames);
elements.search.addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(loadGames, 250); });
elements.clear.addEventListener('click', () => { elements.search.value = ''; elements.genre.value = ''; elements.status.value = ''; loadGames(); });
elements.list.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]'); if (!button) return;
  if (button.dataset.action === 'details') openDetails(button.dataset.id);
  if (button.dataset.action === 'edit') openEdit(button.dataset.id);
  if (button.dataset.action === 'delete') askDelete(button.dataset.id, button);
});
elements.cancelDelete.addEventListener('click', cancelDelete);
elements.confirmDelete.addEventListener('click', confirmDelete);
elements.catalogSearch.addEventListener('click', searchCatalog);
elements.catalogResults.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-candidate]');
  if (button) applyCandidate(button.dataset.candidate);
});
document.querySelectorAll('[data-close]').forEach((button) => button.addEventListener('click', () => $(`#${button.dataset.close}`).close()));

loadGames();
