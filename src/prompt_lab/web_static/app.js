const form = document.querySelector('#prompt-form');
const promptInput = document.querySelector('#prompt');
const submitButton = document.querySelector('#submit-prompt');
const characterCount = document.querySelector('#character-count');
const statusMessage = document.querySelector('#status-message');
const resultPanel = document.querySelector('#result-panel');
const resultResponse = document.querySelector('#result-response');
const resultId = document.querySelector('#result-id');
const historyList = document.querySelector('#history-list');
const historyStatus = document.querySelector('#history-status');
const refreshHistoryButton = document.querySelector('#refresh-history');
const detailsPanel = document.querySelector('#details-panel');

function updateCharacterCount() {
  characterCount.textContent = `${promptInput.value.length.toLocaleString('pt-BR')} / 10.000`;
}

function setStatus(message, isError = false) {
  statusMessage.textContent = message;
  statusMessage.classList.toggle('error', isError);
  statusMessage.setAttribute('role', isError ? 'alert' : 'status');
}

function setLoading(loading) {
  submitButton.disabled = loading;
  submitButton.textContent = loading ? 'Executando...' : 'Executar prompt';
  promptInput.setAttribute('aria-busy', String(loading));
}

async function readJson(response) {
  try {
    return await response.json();
  } catch {
    throw new Error('O servidor retornou uma resposta inválida. Tente novamente.');
  }
}

async function requestJson(url, options) {
  const response = await fetch(url, options);
  const payload = await readJson(response);
  if (!response.ok) {
    throw new Error(payload.error || 'Não foi possível concluir a operação.');
  }
  return payload;
}

function renderResult(experiment) {
  resultResponse.textContent = experiment.response;
  resultId.textContent = experiment.id;
  resultPanel.hidden = false;
}

function formatDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.valueOf())
    ? value
    : new Intl.DateTimeFormat('pt-BR', {
        dateStyle: 'short',
        timeStyle: 'medium',
        timeZone: 'UTC',
      }).format(date) + ' UTC';
}

function renderHistory(items) {
  historyList.replaceChildren();
  if (items.length === 0) {
    historyStatus.textContent = 'Nenhum experimento registrado.';
    return;
  }

  historyStatus.textContent = `${items.length} experimento${items.length === 1 ? '' : 's'} registrado${items.length === 1 ? '' : 's'}.`;
  for (const experiment of items) {
    const item = document.createElement('li');
    const button = document.createElement('button');
    const prompt = document.createElement('span');
    const metadata = document.createElement('span');
    const summary = experiment.prompt.length > 72
      ? `${experiment.prompt.slice(0, 72)}…`
      : experiment.prompt;

    button.type = 'button';
    button.className = 'history-button';
    button.setAttribute('aria-label', `Ver detalhes do experimento: ${experiment.prompt}`);
    button.dataset.experimentId = experiment.id;
    prompt.className = 'history-prompt';
    prompt.textContent = summary;
    metadata.className = 'history-meta';
    metadata.textContent = `${formatDate(experiment.created_at)} · ${experiment.id}`;
    button.append(prompt, metadata);
    item.append(button);
    historyList.append(item);
  }
}

async function loadHistory() {
  historyStatus.textContent = 'Carregando histórico...';
  try {
    const payload = await requestJson('/api/experiments');
    renderHistory(payload.items);
    if (payload.warnings.length > 0) {
      historyStatus.textContent += ` ${payload.warnings.length} registro(s) inválido(s) foram ignorados.`;
    }
  } catch (error) {
    historyList.replaceChildren();
    historyStatus.textContent = `${error.message} Use “Atualizar histórico” para tentar novamente.`;
  }
}

function setDetail(id, value) {
  document.querySelector(id).textContent = value;
}

function renderDetails(experiment) {
  setDetail('#detail-id', experiment.id);
  setDetail('#detail-created-at', experiment.created_at);
  setDetail('#detail-provider', experiment.provider);
  setDetail('#detail-model', experiment.model);
  setDetail('#detail-status', experiment.status);
  setDetail('#detail-prompt', experiment.prompt);
  setDetail('#detail-response', experiment.response);
  detailsPanel.hidden = false;
  detailsPanel.focus();
}

async function showDetails(experimentId) {
  setStatus('Carregando detalhes...');
  try {
    const experiment = await requestJson(`/api/experiments/${encodeURIComponent(experimentId)}`);
    renderDetails(experiment);
    setStatus('Detalhes carregados.');
  } catch (error) {
    setStatus(error.message, true);
  }
}

promptInput.addEventListener('input', updateCharacterCount);
refreshHistoryButton.addEventListener('click', loadHistory);
historyList.addEventListener('click', (event) => {
  const button = event.target.closest('[data-experiment-id]');
  if (button) {
    showDetails(button.dataset.experimentId);
  }
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const prompt = promptInput.value.trim();
  resultPanel.hidden = true;
  detailsPanel.hidden = true;

  if (!prompt) {
    setStatus('O prompt não pode estar vazio.', true);
    promptInput.focus();
    return;
  }
  if (prompt.length > 10_000) {
    setStatus('O prompt deve ter no máximo 10.000 caracteres.', true);
    promptInput.focus();
    return;
  }

  setLoading(true);
  setStatus('Executando o prompt localmente...');
  try {
    const experiment = await requestJson('/api/experiments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    renderResult(experiment);
    setStatus('Experimento executado e salvo com sucesso.');
    await loadHistory();
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    setLoading(false);
  }
});

updateCharacterCount();
loadHistory();
