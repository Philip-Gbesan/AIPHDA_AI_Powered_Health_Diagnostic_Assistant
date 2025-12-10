/* admin.js
   Frontend logic for Admin Dashboard (fetches real backend endpoints).
   Expects the backend admin blueprint to be mounted under http://127.0.0.1:5000/api/admin/*,
   as in your snippets (e.g. GET http://127.0.0.1:5000/api/admin/logs, 
   GET http://127.0.0.1:5000/api/admin/models, POST http://127.0.0.1:5000/api/admin/upload-dataset).
*/

(() => {
  const totalChecksEl = document.getElementById('totalChecks');
  const successfulChecksEl = document.getElementById('successfulChecks');
  const modelRetrainsEl = document.getElementById('modelRetrains');
  const savedModelsEl = document.getElementById('savedModels');

  const dragArea = document.getElementById('dragArea');
  const fileInput = document.getElementById('fileInput');
  const selectedFilesEl = document.getElementById('selectedFiles');

  const syncDataBtn = document.getElementById('syncDataBtn');
  // const saveModelBtn = document.getElementById('saveModelBtn');
  const retrainBtn = document.getElementById('retrainBtn');

  const syncStatus = document.getElementById('syncStatus');
  const actionStatus = document.getElementById('actionStatus');

  let selectedFiles = [];

  /* ---------- UTIL ---------- */
  function fmt(n) { return (n === null || n === undefined) ? '—' : String(n); }
  function setStatus(msg, el = actionStatus) { el.textContent = msg; }

  /* ---------- LOAD STATS ---------- */
  async function loadStats() {
    try {
      const logsResp = await fetch('http://127.0.0.1:5000/api/admin/logs');
      const logs = logsResp.ok ? await logsResp.json() : [];
      const total = Array.isArray(logs) ? logs.length : 0;
      const successful = Array.isArray(logs) ? logs.filter(l => l.predictions && l.predictions !== '[]').length : 0;

      totalChecksEl.textContent = fmt(total);
      successfulChecksEl.textContent = fmt(successful);

      const modelsResp = await fetch('http://127.0.0.1:5000/api/admin/models');
      const models = modelsResp.ok ? await modelsResp.json() : [];
      savedModelsEl.textContent = fmt(Array.isArray(models) ? models.length : 0);
      modelRetrainsEl.textContent = fmt(Array.isArray(models) ? models.length : 0);

      const datasetsResp = await fetch('http://127.0.0.1:5000/api/admin/datasets');
      const datasets = datasetsResp.ok ? await datasetsResp.json() : [];
      renderDatasets(datasets);

    } catch (err) {
      console.error('loadStats error', err);
      setStatus('Failed to load stats. Check backend.', syncStatus);
      setStatus('Failed to load stats. Check backend.', actionStatus);
    }
  }

  function renderDatasets(list) {
    datasetsList.innerHTML = '';
    if (!Array.isArray(list) || list.length === 0) {
      datasetsList.innerHTML = '<div class="small" style="color:var(--muted)">No uploaded datasets</div>';
      return;
    }
  }

  /* ---------- FILE PICK / DRAG & DROP ---------- */
  function updateSelectedFilesUI() {
    if (!selectedFiles.length) {
      selectedFilesEl.textContent = 'No files selected';
      syncDataBtn.disabled = true;
      return;
    }
    const names = selectedFiles.map(f => f.name).join(', ');
    selectedFilesEl.textContent = names;
    syncDataBtn.disabled = false;
  }

  dragArea.addEventListener('click', () => fileInput.click());
  dragArea.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') fileInput.click(); });

  dragArea.addEventListener('dragover', (e) => { e.preventDefault(); dragArea.style.borderColor = 'rgba(25,138,230,0.3)'; });
  dragArea.addEventListener('dragleave', (e) => { e.preventDefault(); dragArea.style.borderColor = 'rgba(25,138,230,0.12)'; });

  dragArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dragArea.style.borderColor = 'rgba(25,138,230,0.12)';
    const files = Array.from(e.dataTransfer.files || []).filter(f => f.name.toLowerCase().endsWith('.csv'));
    if (files.length === 0) {
      alert('Please drop CSV files only.');
      return;
    }
    selectedFiles = files;
    updateSelectedFilesUI();
  });

  fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files || []).filter(f => f.name.toLowerCase().endsWith('.csv'));
    selectedFiles = files;
    updateSelectedFilesUI();
  });

  /* ---------- SYNC DATA (upload selected files) ---------- */
  async function syncData() {
    if (!selectedFiles.length) return alert('No files selected');

    syncStatus.textContent = 'Uploading...';
    syncDataBtn.disabled = true;

    try {
      for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];
        const form = new FormData();
        form.append('file', file, file.name);

        const resp = await fetch('http://127.0.0.1:5000/api/admin/upload-dataset', {
          method: 'POST',
          body: form
        });

        if (!resp.ok) {
          const text = await resp.text();
          throw new Error('Upload failed: ' + (text || resp.status));
        }
        setStatus('Data has been synced with the raw training dataset.', syncStatus);
        setStatus('Sync complete. You may preprocess & retrain.', actionStatus);
      }
      
      await loadStats();

      selectedFiles = [];
      fileInput.value = '';
      updateSelectedFilesUI();
    } catch (err) {
      console.error('syncData error', err);
      setStatus('Sync (Dataset upload) failed: ' + (err.message || ''), syncStatus);
    } finally {
      syncDataBtn.disabled = false;
    }
  }

  // /* ---------- SAVE MODEL ---------- */
  // async function saveModel() {
  //   syncStatus.textContent = 'Saving Model...';
  //   try {
  //     const resp = await fetch('http://127.0.0.1:5000/api/admin/save-model', { method: 'POST' });
  //     const data = await resp.json();

  //     if (resp.ok) {
  //       syncStatus.textContent = 'ML Model Saved Successfully';
  //       await loadStats();   // <-- update the savedModels counter immediately
  //     } else {
  //       syncStatus.textContent = setStatus("Save model failed: " + (data.error || ""), actionStatus);
  //     }

  //   } catch(err) {
  //     console.error('saveModel error', err);
  //     syncStatus.textContent = setStatus("Save model failed: " + err.message, actionStatus);
  //   }
  // }


  /* ---------- RETRAIN ---------- */
  async function retrain() {
    if (!confirm('This will retrain the ML model with the master dataset. Continue?')) return;
    setStatus('Retraining started...');
    try {
      const resp = await fetch('http://127.0.0.1:5000/api/admin/retrain', { method: 'POST' });
      const data = await resp.json();
      if(resp.ok) setStatus("Retrain triggered. Check logs for progress.", actionStatus);
      else setStatus("Retrain failed: " + (data.error || ""), actionStatus);
    } catch(err) {
      console.error('retrain error', err);
      setStatus("Retrain failed: " + err.message, actionStatus);
    }
  }

  /* ---------- EVENTS ---------- */
  syncDataBtn.addEventListener('click', async (e) => {
      e.preventDefault();       // prevent page reload
      syncData();               // call your existing function
  });

  // saveModelBtn.addEventListener('click', async (e) => {
  //     e.preventDefault();       // prevent page reload
  //     saveModel();              // call your existing function
  // });

  retrainBtn.addEventListener('click', async (e) => {
      e.preventDefault();       // prevent page reload
      retrain();                // call your existing function
  });


  /* ---------- INITIALIZE ---------- */
  loadStats();
  setInterval(loadStats, 60 * 1200);

  /* ----------- PROGRESS BAR ----------- */
  function setProgress(value) {
    const container = document.getElementById('progressContainer');
    const bar = document.getElementById('progressBar');

    container.style.display = "block";
    bar.style.width = value + "%";
  }

  /* ----------- PREPROCESS RAW DATA ----------- */
  async function preprocessData() {
    if (!confirm("Preprocess ALL raw datasets into a single master dataset?")) return;

    setProgress(10);
    setStatus("Preprocessing in progress !", syncStatus);
    setStatus("Preprocessing raw data...", actionStatus);

    try {
      const resp = await fetch("http://127.0.0.1:5000/api/admin/preprocess", {
        method: "POST",
      });

      const data = await resp.json();

      if (resp.ok) {
        setProgress(100);
        setStatus("Preprocessing successful.", syncStatus);
        setStatus("Preprocessing complete. Master dataset ready.", actionStatus);
      } else {
        setStatus("Preprocess failed: " + (data.error || "", actionStatus));
        setStatus("Preprocess failed: " + (data.error || "", actionStatus));
        setProgress(0);
      }

    } catch (err) {
      console.error(err);
      setStatus("Preprocess failed: " + err.message, syncStatus);
      setStatus("Preprocess failed: " + err.message, actionStatus);
      setProgress(0);
    }
  }

  /* ----------- REVERT TO LAST MODEL ----------- */
  async function revertModel() {
    if (!confirm("This will restore the PREVIOUS model version.\n\nThis action cannot be undone.\nContinue?")) return;

    setStatus("Reverting model...", syncStatus);

    try {
      const resp = await fetch("http://127.0.0.1:5000/api/admin/revert-model", {
        method: "POST"
      });

      const data = await resp.json();

      if (resp.ok) {
        setStatus("Model reverted successfully.", syncStatus);
        setStatus("Model reverted to the previous model successfully.", actionStatus);
        loadStats();
      } else {
        setStatus("Revert failed: " + (data.error || ""), syncStatus);
        setStatus(" ", actionStatus);
      }

    } catch (err) {
      console.error(err);
      setStatus("Revert failed: " + err.message, syncStatus);
      etStatus(" ", actionStatus);
    }
  }

  /* ----------- DOWNLOAD CURRENT MODEL ----------- */
  async function downloadModel() {
    setStatus("Preparing model download...", syncStatus);

    try {
      const resp = await fetch("http://127.0.0.1:5000/api/admin/download-model");

      if (!resp.ok) {
        const msg = await resp.text();
        setStatus("Download failed: " + msg, syncStatus);
        return;
      }

      // actual file blob
      const blob = await resp.blob();

      // create temporary download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "current_model_bundle.zip";
      document.body.appendChild(a);
      a.click();
      a.remove();

      setStatus("Current Model has been downloaded to a zip file.", syncStatus);
      setStatus("Download completed.", actionStatus);
    } catch (err) {
      setStatus("Download failed due to Backend: " + err.message, syncStatus);
      setStatus("Download Failed: " + err.message, actionStatus);
    }
  }

  /* ----------- BUTTON EVENTS ----------- */
  document.getElementById("preprocessBtn")
    .addEventListener("click", (e) => { e.preventDefault(); preprocessData(); });

  document.getElementById("revertModelBtn")
    .addEventListener("click", (e) => { e.preventDefault(); revertModel(); });

  document.getElementById("downloadModelBtn")
    .addEventListener("click", (e) => { e.preventDefault(); downloadModel(); });


})();

